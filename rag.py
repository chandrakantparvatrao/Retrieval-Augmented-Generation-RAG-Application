from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from groq import Groq
import streamlit as st


reader = PdfReader("../datasets/budget_speech.pdf")
number_of_pages = len(reader.pages)

book = ''
for page in reader.pages:
    text = page.extract_text()
    book = book + text

    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)
texts = text_splitter.create_documents([book])

chunks = [d.page_content for d in texts]

client = chromadb.Client()
collection = client.get_collection(name = 'collection1')

ids = [str(i) for i in range (len(chunks))]
collection.add(documents = chunks, ids = ids)

query = st.text_input('Please enter your query')
st.button("Submit")
results = collection.query(query_texts=[query],n_results=3)
context = ' '.join(results['documents'][0])

# print(context)
prompt = '''Act as an AI assistant for question answering system.
All information with respect to question will be provided and question will also be provided.
You find out the exact answer of question in provided information and give answer in proper language.
If you don't get the answer from provided information , just say "No information found in given Context".
Information : {}
Question: {}'''.format(context, query)

client = Groq(
    api_key='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',
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="llama-3.3-70b-versatile",
)
answer = chat_completion.choices[0].message.content

st.write(answer)