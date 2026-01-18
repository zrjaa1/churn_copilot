# 🚀 Deploy ChurnPilot in 5 Minutes

## What You'll Need
- ✅ GitHub account (you have this)
- ✅ Your Anthropic API key
- ⏱️ 5 minutes

---

## Step-by-Step Deployment

### 1️⃣ Push Code to GitHub (if not already done)

```bash
cd C:\Users\JayCh\workspace\churn_copilot
git push origin main
```

If you don't have a GitHub remote yet:
```bash
# Create a new repo on GitHub first (github.com/new), then:
git remote add origin https://github.com/YOUR_USERNAME/churn_copilot.git
git push -u origin main
```

---

### 2️⃣ Go to Streamlit Cloud

Open in browser: **https://share.streamlit.io/**

Click **"Sign up"** or **"Sign in"** with your GitHub account.

---

### 3️⃣ Deploy New App

1. Click big blue **"New app"** button

2. Fill in the form:
   - **Repository:** Select `churn_copilot` (or whatever you named it)
   - **Branch:** `main`
   - **Main file path:** `src/ui/app.py` ⚠️ IMPORTANT - include the `src/ui/` prefix!

3. Click **"Advanced settings..."** at the bottom

4. In the **Secrets** box, paste this (replace with your actual API key):

```toml
ANTHROPIC_API_KEY = "sk-ant-api03-YOUR-ACTUAL-KEY-HERE"
```

⚠️ **CRITICAL:** Use your REAL Anthropic API key from https://console.anthropic.com/settings/keys

5. Click **"Deploy!"**

---

### 4️⃣ Wait 2-3 Minutes ⏳

Streamlit will:
- Install Python dependencies
- Start your app
- Give you a public URL

You'll see build logs in real-time.

---

### 5️⃣ Get Your Public URL 🎉

Once deployed, you'll get a URL like:
```
https://churnpilot-YOUR-USERNAME.streamlit.app
```

Or:
```
https://YOUR-USERNAME-churnpilot-srcuiapp-HASH.streamlit.app
```

**That's your app!** Share this URL with test users.

---

## Testing Your Deployed App

1. Open the URL in a browser
2. Try adding a card from the library
3. Try importing from spreadsheet
4. Check that all features work

---

## Troubleshooting

### ❌ "ModuleNotFoundError"
- Check that main file path is exactly: `src/ui/app.py`
- Make sure you pushed all files to GitHub

### ❌ "ANTHROPIC_API_KEY not found"
- Go to app dashboard → "⋮" menu → "Settings" → "Secrets"
- Paste your API key again

### ❌ App is slow
- First load takes 30-60 seconds (normal)
- Subsequent loads are faster
- Consider upgrading Streamlit plan for more resources

### ❌ Changes not showing
- Push changes to GitHub: `git push`
- Streamlit auto-deploys in 1-2 minutes
- Or manually restart: Dashboard → "⋮" → "Reboot app"

---

## Updating the App Later

Just push to GitHub:
```bash
git add .
git commit -m "Add new feature"
git push origin main
```

Streamlit auto-updates your app! 🎊

---

## Inviting Test Users

Share the public URL with anyone:
- No installation required
- Works on phone, tablet, computer
- Each user's data stays private (in their browser)
- Free for all users

Example message to send:
```
Hey! I built a credit card churning tool.

Try it here: https://churnpilot-YOUR-USERNAME.streamlit.app

Features:
- Track SUB deadlines
- 5/24 calculator
- Benefit reminders
- Import from spreadsheet

Let me know what you think!
```

---

## Need Help?

1. Check Streamlit logs: Dashboard → "Manage app" → "Logs"
2. Streamlit Community: https://discuss.streamlit.io/
3. Or ask me - I'm here to help!

---

**Ready? Let's deploy! 🚀**
