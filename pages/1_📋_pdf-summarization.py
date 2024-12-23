import os
from groq import Groq
import streamlit as st
from io import StringIO
import base64

st.set_page_config(
    page_title="PDF summize",
    page_icon="📋",
)

text = """
    <h1 style="text-align:center">SUMMIZE AI 🕮</h1>
    """


st.html(text)

uploaded_file = st.file_uploader("choose a PDF",type="PDF")

if uploaded_file is not None:

    pdf_bytes = uploaded_file.read()

    base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    
    # Display PDF in an iframe
    st.markdown(pdf_display, unsafe_allow_html=True)