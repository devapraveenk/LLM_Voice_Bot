# # import bs4
# # from langchain.chains import create_history_aware_retriever, create_retrieval_chain
# # from langchain.chains.combine_documents import create_stuff_documents_chain
# # from langchain_chroma import Chroma
# # from langchain_groq import ChatGroq
# # from langchain_community.chat_message_histories import ChatMessageHistory
# # from langchain_community.document_loaders import WebBaseLoader
# # from langchain_core.chat_history import BaseChatMessageHistory
# # from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# # from langchain_core.runnables.history import RunnableWithMessageHistory
# # # from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # from langchain_community.document_loaders.csv_loader import CSVLoader
# # from langchain_huggingface import HuggingFaceEmbeddings
# # # from langchain_huggingface import HuggingFaceEmbeddings
# # from langchain_community.vectorstores import FAISS

# # groq_api_key = ""
# # llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-groq-70b-8192-tool-use-preview")


# # ### Construct retriever ###
# # loader = CSVLoader(r"/Users/balanivas/Desktop/SIH/server/Copy of Book1(1).csv")
# # # docs = loader.load()
# # import os
# # data = loader.load()
# # db_file_path='musuem'
# # embeddings = HuggingFaceEmbeddings()
# # if not os.path.exists(db_file_path):


# #     db =FAISS.from_documents(data, embeddings)
# #     db.save_local(db_file_path)

# # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# # splits = text_splitter.split_documents(data)
# # db=FAISS.load_local(db_file_path, embeddings,allow_dangerous_deserialization=True)
# # retriever =db.as_retriever(score_threshold=0.7)


# # ### Contextualize question ###
# # contextualize_q_system_prompt = (
# #     "Given a chat history and the latest user question "
# #     "which might reference context in the chat history, "
# #     "formulate a standalone question which can be understood "
# #     "without the chat history. Do NOT answer the question, "
# #     "just reformulate it if needed and otherwise return it as is."
# # )
# # contextualize_q_prompt = ChatPromptTemplate.from_messages(
# #     [
# #         ("system", contextualize_q_system_prompt),
# #         MessagesPlaceholder("chat_history"),
# #         ("human", "{input}"),
# #     ]
# # )
# # history_aware_retriever = create_history_aware_retriever(
# #     llm, retriever, contextualize_q_prompt
# # )


# # ### Answer question ###
# # system_prompt = (
# #     """ "you are an musuem ticket booking chatbot"
# #     "do not hallucinate the response"
# #     "response should not exceed 10 words"
# #      "please accept to book a ticket after the date 11/12/2024 example: 12.12.24"

# #     """
# #     """
# #     user: hi
# #     bot: give some greetings and ask them how to assist
# #     user: if they ask about recommendations or suggestions
# #     bot: reply them acording and suggest them the musuems
# #     user: if they query about booking ticket
# #     bot: ask them and retreive details such as no_of_tickets,date and musuem (if they chose in recommendations avoid asking name of musuem)
# #     user: if they ask about booking link (if they gave everything needed give response: BOOK_NOW)
# #     bot: if they miss any information (ask them kindly those missed information alone)
# #     user: if they ask booking link
# #     bot: do not send them any links (instead if you got everything then sent BOOK_NOW)

# #     user: asks anything outside the box(musuem related)
# #     bot: reply concernly that you are an ai assistant for musuem alone!"""
# # )
# # qa_prompt = ChatPromptTemplate.from_messages(
# #     [
# #         ("system", system_prompt),
# #         MessagesPlaceholder("chat_history"),
# #         ("human", "{input}"),
# #     ]
# # )
# # question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

# # rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


# # ### Statefully manage chat history ###
# # store = {}


# # def get_session_history(session_id: str) -> BaseChatMessageHistory:
# #     if session_id not in store:
# #         store[session_id] = ChatMessageHistory()
# #     return store[session_id]


# # conversational_rag_chain = RunnableWithMessageHistory(
# #     rag_chain,
# #     get_session_history,
# #     input_messages_key="input",
# #     history_messages_key="chat_history",
# #     output_messages_key="answer",
# # )

# # print(conversational_rag_chain.invoke(
# #     {"input": "what is the price of adult ticket in gass forest musuem in coimbatore"},
# #     config={
# #         "configurable": {"session_id": "abcd123"}
# #     },  # constructs a key "abc123" in `store`.
# # )["answer"])


# import bs4
# from langchain.chains import create_history_aware_retriever, create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_chroma import Chroma
# from langchain_groq import ChatGroq
# from langchain_community.chat_message_histories import ChatMessageHistory
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_core.chat_history import BaseChatMessageHistory
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders.csv_loader import CSVLoader
# from langchain_huggingface import HuggingFaceEmbeddings
# # from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS

# groq_api_key = "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"
# llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-8b-instant")


