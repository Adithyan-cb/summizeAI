from groq import Groq
import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(
    page_title="summize-ai-pdf-summarisation",
    page_icon="📋",
)

hide_st_style = """
    <style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
"""
st.markdown(hide_st_style,unsafe_allow_html=True)

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
        <h1 style="text-align:center">SUMMIZE AI </h1>
        """

    col1, col2, col3 = st.columns([5,6,1])

    with col1:
        st.write("")

    with col2:
        st.image("images/summize-logo.png",width=100)

    with col3:
        st.write("")



    st.html(text)

    uploaded_file = st.file_uploader("choose a PDF",type="PDF")

    if uploaded_file is not None:

        st.success("file uploaded succesfully...")


        reader = PdfReader(uploaded_file)
        text = ""

        for pages in reader.pages:
            text += pages.extract_text()
        
        summary = text_summarize(text=text)
        st.write(summary)

if __name__ == "__main__":
    main()