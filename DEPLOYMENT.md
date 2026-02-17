# OCR App Production Deployment Guide

This guide covers deploying the Flask backend to Render.com and the static frontend to Firebase Hosting.

## Prerequisites

1.  **Google Cloud Project**: Enabled Vision API.
2.  **Service Account Key**: `credentials.json` file.
3.  **GitHub Account**: For source code hosting.
4.  **Render Account**: For backend hosting.
5.  **Firebase Project**: For frontend hosting.

---

## Part 1: Backend Deployment (Render)

### 1. Push to GitHub

Ensure your latest code is pushed to a GitHub repository.

```bash
git add .
git commit -m "Prepare for production deployment"
git push origin main
```

### 2. Create Web Service on Render

1.  Log in to [dashboard.render.com](https://dashboard.render.com/).
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub repository.
4.  Configure the service:
    *   **Name**: `ocr-demo` (or similar)
    *   **Region**: Choose closest to you (e.g., Singapore, Frankfurt, Oregon)
    *   **Branch**: `main`
    *   **Runtime**: `Docker` (important!)
    *   **Plan**: Free

### 3. Environment Variables

Scroll down to the **Environment Variables** section and add the following:

| Key | Value |
| --- | --- |
| `GOOGLE_CREDENTIALS_JSON` | **[CRITICAL]** Paste the *entire content* of your `credentials.json` file here. |
| `PORT` | `8080` (Optional, Render sets this automatically) |

> **Note:** Open your `credentials.json` locally, copy all text, and paste it as the value for `GOOGLE_CREDENTIALS_JSON`. Do NOT upload the file itself.

### 4. Deploy

Click **Create Web Service**. Render will start building your Docker image. This may take a few minutes as it installs dependencies.

Once successful, copy your **Service URL** (e.g., `https://ocr-demo-xyz.onrender.com`).

---

## Part 2: Frontend Deployment (Firebase)

### 1. Update Backend URL

Open `public/index.html` locally and update the configuration:

```javascript
// Configuration
const PRODUCTION_BACKEND_URL = 'https://ocr-demo-xyz.onrender.com'; // REPLACE THIS WITH YOUR RENDER URL
```

### 2. Deploy to Firebase

Run the following commands in your terminal:

```bash
# Login to Firebase (if not already logged in)
firebase login

# Initialize project (if not done) - usually select 'Hosting'
# firebase init hosting

# Deploy to production
firebase deploy --only hosting
```

The CLI will output your Hosting URL (e.g., `https://ocr-doc-59a5e.web.app`).

---

## Part 3: Validation

1.  Open your Firebase Hosting URL on a mobile phone or another computer.
2.  Upload an image.
3.  Check if the extraction works.
4.  Verify the timer shows up during processing.

## Troubleshooting

*   **Server Error (500)**: Check Render logs. If it says "Google Cloud credentials not found", verify the `GOOGLE_CREDENTIALS_JSON` variable.
*   **Network Error / CORS**: Ensure your backend handles CORS correctly (currently set to allow all origins).
*   **Tesseract Error**: Confirm the Docker build installed `tesseract-ocr`.
