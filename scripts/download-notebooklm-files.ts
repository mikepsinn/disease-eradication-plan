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

// Helper function to wait (replacement for deprecated waitForTimeout)
function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Dynamic import for puppeteer (in case it's not installed)
async function loadPuppeteer() {
  try {
    const puppeteer = await import('puppeteer');
    return puppeteer.default;
  } catch (error) {
    console.error('\n❌ Puppeteer is not installed!');
    console.error('Please install it first:');
    console.error('  pnpm add -D puppeteer -w\n');
    process.exit(1);
  }
}

async function downloadNotebookLMFiles(notebookUrl: string, useExistingBrowser: boolean = false) {
  const puppeteerModule = await loadPuppeteer();
  
  console.log(`\n🚀 Starting download automation for NotebookLM`);
  console.log(`📄 URL: ${notebookUrl}\n`);

  let browser;
  
  if (useExistingBrowser) {
    // Connect to existing browser (must be launched with remote debugging)
    // To use this, first launch Chrome with: chrome.exe --remote-debugging-port=9222
    console.log('🔗 Connecting to existing browser on port 9222...');
    try {
      browser = await puppeteerModule.connect({
        browserURL: 'http://127.0.0.1:9222',
        defaultViewport: null,
      });
      console.log('✅ Connected to existing browser\n');
    } catch (error) {
      console.error('❌ Could not connect to existing browser.');
      console.error('   Make sure Chrome is running with: chrome.exe --remote-debugging-port=9222');
      console.error('   Or close Chrome and let the script launch it with your profile.\n');
      process.exit(1);
    }
  } else {
    // Use a separate automation profile to avoid Windows authentication prompts
    // This will open a fresh Chrome instance - you'll need to log in once
    const automationProfileDir = path.join(process.cwd(), '.chrome-automation-profile');
    
    console.log('📁 Using separate automation profile (no Windows passkey needed)');
    console.log('⚠️  You will need to log in to NotebookLM in the browser window that opens\n');
    
    browser = await puppeteerModule.launch({
      headless: false,
      defaultViewport: { width: 1280, height: 720 }, // Use a specific size instead of maximized
      userDataDir: automationProfileDir,
      args: [
        '--disable-blink-features=AutomationControlled',
        '--window-size=1280,720', // Set window size to ensure tabs are visible
      ],
    });
  }

  try {
    const page = await browser.newPage();

    // Set up automatic download acceptance
    const downloadsDir = path.resolve(process.cwd(), 'downloads');
    if (!fs.existsSync(downloadsDir)) {
      fs.mkdirSync(downloadsDir, { recursive: true });
    }
    
    const client = await page.target().createCDPSession();
    await client.send('Page.setDownloadBehavior', {
      behavior: 'allow',
      downloadPath: downloadsDir,
    });
    
    // Track downloads with their intended filenames
    const downloadMap = new Map<string, string>();

    // Navigate to the notebook
    console.log('📍 Navigating to notebook...');
    console.log('⏳ Please log in to NotebookLM in the browser window that opens.');
    console.log('   The script will wait for you to log in and navigate to the notebook.\n');
    await page.goto(notebookUrl, { waitUntil: 'domcontentloaded', timeout: 120000 });
    
    // Wait for user to log in - check if we're on a login page
    console.log('⏸️  Waiting for you to log in...');
    console.log('   Press ENTER in this terminal when you are logged in and on the NotebookLM page.');
    console.log('   (Or wait 60 seconds and the script will continue automatically)\n');
    
    // Wait for either user input or timeout
    const readline = await import('readline');
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });
    
    const waitForLogin = new Promise<void>((resolve) => {
      // Auto-continue after 60 seconds
      setTimeout(() => {
        console.log('⏩ Auto-continuing after 60 seconds...\n');
        resolve();
      }, 60000);
      
      // Or wait for Enter key
      rl.question('', () => {
        console.log('✅ Continuing...\n');
        rl.close();
        resolve();
      });
    });
    
    await waitForLogin;
    await delay(2000);

    // Click on Studio tab
    console.log('🎯 Looking for Studio tab...');
    // Wait a bit and try multiple times in case page is still loading
    let studioTabClicked = false;
    for (let attempt = 0; attempt < 10; attempt++) {
      studioTabClicked = await page.evaluate(() => {
        // Try multiple ways to find the Studio tab
        // Method 1: Look for tabs by role
        const tabs = Array.from(document.querySelectorAll('[role="tab"]'));
        let studioTab = tabs.find(tab => {
          const text = tab.textContent?.trim().toLowerCase() || '';
          return text === 'studio';
        });
        
        // Method 2: Look for button with Studio text
        if (!studioTab) {
          const buttons = Array.from(document.querySelectorAll('button'));
          studioTab = buttons.find(btn => {
            const text = btn.textContent?.trim().toLowerCase() || '';
            const ariaLabel = btn.getAttribute('aria-label')?.toLowerCase() || '';
            return text === 'studio' || ariaLabel === 'studio';
          }) as any;
        }
        
        // Method 3: Look for any element containing "Studio"
        if (!studioTab) {
          const allElements = Array.from(document.querySelectorAll('*'));
          studioTab = allElements.find(el => {
            const text = el.textContent?.trim().toLowerCase() || '';
            return text === 'studio' && (el.tagName === 'BUTTON' || el.getAttribute('role') === 'tab');
          }) as any;
        }
        
        if (studioTab) {
          (studioTab as HTMLElement).click();
          return true;
        }
        return false;
      });
      
      if (studioTabClicked) {
        console.log('✅ Found and clicked Studio tab');
        break;
      }
      
      if (attempt < 9) {
        console.log(`   Attempt ${attempt + 1}/10: Studio tab not found yet, waiting...`);
        await delay(2000);
      }
    }

    if (!studioTabClicked) {
      console.error('\n❌ Could not find Studio tab automatically.');
      console.error('   Please manually click the Studio tab in the browser window.');
      console.error('   The script will wait 30 seconds for you to do this, then continue...\n');
      await delay(30000);
      
      // Try one more time after manual click
      studioTabClicked = await page.evaluate(() => {
        const tabs = Array.from(document.querySelectorAll('[role="tab"]'));
        const studioTab = tabs.find(tab => {
          const text = tab.textContent?.trim().toLowerCase() || '';
          return text === 'studio';
        });
        return !!studioTab;
      });
      
      if (!studioTabClicked) {
        console.error('⚠️  Still cannot detect Studio tab. Continuing anyway...\n');
      }
    }

    await delay(2000);

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

          // Skip any buttons that live inside the source list component.
          // The Angular component is <source-picker>, so any button with that
          // as an ancestor is part of the Sources panel, not the Studio items.
          const inSourcePicker =
            !!btn.closest('source-picker') ||
            !!btn.closest('[ng-reflect-ng-switch][class*="source"]');
          if (inSourcePicker) {
            return;
          }
          
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
            // Re-query buttons each time as DOM may change
            const currentButtons = await page.$$('button');
            const buttonIndex = moreButtons[i];
            
            if (buttonIndex < currentButtons.length) {
              // First, get the filename from the item before clicking
              const itemInfo = await page.evaluate((index) => {
                const buttons = Array.from(document.querySelectorAll('button'));
                const moreButton = buttons[index];
                if (!moreButton) return null;
                
                // Find the parent container that holds the file name
                let container = moreButton.closest('div[role="button"], div[class*="item"], div[class*="source"], li, [class*="card"]');
                if (!container) {
                  container = moreButton.parentElement?.parentElement?.parentElement;
                }
                
                // Try to find the file name/label
                let fileName = '';
                if (container) {
                  // Look for text content that seems like a file name
                  const textElements = container.querySelectorAll('span, div, p, button');
                  for (const el of Array.from(textElements)) {
                    const text = el.textContent?.trim() || '';
                    // Skip if it's too short, contains common UI text, or is the More button text
                    if (text.length > 5 && 
                        !text.toLowerCase().includes('more') &&
                        !text.toLowerCase().includes('ago') &&
                        !text.toLowerCase().includes('source') &&
                        !text.toLowerCase().includes('play') &&
                        !text.match(/^\d+\s*(source|ago|min|hour)/i) &&
                        text.length < 200) {
                      // This looks like a file name
                      fileName = text;
                      break;
                    }
                  }
                }
                
                // Fallback: try to get from button's aria-label or nearby text
                if (!fileName) {
                  const ariaLabel = moreButton.getAttribute('aria-label') || '';
                  if (ariaLabel && !ariaLabel.toLowerCase().includes('more')) {
                    fileName = ariaLabel;
                  }
                }
                
                return fileName;
              }, buttonIndex);
              
              const displayName = itemInfo || `File ${i + 1}`;
              console.log(`📥 Processing ${i + 1}/${moreButtons.length}: ${displayName.substring(0, 50)}...`);
              
              // Scroll button into view
              await currentButtons[buttonIndex].scrollIntoView();
              await delay(500);
              
              // Click More button
              await currentButtons[buttonIndex].click();
              await delay(1000);
              
              // Look for Download menu item and get download info
              const downloadInfo = await page.evaluate((itemName) => {
                const menuItems = Array.from(document.querySelectorAll('[role="menuitem"]'));
                const downloadItem = menuItems.find(item => {
                  const label = item.getAttribute('aria-label') || item.textContent || '';
                  return label.toLowerCase().includes('download') && 
                         !label.toLowerCase().includes('remove') &&
                         !label.toLowerCase().includes('delete');
                });
                
                if (downloadItem) {
                  // Get the download link or trigger
                  (downloadItem as HTMLElement).click();
                  return { found: true, name: itemName };
                }
                return { found: false, name: itemName };
              }, itemInfo || '');
              
              if (downloadInfo.found) {
                // Sanitize filename for filesystem
                const sanitizedName = (downloadInfo.name || `File_${i + 1}`)
                  .replace(/[<>:"/\\|?*]/g, '_')
                  .replace(/\s+/g, '_')
                  .substring(0, 200);
                
                // Wait for download to start, then rename it
                console.log(`   ✅ Download initiated`);
                downloadedCount++;
                
                // Monitor downloads directory for new files
                const filesBefore = new Set(fs.readdirSync(downloadsDir));
                await delay(3000); // Wait for download to start
                const filesAfter = new Set(fs.readdirSync(downloadsDir));
                const newFiles = Array.from(filesAfter).filter(f => !filesBefore.has(f));
                
                // Rename the downloaded file if we can identify it
                if (newFiles.length > 0) {
                  const downloadedFile = newFiles[0];
                  const filePath = path.join(downloadsDir, downloadedFile);
                  const ext = path.extname(downloadedFile);
                  const newPath = path.join(downloadsDir, `${sanitizedName}${ext}`);
                  
                  // Wait a bit more to ensure download is complete
                  await delay(2000);
                  
                  try {
                    if (fs.existsSync(filePath)) {
                      // Check if file is still being written (size changes)
                      let prevSize = 0;
                      for (let check = 0; check < 10; check++) {
                        const stats = fs.statSync(filePath);
                        if (stats.size === prevSize && stats.size > 0) {
                          break; // File size stable, download likely complete
                        }
                        prevSize = stats.size;
                        await delay(1000);
                      }
                      
                      fs.renameSync(filePath, newPath);
                      console.log(`   📝 Renamed to: ${sanitizedName}${ext}`);
                    }
                  } catch (renameError: any) {
                    console.log(`   ⚠️  Could not rename file: ${renameError.message}`);
                  }
                }
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
          await delay(500);
        }

        console.log(`\n✨ Completed! Downloaded ${downloadedCount} files.`);
        break;
      } else {
        attempt++;
        if (attempt < maxAttempts) {
          console.log(`   ⏳ No More buttons found, retrying... (attempt ${attempt + 1}/${maxAttempts})`);
          await delay(2000);
        } else {
          console.log(`\n⚠️  Could not find More buttons. Make sure you're on the Studio tab.`);
        }
      }
    }

    // Wait for downloads to complete
    console.log('\n⏳ Waiting for downloads to complete...');
    await delay(5000);

  } catch (error: any) {
    console.error('\n❌ Error during automation:', error.message);
    console.error(error.stack);
  } finally {
    console.log('\n🔒 Keeping browser open for 5 seconds, then closing...');
    await delay(5000);
    await browser.close();
    console.log('✅ Done!\n');
  }
}

// Main execution
const notebookUrl = process.argv[2];
if (!notebookUrl) {
  console.error('❌ Usage: tsx scripts/download-notebooklm-files.ts <notebook-url> [--use-existing]');
  console.error('📝 Example: tsx scripts/download-notebooklm-files.ts "https://notebooklm.google.com/notebook/..."');
  console.error('📝 With existing browser: tsx scripts/download-notebooklm-files.ts "..." --use-existing');
  console.error('\n💡 To use existing browser:');
  console.error('   1. Close all Chrome windows');
  console.error('   2. Launch Chrome with: chrome.exe --remote-debugging-port=9222');
  console.error('   3. Log in to NotebookLM');
  console.error('   4. Run script with --use-existing flag\n');
  process.exit(1);
}

const useExisting = process.argv.includes('--use-existing');
downloadNotebookLMFiles(notebookUrl, useExisting).catch(console.error);