# ### Construct retriever ###
# loader = CSVLoader(r"/Users/balanivas/Desktop/SIH/server/Copy of Book1(1).csv")
# # docs = loader.load()
# import os
# data = loader.load()
# db_file_path='musuem'
# embeddings = HuggingFaceEmbeddings()
# if not os.path.exists(db_file_path):


#     db =FAISS.from_documents(data, embeddings)
#     db.save_local(db_file_path)

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# splits = text_splitter.split_documents(data)
# db=FAISS.load_local(db_file_path, embeddings,allow_dangerous_deserialization=True)
# retriever =db.as_retriever(score_threshold=0.7)


# ### Contextualize question ###
# contextualize_q_system_prompt = (
#     "Given a chat history and the latest user question "
#     "which might reference context in the chat history, "
#     "formulate a standalone question which can be understood "
#     "without the chat history. Do NOT answer the question, "
#     "just reformulate it if needed and otherwise return it as is."
# )
# contextualize_q_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", contextualize_q_system_prompt),
#         MessagesPlaceholder("chat_history"),
#         ("human", "{input}"),
#     ]
# )
# history_aware_retriever = create_history_aware_retriever(
#     llm, retriever, contextualize_q_prompt
# )


# ### Answer question ###
# system_prompt = (
#     "you are an ticket booking chatbot"
#     "dont recomand only museums"
#     "recomand accordingly to the area of interest if said"
#     "do not hallucinate the response"
#     "response should not exceed 10 words"
#     "dont provide like booking completed just get information and trigger BOOK_NOW"
#     "if user asked any place is not in the database , please reply them accordingly (dont say not in db)"
#     "dont send any unnecessary links"
#     "just retrive information and give booking details and BOOK_NOW"
#     "kindly fetch the correct prices from database fetch only indian (not foreign prices)"
# """
#     user: hi
#     bot: give some greetings as hi and ask them how to assist
#     user: if they ask about recommendations or suggestions
#     bot: reply them according to the query and suggest them the places from there
#     user: if they query about booking ticket
#     bot: ask them and retreive details such as no_of_tickets,date and musuem (if they chose in recommendations avoid asking name of musuem)
#     user: if they ask about booking link (if they gave everything needed give response: BOOK_NOW)
#     bot: if they miss any information (ask them kindly those missed information alone)
#     user: if they ask booking link
#     bot: do not send them any links (instead if you got everything then sent BOOK_NOW)

#     user: asks anything outside the box(related)
#     bot: reply concernly that you are an ai assistant !
#      """

#     "\n\n"
#     "{context}"
# )
# qa_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", system_prompt),
#         MessagesPlaceholder("chat_history"),
#         ("human", "{input}"),
#     ]
# )
# question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

# rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


# ### Statefully manage chat history ###
# store = {}


# def get_session_history(session_id: str) -> BaseChatMessageHistory:
#     if session_id not in store:
#         store[session_id] = ChatMessageHistory()
#     return store[session_id]


# conversational_rag_chain = RunnableWithMessageHistory(
#     rag_chain,
#     get_session_history,
#     input_messages_key="input",
#     history_messages_key="chat_history",
#     output_messages_key="answer",
# )

# print(conversational_rag_chain.invoke(
#     {"input": "what is the price of adult ticket in gass forest musuem in coimbatore"},
#     config={
#         "configurable": {"session_id": "abcd123"}
#     },  # constructs a key "abc123" in `store`.
# )["answer"])


import bs4
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings

# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.retrievers import (
    ContextualCompressionRetriever,
    MergerRetriever,
)

# from  langchain_openai import ChatOpenAI
import os
from datetime import date

# from langchain_ollama import ChatOllama
# Returns the current local date
today = date.today()

groq_api_key = ""
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")
# from langchain_google_genai import ChatGoogleGenerativeAI
# llm = ChatOllama(
#     model="llama3.1",
#     temperature=0.4,
#     # other params...
# )
# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-pro",
#     api_key= '',
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
#     # other params...
# )
# llm = model = ChatOpenAI(model="GPT-4o mini", temperature=0,api_key='')
PLACE1 = ".\full"


urls = [
    "https://insider.in/all-events-in-chennai",
    "https://insider.in/all-events-in-coimbatore",
    "https://insider.in/all-events-in-kolkata",
    "https://insider.in/all-events-in-mumbai",
    "https://insider.in/all-events-in-delhi",
    "https://insider.in/all-events-in-banglore",
    "https://insider.in/all-events-in-patna",
]

loader = UnstructuredURLLoader(urls=urls)

data = loader.load()

embeddings = HuggingFaceEmbeddings()

full = []
text_splitters = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
documents = text_splitters.split_documents(data)
full.extend(documents)
# documents = [Document(page_content=text) for text in splits]

