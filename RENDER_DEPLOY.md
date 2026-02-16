# Deploy to Render.com (FREE, No Billing!)

Since Google Cloud is having issues, we'll deploy to Render.com which:
- ✅ Is completely FREE
- ✅ Doesn't require billing/credit card
- ✅ Works with Tesseract OCR
- ✅ Gives you a public URL instantly

## Option 1: Deploy from GitHub (Recommended)

### Step 1: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `ocr-demo`
3. Make it **Public**
4. Click "Create repository"

### Step 2: Push Your Code
Open PowerShell in the `ocr_web_app` folder and run:

```powershell
cd "c:\Users\tanay\Downloads\ocr docs\ocr_web_app"

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial OCR app"

# Add your GitHub repo (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/ocr-demo.git

# Push
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Render
1. Go to https://render.com and sign up (use GitHub login)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Settings:
   - **Name**: `ocr-demo`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`
5. Click **"Advanced"** and add these:
   - Click **"Add Environment Variable"**
   - Key: `PORT`, Value: `8000`
6. Click **"Create Web Service"**

Render will:
- Install Tesseract automatically (from Dockerfile)
- Install Python dependencies
- Deploy your app
- Give you a URL like `https://ocr-demo.onrender.com`

---

## Option 2: Deploy Without GitHub

If you don't want to use GitHub:

### Using Render Blueprint (Simpler)
1. Create a `render.yaml` file (already included if you see it)
2. Zip your `ocr_web_app` folder
3. Go to Render Dashboard → "Blueprints"
4. Upload the ZIP file
5. Deploy!

---

## What Changed?
- ❌ Removed Google Vision API (requires billing)
- ✅ Using Tesseract OCR only (100% free)
- ✅ Same dark UI, PDF support, everything works!

## Testing Local Version
Before deploying, test it locally:

```powershell
cd "c:\Users\tanay\Downloads\ocr docs\ocr_web_app"
python app.py
```

Go to http://localhost:5000 and upload a test image!

---

## Need Help?
- Render.com has amazing docs: https://render.com/docs
- Your app will be live in ~5 minutes after deployment
- Free tier stays active forever (no time limit)

## After Deployment
You'll get a URL like: `https://ocr-demo-abc123.onrender.com`

Use this URL for your internship demo! 🚀
