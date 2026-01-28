# Git Setup and Push Instructions

## Step 1: Restart PowerShell
1. Close this PowerShell window completely
2. Open a NEW PowerShell window
3. Navigate to your project: `cd C:\Users\kaunt\BeatZGPT`

## Step 2: Verify Git Installation
```powershell
git --version
```
You should see: `git version 2.x.x`

## Step 3: Configure Git (One-time setup)
```powershell
git config --global user.name "KaunteyAcharya"
git config --global user.email "your.email@example.com"
```
**Replace** `your.email@example.com` with your actual GitHub email.

## Step 4: Initialize Repository
```powershell
git init
```

## Step 5: Add All Files
```powershell
git add .
```

## Step 6: Create First Commit
```powershell
git commit -m "Initial commit: AI text humanizer with GitHub Pages demo"
```

## Step 7: Connect to GitHub
```powershell
git remote add origin https://github.com/KaunteyAcharya/BZGPT.git
```

## Step 8: Set Main Branch
```powershell
git branch -M main
```

## Step 9: Push to GitHub
```powershell
git push -u origin main
```

**Note**: You may be prompted to authenticate with GitHub. Use your GitHub username and a Personal Access Token (not password).

---

## If You Need a Personal Access Token:
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (full control)
4. Click "Generate token"
5. Copy the token and use it as your password when pushing

---

## Step 10: Enable GitHub Pages
1. Go to: https://github.com/KaunteyAcharya/BZGPT/settings/pages
2. Under "Source":
   - Branch: `main`
   - Folder: `/ (root)`
3. Click "Save"
4. Wait 1-2 minutes

**Your live demo will be at:**
```
https://kaunteyacharya.github.io/BZGPT/
```

---

## Troubleshooting

### If git is still not recognized:
1. Check if Git is installed: `C:\Program Files\Git\bin\git.exe`
2. Add to PATH manually:
   - Search "Environment Variables" in Windows
   - Edit "Path" variable
   - Add: `C:\Program Files\Git\bin`
   - Restart PowerShell

### If push fails with authentication error:
- Use Personal Access Token instead of password
- Or use GitHub Desktop as alternative

---

## Alternative: GitHub Desktop (Easier)
1. Download: https://desktop.github.com/
2. Install and sign in
3. File → Add Local Repository → Select `C:\Users\kaunt\BeatZGPT`
4. Publish repository to GitHub
5. Enable GitHub Pages in repo settings

---

**Need help?** Let me know which step is giving you trouble!
