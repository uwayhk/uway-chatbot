# UWAY Chatbot - Hugging Face Spaces (Frontend)

## Setup
1. Create a new Space on Hugging Face (Dashboard → New Space)
2. Select "Streamlit" as SDK
3. Upload these files
4. In Settings → Repository secrets, add:
   - `AWS_API_URL` = `https://<your-ec2-public-ip>/api/chat`

## Run Locally (for testing)
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py --server.port 8501
```

## Embed into Website
```html
<iframe 
    src="https://your-username-your-space.hf.space"
    width="100%" 
    height="600px"
    style="border: none; border-radius: 8px;"
></iframe>