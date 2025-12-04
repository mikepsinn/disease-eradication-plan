#!/usr/bin/env tsx
/**
 * Script to automatically download all files from a NotebookLM Studio tab
 * 
 * First install puppeteer:
 *   npm install --save-dev puppeteer @types/puppeteer
 * 
 * Usage:
 *   tsx scripts/download-notebooklm-files.ts <notebook-url>
 * 
 * Example:
 *   tsx scripts/download-notebooklm-files.ts "https://notebooklm.google.com/notebook/c0db63d3-f876-448a-b15c-f5760c4587a3?authuser=1"
 * 
 * Note: This script will automatically accept downloads. Make sure your browser
 * is configured to automatically save files to a specific folder, or the script
 * will handle downloads programmatically.
 */

import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

// Dynamic import for puppeteer (in case it's not installed)
let puppeteer: any;

async function loadPuppeteer() {
  try {
    puppeteer = await import('puppeteer');
    return puppeteer.default;
  } catch (error) {
    console.error('\n❌ Puppeteer is not installed!');
    console.error('Please install it first:');
    console.error('  npm install --save-dev puppeteer @types/puppeteer\n');
    process.exit(1);
  }
}

async function downloadNotebookLMFiles(notebookUrl: string) {
  const puppeteerModule = await loadPuppeteer();
  
  console.log(`\n🚀 Starting download automation for NotebookLM`);
  console.log(`📄 URL: ${notebookUrl}\n`);

  const browser = await puppeteerModule.launch({
    headless: false, // Show browser so you can see what's happening
    defaultViewport: null,
    args: ['--start-maximized'],
  });

  try {
    const page = await browser.newPage();

    // Set up automatic download acceptance
    const client = await page.target().createCDPSession();
    await client.send('Page.setDownloadBehavior', {
      behavior: 'allow',
      downloadPath: path.resolve(process.cwd(), 'downloads'),
    });

    // Navigate to the notebook
    console.log('📍 Navigating to notebook...');
    await page.goto(notebookUrl, { waitUntil: 'networkidle2', timeout: 60000 });
    await page.waitForTimeout(3000);

    // Click on Studio tab
    console.log('🎯 Clicking Studio tab...');
    const studioTabClicked = await page.evaluate(() => {
      const tabs = Array.from(document.querySelectorAll('[role="tab"]'));
      const studioTab = tabs.find(tab => {
        const text = tab.textContent?.trim().toLowerCase() || '';
        return text === 'studio';
      });
      if (studioTab) {
        (studioTab as HTMLElement).click();
        return true;
      }
      return false;
    });

    if (!studioTabClicked) {
      throw new Error('Could not find Studio tab');
    }

    await page.waitForTimeout(2000);

    // Find all More buttons by looking for buttons with aria-label containing "More"
    // or buttons that are in the file list area
    console.log('🔍 Finding all files with More buttons...');
    
    let moreButtonCount = 0;
    let attempt = 0;
    const maxAttempts = 3;

    while (attempt < maxAttempts) {
      const buttons = await page.$$('button');
      moreButtonCount = buttons.length;
      
      // Filter to find More buttons - look for buttons with specific patterns
      const moreButtons = await page.evaluate(() => {
        const allButtons = Array.from(document.querySelectorAll('button'));
        const moreButtons: number[] = [];
        
        allButtons.forEach((btn, index) => {
          const ariaLabel = btn.getAttribute('aria-label') || '';
          const text = btn.textContent?.trim() || '';
          
          // Look for More buttons - they typically have "More" in aria-label
          // or are the three-dot menu buttons
          if (ariaLabel.toLowerCase().includes('more') && 
              !ariaLabel.toLowerCase().includes('recently used') &&
              !ariaLabel.toLowerCase().includes('search')) {
            moreButtons.push(index);
          }
        });
        
        return moreButtons;
      });

      if (moreButtons.length > 0) {
        console.log(`✅ Found ${moreButtons.length} More buttons\n`);
        
        // Click each More button and download
        let downloadedCount = 0;
        for (let i = 0; i < moreButtons.length; i++) {
          try {
            console.log(`📥 Processing file ${i + 1}/${moreButtons.length}...`);
            
            // Re-query buttons each time as DOM may change
            const currentButtons = await page.$$('button');
            const buttonIndex = moreButtons[i];
            
            if (buttonIndex < currentButtons.length) {
              // Scroll button into view
              await currentButtons[buttonIndex].scrollIntoView();
              await page.waitForTimeout(500);
              
              // Click More button
              await currentButtons[buttonIndex].click();
              await page.waitForTimeout(1000);
              
              // Look for Download menu item - it has aria-label with "Download"
              const downloadFound = await page.evaluate(() => {
                const menuItems = Array.from(document.querySelectorAll('[role="menuitem"]'));
                const downloadItem = menuItems.find(item => {
                  const label = item.getAttribute('aria-label') || item.textContent || '';
                  return label.toLowerCase().includes('download') && 
                         !label.toLowerCase().includes('remove') &&
                         !label.toLowerCase().includes('delete');
                });
                
                if (downloadItem) {
                  (downloadItem as HTMLElement).click();
                  return true;
                }
                return false;
              });
              
              if (downloadFound) {
                console.log(`   ✅ Download initiated`);
                downloadedCount++;
                await page.waitForTimeout(2000); // Wait for download to start
              } else {
                console.log(`   ⚠️  No Download option found`);
                // Click outside to close menu
                await page.click('body', { clickCount: 1, delay: 100 });
              }
            }
          } catch (error: any) {
            console.error(`   ❌ Error: ${error.message}`);
            // Try to close any open menus
            try {
              await page.keyboard.press('Escape');
            } catch {}
          }
          
          // Small delay between files
          await page.waitForTimeout(500);
        }

        console.log(`\n✨ Completed! Downloaded ${downloadedCount} files.`);
        break;
      } else {
        attempt++;
        if (attempt < maxAttempts) {
          console.log(`   ⏳ No More buttons found, retrying... (attempt ${attempt + 1}/${maxAttempts})`);
          await page.waitForTimeout(2000);
        } else {
          console.log(`\n⚠️  Could not find More buttons. Make sure you're on the Studio tab.`);
        }
      }
    }

    // Wait for downloads to complete
    console.log('\n⏳ Waiting for downloads to complete...');
    await page.waitForTimeout(5000);

  } catch (error: any) {
    console.error('\n❌ Error during automation:', error.message);
    console.error(error.stack);
  } finally {
    console.log('\n🔒 Keeping browser open for 5 seconds, then closing...');
    await page.waitForTimeout(5000);
    await browser.close();
    console.log('✅ Done!\n');
  }
}

// Main execution
const notebookUrl = process.argv[2];
if (!notebookUrl) {
  console.error('❌ Usage: tsx scripts/download-notebooklm-files.ts <notebook-url>');
  console.error('📝 Example: tsx scripts/download-notebooklm-files.ts "https://notebooklm.google.com/notebook/..."\n');
  process.exit(1);
}

downloadNotebookLMFiles(notebookUrl).catch(console.error);

