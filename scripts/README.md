---
description: >-
  Automation scripts for repository management including AI-powered file
  organization and content migration
emoji: "\U0001F4C1"
title: Scripts Directory for Repository Management
tags: >-
  repository-management, automation, ai-powered, file-organization,
  content-migration
published: true
editor: markdown
date: '2025-02-12T20:29:36.760Z'
dateCreated: '2025-02-12T20:29:36.760Z'
---
# 📁 Scripts Directory

Repository management automation scripts with AI-powered file organization.

## Key Scripts

### [`reorganize.js`](reorganize.js)
- Creates standardized directory structure
- Generates foundational READMEs
- Enforces consistent taxonomy across docs

### [`migrate-content.js`](migrate-content.js) 
- AI-powered content migration engine
- Analyzes file locations using GPT-4
- Validates moves against directory structure
- Batch processes entire repository

### [`file-path-analyzer.js`](file-path-analyzer.js)
- AI classification module
- Returns JSON analysis with:
  - Target directory suggestions
  - Confidence scoring
  - Priority levels
  - Recommended actions (move/delete/flag)

### [`smart-repo-importer.js`](smart-repo-importer.js)
- Repository ingestion system
- Automatic directory tree generation
- AI-assisted file placement
- Legacy content integration

### [`process-images.js`](process-images.js)
- Automated image pipeline:
  1. S3 bucket synchronization
  2. Markdown URL rewriting
  3. Image catalog generation
  4. Local ↔ cloud validation

# Database Backup Script

This script creates a backup of a PostgreSQL database through an SSH tunnel. The backup is saved as a SQL dump file in the `backups` directory.

## Prerequisites

- Node.js installed
- `pg_dump` command-line tool installed
- SSH access to the remote server
- PostgreSQL database credentials

## Installation

1. Install the required dependencies:
```bash
npm install dotenv ssh2
```

2. Copy `.env.example` to `.env` and fill in your configuration:
```bash
cp .env.example .env
```

3. Update the `.env` file with your actual credentials and configuration.

## Usage

Run the backup script:
```bash
node scripts/db-backup.js
```

The script will:
1. Create an SSH tunnel to the remote server
2. Execute pg_dump through the tunnel
3. Save the backup file in the `backups` directory with a timestamp

## Backup File Format

Backups are saved in the following format:
```
backup-{database_name}-{timestamp}.sql
```

## Restoring a Backup

To restore a backup to another PostgreSQL instance:

```bash
psql -h {host} -U {username} -d {database} < backup-file.sql
```

## Environment Variables

- `DB_HOST`: Database host on the remote server
- `DB_PORT`: Database port (default: 5432)
- `DB_NAME`: Database name
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `SSH_HOST`: SSH server hostname
- `SSH_USER`: SSH username
- `SSH_PORT`: SSH port (default: 22)
- `SSH_PRIVATE_KEY_PATH`: Path to your SSH private key file
