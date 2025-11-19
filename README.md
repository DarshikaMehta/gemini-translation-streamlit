# Gemini Multilingual Translation App (Streamlit)

This is a simple AI-powered web application that performs multilingual translation and text-to-speech using Google Gemini and Streamlit. The app is deployed on Streamlit Community Cloud and connected to a GitHub repository for version control and continuous deployment.

## Features

- Translate text into multiple languages using **Google Gemini (gemini-2.5-flash)**  
- Two input modes:
  - **Text mode** – type or paste input text
  - **File mode** – upload **PDF, Excel, or CSV**; the app extracts text automatically
- Generates audio for the translated text using **gTTS**
- Allows users to **play** the audio in the browser or **download** it as an MP3 file
- Securely loads the Gemini API key via **Streamlit Secrets** (`GENAI_API_KEY`)

## Tech Stack

- Python
- Streamlit
- Google Generative AI (`google-generativeai`)
- gTTS
- PyPDF2
- pandas

## Deployment

The app is deployed on **Streamlit Community Cloud**:

- Code is stored in a public GitHub repository
- Streamlit pulls the code from GitHub, installs dependencies from `requirements.txt`, and runs `gemini_Translation.py`
- The Gemini API key is configured in **Streamlit Secrets** as `GENAI_API_KEY`

## How to Run Locally

```bash
git clone https://github.com/<your-username>/gemini-translation-streamlit.git
cd gemini-translation-streamlit
pip install -r requirements.txt
set GENAI_API_KEY=your_api_key_here   # on Windows (or export on Mac/Linux)
streamlit run gemini_Translation.py
