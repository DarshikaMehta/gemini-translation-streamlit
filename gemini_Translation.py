import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from PyPDF2 import PdfReader
import pandas as pd
import os
import tempfile
text_input=""
#step 2: Configure the Gemini API
import getpass
 
#Load API key securely: prefer Streamlit secrets or environment variable
api_key = os.environ.get("GENAI_API_KEY") #or st.secrets.get("GENAI_API_KEY") if hasattr(st, "secrets") else None
if not api_key:
     #entered = st.text_input("Gemini API key (or set GENAI_API_KEY env var / Streamlit secrets)", type="password")
    try:
        api_key=st.secrets["GENAI_API_KEY"]
        #if entered:
        # api_key = entered
    except Exception:
         api_key = None


if not api_key:
     st.warning("No Gemini API key found. Set GENAI_API_KEY env var or add it to Streamlit secrets, or enter it above to continue.")
     st.stop()         

genai.configure(api_key=api_key)

#step 3 : Configure LLM model 
model=genai.GenerativeModel("gemini-2.5-flash")

#Function : Translate text using gemini
def translate_text_gemini(text, target_language):
    try:
        prompt = f"Translate following text into {target_language}, provide only the traslated text \n\n :{text}"
        response =  model.generate_content(prompt)
        return response.text.strip() 
    except Exception as err:
            return f"Error occurred: {err}"
    
#Function to convert Text to Speech 
def text_to_Speech(text, language_code):
    try:
        tts = gTTS(text=text, lang=language_code)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        return temp_file.name   
    except Exception as err:
            return f"Error occured:{err}"
        
def extracted_text_from_file(uploaded_file) -> str:
     file_name=uploaded_file.name.lower()
     if file_name.endswith(".pdf"):
        try:
              reader = PdfReader(uploaded_file)
              text_chunks = []
              for page in reader.pages:
                  page_text  = page.extract_text or "" 
                  text_chunks.append(page.extract_text()) 
                  return "\n".join(text_chunks).strip()
        except Exception as err:
             st.error(f"Error reading pdf:{err}")
             return ""
     elif file_name.endswith(".xlsx") or file_name.endswith(".xls"):
        try:
            df = pd.read_excel(uploaded_file)
            # Convert all cells to string, then join
            return df.astype(str).to_string(index=False)
        except Exception as err:
            st.error(f"Error reading Excel file: {err}")
            return ""

    # CSV
     elif file_name.endswith(".csv"):
        try:
            df = pd.read_csv(uploaded_file)
            return df.astype(str).to_string(index=False)
        except Exception as err:
            st.error(f"Error reading CSV file: {err}")
            return ""

     else:
        st.error("Unsupported file type. Please upload PDF, Excel, or CSV.")
        return ""   




     
    # STREAMLIT Application 
def main():
    with st.sidebar:
        st.header("ℹ️ About this App")
        st.write("""
        This multilingual translation assistant is powered by **Google Gemini**  
        and built using **Streamlit**.

        **Capabilities:**
        - Translate text into multiple languages  
        - Upload PDF, Excel, or CSV documents for translation  
        - Convert translated text to speech (MP3 audio)  
        - Preview extracted text from files  

        **Tech Stack:**  
        Streamlit · Google Gemini · Python · gTTS · PyPDF2 · pandas  

        **Live App URL:**  
        https://gemini-translation-app-ammxgoduaapppl5hmsjvej9.streamlit.app
        """)

    st.write("---")
    st.write("Developed as part of GenAI learning project.") 

    #st.title('Multi-Language Application by using GEMINI(API)')
    st.title("🌍 Multi-Language Translator using Google Gemini")

    st.markdown("""
        This AI-powered web application translates text or uploaded documents  
        into multiple languages and generates natural MP3 speech output.
    """)

    #Laungage Selection 
    languages = {
             "English":"en",
             "French":"fr",
             "German":"de",
             "Spanish":"es",
             "Italian":"it",
             "Japanese":"ja",
             "Chinese":"zh-cn",
             "Russian":"ru",
             "Hindi":"hi",
             "Gujarati":"gu",
             "Telugu":"te"             
        }
    selected_language =st.selectbox("Select the Language",list(languages.keys()))

    #Choose input mode
    input_mode = st.radio("choose Input mode",["Text","File"])
    if input_mode=="Text":
        text_input= st.text_area('Enter the Text here:')

    else: # File Mode
        uploaded_file = st.file_uploader("upload a file (PDF, Excel or CSV)",type=['pdf','xlsx','csv'],)
        if uploaded_file is not None:
            st.info(f"uploaded File:{uploaded_file.name}")
            text_input = extracted_text_from_file(uploaded_file) ## repalced source_text with text_input
            #text_input = source_text   
            if text_input: ##source_text:
                with st.expander("Preview extracted text"):
                        st.write(text_input[:3000] + ("\n...\n(trucated)" if len(text_input)>3000 else "")) ## again repalced source_text with text_input


    if st.button('Translate and Convert'):
                if text_input.strip() == "":
                    st.error('Please provide the text to translate')
                else:
                    with st.spinner("Translating text and generating audio..."):    
                        translate_text = translate_text_gemini(text_input, selected_language)
                        st.subheader('Translated text')
                        st.write(translate_text) 

                        #Convert text to speech 
                        audio_file = text_to_Speech(translate_text, languages[selected_language])
                        if audio_file and os.path.exists(audio_file): 
                            #st.audio(audio_file, format ="audio/mp3")
                            with open(audio_file,'rb') as f:
                                audio_bytes = f.read()
                            # use bytes instead of File_path
                            st.audio(audio_bytes, format ="audio/mpeg")
                            st.download_button('Download audio',data=audio_bytes,file_name='translated_audio.mp3',mime="audio/mpeg")
                        else:
                            st.error('Failed to generate Audio')              

if __name__ == "__main__":
     main()

















             