if not os.path.exists(PLACE1):
    db = FAISS.from_documents(documents=documents, embedding=HuggingFaceEmbeddings())
    db.save_local(PLACE1)
else:
    db = FAISS.load_local(PLACE1, embeddings, allow_dangerous_deserialization=True)

PLACE2 = "./PLACE2"

retriever1 = db.as_retriever()

loader = CSVLoader(file_path="Copy of Book1(1).csv")
data = loader.load()

documents = text_splitters.split_documents(data)
full.extend(documents)
# print(full)
# documents = [Document(page_content=text) for text in splits]
# print(documents)

if not os.path.exists("./full"):
    db = FAISS.from_documents(documents=full, embedding=HuggingFaceEmbeddings())
    db.save_local("./full")
else:
    db = FAISS.load_local(PLACE2, embeddings, allow_dangerous_deserialization=True)

# retriever2 = db.as_retriever()
# ### Construct retriever ###
# # loader = CSVLoader(r"data_assets\cleaned_ticket_booking_data.csv")
# # # docs = loader.load()
# # import os
# # data = loader.load()
# # db_file_path='musuem'
# # embeddings = HuggingFaceEmbeddings()
# # if not os.path.exists(db_file_path):


# #     db =FAISS.from_documents(data, embeddings)
# #     db.save_local(db_file_path)

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# splits = text_splitter.split_documents(data)
# # db=FAISS.load_local(db_file_path, embeddings,allow_dangerous_deserialization=True)
# # retriever =db.as_retriever(score_threshold=0.7)


# ### Contextualize question ###
# contextualize_q_system_prompt = (
#     "You are an chatbot for musuem ticket booking tasks. "
#     "do not move away from musuem ticket assistant"
#     "answer in a crisp and proficiently short chat"
#     "try to answer within 2 lines"
#     "do not say to collect tickets ffrom counter"
#     "if you get the details (date,number of tickets) then ask them to click the link below to book ticket otherwise do not give them link"
#     "the link is book now"
#     "Use the following pieces of retrieved context to answer "
#     "do not do away from instructions be precious"
#     "please give response within a line"
#     "answer concise."
# )
# contextualize_q_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", contextualize_q_system_prompt),
#         MessagesPlaceholder("chat_history"),
#         ("human", "{input}"),
#     ]
# )

# lotr = MergerRetriever(retrievers=[retriever2,retriever1])
# history_aware_retriever = create_history_aware_retriever(
#     llm, lotr, contextualize_q_prompt
# )


# ### Answer question ###
# system_prompt = (
#    "you are an indian musuem ticket booking chatbot"
#    "help user to book the tickets in chatbot"
#     "do not hallucinate the response"
#     "response should not exceed 10 words"
#     "if user asked musuem is not in the database , please reply them accordingly (say not in db)"
#     """
#     user: hi
#     bot: give some greetings and ask them how to assist
#     user: if they ask about recommendations or suggestions
#     bot: reply them acording and suggest them the musuems
#     user: if they query about booking ticket
#     bot: ask them and retreive details such as no_of_tickets,date and musuem (if they chose in recommendations avoid asking name of musuem)
#     user: if they ask about booking link (if they gave everything needed give response: BOOK_NOW)
#     bot: if they miss any information (ask them kindly those missed information alone)
#     user: if they ask booking link
#     bot: do not send them any links (instead if you got everything then sent BOOK_NOW)
#     user: asks anything outside the box(musuem related)
#     bot: reply concernly that you are an ai assistant for musuem alone!"""
#     "\n\n"
#     "{context}"
# )
# qa_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", system_prompt),
#         MessagesPlaceholder("chat_history"),
#         ("human", "{input}"),
#     ]
# )
# question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

# rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


# ### Statefully manage chat history ###
# store = {}


# def get_session_history(session_id: str) -> BaseChatMessageHistory:
#     if session_id not in store:
#         store[session_id] = ChatMessageHistory()
#     return store[session_id]


# conversational_rag_chain = RunnableWithMessageHistory(
#     rag_chain,
#     get_session_history,
#     input_messages_key="input",
#     history_messages_key="chat_history",
#     output_messages_key="answer",
# )

# # print(conversational_rag_chain.invoke(
# #     {"input": "what are the events scheduled in coimbatore "},
# #     config={
# #         "configurable": {"session_id": "ab23"}
# #     },  # constructs a key "abc123" in `store`.
# # )["answer"])

# # while True:
# #     res = input('enter your prompt')+' please give events after date:12/12/2024'
# #     if 'bye' in res or 'exit' in res:
# #         break
# #     print('response')
# #     print(conversational_rag_chain.invoke(
# #     {"input":  res},
# #     config={
# #         "configurable": {"session_id": "ab23"}
# #     },  # constructs a key "abc123" in `store`.
# # )["answer"])
