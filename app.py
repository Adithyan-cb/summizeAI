######################## IMPORTING NECESSARY LIBRARIES #############

import os
from groq import Groq
import streamlit as st

# groq api 
client = Groq(
    api_key=st.secrets["API_KEY"]
)



################## SUMMARIZATION FUNCION #################

def text_summarize(text,modes):
    normal = f"summarzie this text with the following characteristics: use bullet points,provide only the important points,short and concise,each points should be 2 or 3 sentences here is the text :{text}"
    conversational = f"Summarize this text conversationally and professionally, blending academic objectivity with a storyteller's touch and a hint of humor, ensuring it sounds like a natural human explanation: {text}"
    #concise = f"Create a precisely crafted 100-word summary in 3-4 sentences, distilling the most critical 20% of information while ensuring comprehensive understanding, with a fluid and natural language flow: {text}"
    student = f"Summarize this text as an experienced college professor, creating student-friendly bullet points that boldly highlight key terms, use simple language, include relatable examples, and provide comprehensive yet concise insights (approximately 100 words per point), demonstrating deep academic understanding while remaining accessible: {text}"
    
    presentation = f"Summarize this text as a concise, presentation-ready brief for a professional seminar. Highlight key points, potential discussion triggers, and critical insights that would engage an academic or industry audience. Structure the summary to support a clear 10-15 minute presentation flow: {text}"

    ####### RESPONSE MODE ##########
    if modes == "conversational":
        modes = conversational
    elif modes == "student":
        modes = student
    elif modes == "presentation":
        modes = presentation
    else:
        modes = normal

    try:
        summary = client.chat.completions.create(
            messages= [
                {
                    "role":"system",
                    "content":"you are a helpful assistant"
                },
                {
                    "role":"user",
                    "content":modes,
                }
            ],
            model="llama-3.1-8b-instant"
            
        )
        return summary.choices[0].message.content
    except Exception as e:
        return f"An error occured at {e}"

#################### STREAMLIT APP ###############

def main():
    if "text_area_content" not in st.session_state:
        st.session_state.text_area_content = ""

    text = """
    <h1 style="text-align:center">SUMMIZE AI 🕮</h1>
    """


    st.html(text)

    text_input = st.text_area(label="text",placeholder="enter a text",label_visibility="hidden",value=st.session_state.text_area_content,key="text_area_display")
    st.session_state.text_area_content = text_input
    option = st.selectbox(label="select the response mode:",options=("normal","conversational","student","presentaion"))
    send = st.button("**send**")

    if send:
        if not text_input.strip():
            st.write("The text area is empty")
        else:
            summary = text_summarize(text=text_input,modes=option)
            st.write(summary)

############## RUN APP #############

if __name__ == "__main__":
    main()