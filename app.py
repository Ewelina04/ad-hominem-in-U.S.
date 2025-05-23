
#  python -m streamlit run C:\Users\User\Downloads\Elections_2024\ECA_APP.py

import streamlit as st
from autogen import ConversableAgent
import requests
import pandas as pd
import numpy as np
import time
import re
#from sklearn import metrics
#from transformers import pipeline
from autogen import LLMConfig


def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Enter a text message for the analysis. "}]

def add_spacelines(number_sp=2):
    for xx in range(number_sp):
        st.write("\n")




# App title
st.set_page_config(page_title="💬 Chatbot")
st.title('Countering Ad Hominem Fallacies with LLM-Chatbot')
#Countering Fallacies with LLMs: A System for Recognising and Rebutting Ad Hominem Arguments
st.write("\n\n")


# Replicate Credentials
with st.sidebar:
    add_spacelines(2)
    st.write('This chatbot is created using the Gemini-2.0-Flash LLM model from Google.')
    add_spacelines(2)

    replicate_api = st.text_input('Enter Gemini API token:', type='password')
    if len(replicate_api) < 20:
        st.warning('Please enter the correct credentials!', icon='⚠️')
        st.stop()
    else:
        st.success('Proceed to entering your message!', icon='👉')


    add_spacelines(2)
    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a model', ['Gemini-2.0-Flash', ], key='selected_model')
    add_spacelines(1)

    temp = st.sidebar.slider('temperature', min_value=0.01, max_value=1.0, value=0.1, step=0.05)
    max_length = st.sidebar.slider('max_length', min_value=200, max_value=500, value=250, step=50)

    add_spacelines(2)
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


llm_config = LLMConfig(
    config_list=[
        {
            "api_type": "google",
            "model": "gemini-2.0-flash",
           "api_key": str(replicate_api) 
        }
    ],temperature=0.2, max_tokens = max_length,
)

with llm_config:
  # Create an AI agent
  critic = ConversableAgent(
      name="critic",
      system_message="You are a judge critic who assesses argument quality using three critical questions: 1. Does the rebuttal adequately address the specific criticisms raised in the ad hominem attack? 2. Does the generated counterargument restore confidence in targets's credibility? 3. Does the target have the necessary credibility to conduct the proposed actions, if the actions are mentioned?",
  )

  # Create another AI agent
  advocate = ConversableAgent(
      name="advocate",
      system_message="You are the target of ad hominem who produces counterarguments and listens to the critic to improve your arguments.",
  )

#st.stop()
# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "**Assistant**: Enter a text message for the analysis. "}]

# Display or clear chat messages
#for message in st.session_state.messages:
#    with st.chat_message(message["role"]):
#        st.write(message["content"])

add_spacelines(2)

with st.chat_message( "human" ):
    text = st.chat_input("Arabia? And with all of the money they have, we're defending them, and they're not paying? All you have to do is speak to them. Wait. You have so many different things you have to be able to do, and I don't believe that Hillary has the stamina.")
    st.write(text)


# Start the conversation
history_chat = critic.initiate_chat(
    recipient=advocate,
    message=f"Identify whether the text includes ad hominem: {text}. If yes, respond to the ad hominem argument, defending the target's credibility. Write just the rebuttal. Rewrite the rebuttal if adviced by the critic ",
    max_turns=2,
    summary_method="reflection_with_llm",
)


add_spacelines(2)


for i in range(len(history_chat.chat_history[1:])):
    message_text = ""
    output_chat_1 = history_chat.chat_history[i+1]['content']
    if (i+1) % 2 == 0:
        message_text += '**Critic:** '
    else:
        message_text += '**Advocate:** '

    message_text += output_chat_1
    message_text += '\n'
    message_text += ' ************************************************** '
    message_text += '\n'

    with st.chat_message( "assistant" ):
        st.write(message_text)
