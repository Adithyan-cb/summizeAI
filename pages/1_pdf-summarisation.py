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
                    "content":f"""act as an expert in the AI field with decades of experience , your task is to look at the text I'm providing and identify the core topics discussed and explain them in very detail to me using simple language , 
                                you should also include examples if necessary to help the reader understand the concepts easily.the entire explanation should be understood by a person who is between beginner and intermediate in AI ,
                                    write the entire response in markdown format. here is the text:{text}"""
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

    st.html(text)

    uploaded_file = st.file_uploader("choose a PDF",type="PDF")

    if uploaded_file is not None:

        st.success("file uploaded succesfully...")


        reader = PdfReader(uploaded_file)
        pdf_text = ""

        for pages in reader.pages:
            text += pages.extract_text()
        
        summary = text_summarize(text=text)
        st.write(summary)

if __name__ == "__main__":
    main()