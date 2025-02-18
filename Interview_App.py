import streamlit as st
from openai import OpenAI
import requests
import validators
import json

import fun_llm


st.title("Interview Practice App")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    # st.session_state["openai_model"] = "gpt-4o"
    st.session_state["openai_model"] = "gpt-4-turbo"



# Set chatbot max number of questions
# input_max_questions_disabled = False
# max_questions = st.number_input("Chose how many question you'll want to ask: ", key="input_max_questions", min_value=1, max_value=10, value=5, step=1, disabled=input_max_questions_disabled)
# if "chatbot_max_questions" not in st.session_state:
#     st.session_state["chatbot_max_questions"] = max_questions
#     st.session_state.input_max_questions_disabled = True


# Set job_ad_text, which stores web page text of job ad page
# if "job_ad_text" not in st.session_state:
#     st.session_state["job_ad_text"] = ""

# Set chatbot availability. Will be dissabled after n questions
if "chat_input_dissabled" not in st.session_state:
    st.session_state["chat_input_dissabled"] = False

# Set chatbot field's message
if "chat_input_message" not in st.session_state:
    st.session_state["chat_placeholder_message"] = "Ask your question !"

# Set chatbot availability. Will be dissabled after n questions
if "chat_input_counter" not in st.session_state:
    st.session_state["chat_input_counter"] = 1
elif st.session_state["chat_input_counter"] >= 10:
    # Dissable chant input & change field's message
    st.session_state["chat_input_dissabled"] = True
    st.session_state["chat_placeholder_message"] = "Thank you for you time, interview finished"


# App parameters widgets
st.sidebar.title("App Parameters & Status Info")
openai_temperature = st.sidebar.slider("Select questions creativity. Higher values - more random", min_value = 0.5, max_value = 0.9, value = 0.7, step = 0.05)

# App status information. Like chat messages counter
st.sidebar.title("App Status Info")
st.sidebar.write(f"**:red[Chat messages counter: {st.session_state["chat_input_counter"]} / 10]**")




# Read user input of job ad URL
# https://www.cvbankas.lt/ai-developer-vilniuje/1-12713409              for testing
url_job_ad = st.text_input("Enter web URL for job ad (only from www.cvonline.lt). For example: https://www.cvbankas.lt/ai-developer-vilniuje/1-12713409",   value="https://www.cvbankas.lt/ai-developer-vilniuje/1-12713409")
if validators.url(url_job_ad):
    #  Store job ad text
    response_job_ad = requests.get(url_job_ad)
    st.sidebar.write("HTTP response status code: ", response_job_ad.status_code)
    if response_job_ad.status_code == 200:
        st.markdown(":green[**Job ad retrieved sucessfully!**]")
        st.session_state["job_ad_text"] = response_job_ad.text
        x = False
    else:
        st.markdown(f":red[Failed to retrieve job ad page. Please check web address and try again. Status code: {response_job_ad.status_code}]")
else:
    st.markdown(f":red[Incorrect web adress. Review and try again.]")


# Startus tracking
# st.sidebar.write("job_ad_text: ", st.session_state["job_ad_text"])           # turi teksta
if "job_ad_segments" not in st.session_state:
    st.session_state["job_ad_segments"] = fun_llm.extract_job_ad_sections(st.session_state["job_ad_text"], OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"], openai_model=st.session_state["openai_model"] )
# Startus tracking
# st.sidebar.write("job_ad_segment", st.session_state["job_ad_segments"])


if "job_ad_segments" in st.session_state:
    with st.sidebar:
        st.sidebar.title("Job ad Segments")
        st.write("**Job Description:**")
        st.write(st.session_state["job_ad_segments"]["Job description"])
        st.write("**Technical Skills:**")
        st.write(st.session_state["job_ad_segments"]["Technical skills"])
        st.write("**Soft Skills:**")
        st.write(st.session_state["job_ad_segments"]["Soft skills"])


st.divider()

system_prompt = f"""
You are HR (human resources specialist). Your personal characteristics are:
* You are helpful and polite person.
* Your responces are brief, but informative
* When responding always stick to the topic of JOB INTERVIEW
* When responfing to user question, you can ask folow up question yourself.
* You are not alowed to use any personal insults. If user provokes you, you should politely respond and come bact to the main topic: job interview.
* IMPORTANT - You have total 10 messages for conversation. On 9th message thank for conversation and wish a good day!

Job ad description is following:

{json.dumps(st.session_state["job_ad_segments"])}

"""



# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

    # Add system message for job add context
    st.session_state.messages.append({"role": "system", "content": system_prompt})





# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input(st.session_state["chat_placeholder_message"], disabled=st.session_state["chat_input_dissabled"], key="key_chat_input",):

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
            temperature = openai_temperature
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state["chat_input_counter"] += 1

# Track messages
st.sidebar.title("Messages tracker")
st.sidebar.write("All messages: ", st.session_state["messages"])
    
