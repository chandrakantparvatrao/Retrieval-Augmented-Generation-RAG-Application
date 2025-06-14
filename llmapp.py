from groq import Groq

import streamlit as st
topic_name = st.text_input('Enter Topic Name:')
st.button("Submit")
# st.write('Hi, How are you?' + topic_name)

client = Groq(
    api_key='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',
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Recommend me 3 best Python books related to {}. Give me book name and author name only.".format(topic_name),
        }
    ],
    model="llama-3.3-70b-versatile"
)

st.write(chat_completion.choices[0].message.content)