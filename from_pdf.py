"""
Kod jest zaprojektowany do przetwarzania dokumentów PDF w celu tworzenia baz wiedzy dla chatbota.
Dokumenty są ładowane, dzielone na mniejsze fragmenty i przekształcane w wektory za pomocą mechanizmów embeddowania.
Następnie te wektory są przechowywane w bazie danych, która służy do wyszukiwania podobieństw
w oparciu o zapytania użytkownika. Głównym celem jest umożliwienie chatbotowi odpowiadania
na pytania użytkownika na podstawie informacji zawartych w wczytanych dokumentach PDF.
"""

import ipywidgets as widgets
from IPython.display import display
import textract
import os
import pandas as pd
import matplotlib.pyplot as plt
from transformers import GPT2TokenizerFast
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

os.environ["OPENAI_API_KEY"] = "{YOURAPIKEY}"

loader = PyPDFLoader("./attention_is_all_you_need.pdf")
pages = loader.load_and_split()

chunks = pages

doc = textract.process("./attention_is_all_you_need.pdf")

with open('attention_is_all_you_need.txt', 'w') as f:
    f.write(doc.decode('utf-8'))

with open('attention_is_all_you_need.txt', 'r') as f:
    text = f.read()

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")


def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=24,
    length_function=count_tokens,
)

chunks = text_splitter.create_documents([text])

token_counts = [count_tokens(chunk.page_content) for chunk in chunks]
df = pd.DataFrame({'Token Count': token_counts})
df.hist(bins=40)
plt.show()

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(chunks, embeddings)

query = "Who created transformers?"
docs = db.similarity_search(query)

chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
docs = db.similarity_search(query)
chain.run(input_documents=docs, question=query)

qa = ConversationalRetrievalChain.from_llm(
    OpenAI(temperature=0.1), db.as_retriever())
chat_history = []


def on_submit(_):
    query = input_box.value
    input_box.value = ""
    if query.lower() == 'exit':
        print("Thank you for using the State of the Union chatbot!")
        return
    result = qa({"question": query, "chat_history": chat_history})
    chat_history.append((query, result['answer']))
    display(widgets.HTML(f'<b>User:</b> {query}'))
    display(widgets.HTML(
        f'<b><font color="blue">Chatbot:</font></b> {result["answer"]}'))


input_box = widgets.Text(placeholder='Please enter your question:')
input_box.on_submit(on_submit)
display(input_box)
