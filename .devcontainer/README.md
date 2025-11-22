# Dev Container Configuration

This directory contains the configuration for running this project in a containerized development environment.

## What is a Dev Container?

A Dev Container provides a consistent, pre-configured development environment that works identically across:
- **VSCode** (locally with Docker)
- **GitHub Codespaces** (cloud-based development)
- Any other IDE that supports dev containers

## What's Included

When you open this project in a dev container, you automatically get:
- Python 3.11
- Node.js 18
- Quarto CLI (latest version)
- All Python dependencies (from `requirements.txt`)
- All Node.js dependencies (from `package.json`)
- Recommended VSCode extensions

## How to Use

### In VSCode

1. Install [VSCode](https://code.visualstudio.com/) and [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Install the "Dev Containers" extension in VSCode
3. Open this project folder in VSCode
4. Click "Reopen in Container" when prompted (or use Command Palette → "Dev Containers: Reopen in Container")
5. Wait for the container to build (first time takes ~2-3 minutes)
6. Start coding! Everything is already installed.

### In GitHub Codespaces

1. Go to the repository on GitHub
2. Click "Code" → "Codespaces" → "Create codespace on main"
3. Wait for setup to complete
4. Edit directly in your browser

## Why Use This?

**Pros:**
- ✅ Zero setup - Python, Node, Quarto all pre-installed
- ✅ Identical environment for all contributors
- ✅ No "works on my machine" problems
- ✅ Easier onboarding for economists and non-technical contributors

**Cons:**
- ❌ Requires Docker Desktop (which requires admin access)
- ❌ First-time setup takes a few minutes
- ❌ Uses disk space for Docker images

## Troubleshooting

**Container won't start?**
- Make sure Docker Desktop is running
- Try "Dev Containers: Rebuild Container" from Command Palette

**Slow on Windows?**
- Make sure you're using WSL2 backend in Docker settings
- Clone repo inside WSL2 filesystem (not /mnt/c/)

**Still not working?**
- Use manual setup instead (see main README.md)
- Or use GitHub Codespaces (no local Docker required)
