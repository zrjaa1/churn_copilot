# Deploying ChurnPilot to Streamlit Community Cloud

## Quick Setup (5 minutes)

### Step 1: Push to GitHub
Your code is already in a git repository. Make sure it's pushed to GitHub:

```bash
git push origin main
```

### Step 2: Sign up for Streamlit Community Cloud
1. Go to https://share.streamlit.io/
2. Click "Sign up" and use your GitHub account
3. It's completely FREE

### Step 3: Deploy the App
1. Click "New app" button
2. Select your repository: `JayCh/churn_copilot` (or whatever your GitHub username/repo is)
3. Set branch: `main`
4. Set main file path: `src/ui/app.py`
5. Click "Advanced settings"

### Step 4: Add Your API Key (IMPORTANT)
In "Advanced settings" → "Secrets":

```toml
ANTHROPIC_API_KEY = "your-actual-api-key-here"
```

Replace `your-actual-api-key-here` with your real Anthropic API key.

6. Click "Deploy!"

### Step 5: Wait 2-3 Minutes
Streamlit will install dependencies and launch your app.

Your app URL will be: `https://[your-app-name].streamlit.app`

---

## Sharing with Users

Once deployed, you'll get a public URL like:
```
https://churnpilot.streamlit.app
```

Share this link with your test users. They can:
- Access instantly (no installation)
- Use on any device (phone, tablet, computer)
- Data stays in their browser (private)

---

## Updating the App

When you push new code to GitHub:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

Streamlit auto-deploys within 1-2 minutes! 🎉

---

## Troubleshooting

**App won't start?**
- Check that `requirements.txt` has all dependencies
- Verify API key is set correctly in Secrets

**Import errors?**
- Make sure main file path is: `src/ui/app.py`

**Need help?**
- Check Streamlit logs in the dashboard
- Streamlit Community: https://discuss.streamlit.io/
