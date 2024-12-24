import os
from groq import Groq
import streamlit as st
from PyPDF2 import PdfReader
import base64

st.set_page_config(
    page_title="PDF summize",
    page_icon="📋",
)

# client
client = Groq(
    api_key=st.secrets["API_KEY"]
)

############## TEXT SUMMARISATION #################
def text_summarize(text):
    try:
        summary = client.chat.completions.create(
            messages= [
                {
                    "role":"system",
                    "content":"you are a helpful assistant"
                },
                {
                    "role":"user",
                    "content":f"Provide a concise, clear, and accurate summary of the text. Focus on key ideas, critical details, and main points, while omitting unnecessary information. Maintain a neutral tone, and ensure the summary is proportionate to the text length. here is the text : {text}",
                }
            ],
            model="llama-3.1-8b-instant"
            
        )
        return summary.choices[0].message.content
    except Exception as e:
        return f"An error occured at {e}"


########### STREAMLIT APP ##############
def main():

    text = """
        <h1 style="text-align:center">SUMMIZE AI 🕮</h1>
        """


    st.html(text)

    uploaded_file = st.file_uploader("choose a PDF",type="PDF")

    if uploaded_file is not None:

        st.success("file uploaded succesfully...")

        #pdf_bytes = uploaded_file.read()

        reader = PdfReader(uploaded_file)
        text = ""

        for pages in reader.pages:
            text += pages.extract_text()
        
        summary = text_summarize(text=text)
        st.write(summary)

        
        #base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        #pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="700s" type="application/pdf"></iframe>'
        
        # Display PDF in an iframe
        #st.markdown(pdf_display, unsafe_allow_html=True)

if __name__ == "__main__":
    main()