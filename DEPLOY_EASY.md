# Alternative: Deploy via Google Cloud Console (No CLI needed!)

## Quick Web-Based Deployment

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/run
   - Select project: `gen-lang-client-0998176697`

2. **Create New Service**
   - Click "CREATE SERVICE"
   - Choose "Continuously deploy from a repository"
   - Connect to GitHub (if your code is there) OR use "Source Repository"

3. **Manual Upload Option**
   - Zip your entire `ocr_web_app` folder
   - Use Cloud Shell in the console
   - Upload zip and run:
     ```bash
     unzip ocr_web_app.zip
     cd ocr_web_app
     gcloud run deploy ocr-web-app --source . --platform managed --region us-central1 --allow-unauthenticated
     ```

4. **Settings to Configure**
   - Memory: 2 GiB
   - CPU: 1
   - Timeout: 300 seconds
   - Allow unauthenticated invocations: YES

5. **Get Your URL**
   - After deployment completes (~5 mins)
   - Copy the service URL
   - Test it!

## Even Simpler: Use Render.com (Alternative to Google Cloud)

1. Go to: https://render.com
2. Sign up (free)
3. Click "New +" → "Web Service"
4. Connect to GitHub OR upload via Git
5. Settings:
   - Environment: Docker
   - Plan: Free
6. Deploy!

Your internship demo is ready! 🎉
