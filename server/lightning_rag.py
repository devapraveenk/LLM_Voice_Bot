# # from langchain_community.document_loaders.pdf import PyPDFLoader
# from langchain_community.document_loaders.csv_loader import CSVLoader
# from langchain_community.vectorstores import FAISS
# from langchain_groq import ChatGroq
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# # from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.chains import create_retrieval_chain
# from langchain.chains import create_history_aware_retriever
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import MessagesPlaceholder
# # from langchain_core.messages import AIMessage, HumanMessage
# # from langchain.memory import ConversationBufferMemory
# # from langchain_core.prompts import PromptTemplate
# from langchain_huggingface import HuggingFaceEmbeddings
# import os
# # from langchain_ollama import ChatOllama

# # model = ChatOllama(
# #     model="llama3.1",
# #     temperature=0.4,
# #     # other params...
# # )


# groq_api_key = "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"


# embeddings = HuggingFaceEmbeddings(
#     model_name="mixedbread-ai/mxbai-embed-large-v1",
#     encode_kwargs = {'precision': 'binary'}
#     )
# db_file_path = r"vector_stores/one-bit"
# if os.path.exists(db_file_path):
#     one_bit_vectorstore = FAISS.load_local(db_file_path, embeddings,allow_dangerous_deserialization=True)
# else:
#     loader = CSVLoader(r"/Users/balanivas/Desktop/SIH/server/Copy of Book1(1).csv")
#     docs = loader.load()

#     text_splitter = RecursiveCharacterTextSplitter()
#     documents = text_splitter.split_documents(docs)

#     one_bit_vectorstore = FAISS.from_documents(documents, embeddings)
#     one_bit_vectorstore.save_local(db_file_path)

# one_bit_retriever = one_bit_vectorstore.as_retriever(
#                                                     search_kwargs={"k": 3}
#                                                     )

# contextualize_q_system_prompt  = """
#  "you are an ticket booking chatbot"
#     "dont recomand only museums"
#     "recomand accordingly to the area of interest if said"
#     "do not say or gurantee the  successfull payment instead ask user to click the book_now button"
#     "do not hallucinate the response"
#     "if asked about local events just take from web and answer"
#     "if the places is in dataset just answer accordingly to the dataset"
#     "response should not exceed 10 words"
#     "dont provide like booking completed just get information and trigger BOOK_NOW"
#     "if user asked any place is not in the database , please reply them accordingly (dont say not in db)"
#     "dont send any unnecessary links"
#     "just retrive information and give booking details and BOOK_NOW"
#     "kindly fetch the correct prices from database fetch only indian (not foreign prices)"
#     "do not ask phone number and mail address from user"
# """
# """
#     user: hi
#     bot: give some greetings as hi and ask them how to assist
#     user: if they ask about recommendations or suggestions
#     bot: reply them according to the query and suggest them the places from there
#     user: if they query about booking ticket
#     bot: ask them and retreive details such as no_of_tickets,date and place to visit (if they chose in recommendations avoid asking name of musuem)
#     user: if they ask about booking link (if they gave everything needed give response: BOOK_NOW)
#     bot: if they miss any information (ask them kindly those missed information alone)
#     user: if they ask booking link
#     bot: do not send them any links (instead if you got everything then sent BOOK_NOW)

#     user: asks anything outside the box(related)
#     bot: reply concernly that you are an ai assistant !
# """

# contextualize_q_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", contextualize_q_system_prompt),
#         MessagesPlaceholder("chat_history"),
#         ("human", "{input}"),
#     ]
# )

# #
# model = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-8b-instant")
# # document_chain = create_stuff_documents_chain(model, prompt)
# # one_bit_retrieval_chain = create_retrieval_chain(retriever = one_bit_retriever, document_chain)
# history_aware_retriever = create_history_aware_retriever(
#     model, one_bit_retriever, contextualize_q_prompt
# )
# system_prompt = (
#     "you are an musuem ticket booking chatbot"
#     "do not hallucinate the response"
#     "response should not exceed 10 words"
#     "please accept to book a ticket after the date 11/12/2024 example: 12.12.24 "

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
#     bot: reply concernly that you are an ai assistant for musuem alone!


#     """

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
# question_answer_chain = create_stuff_documents_chain(model, qa_prompt)

# rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
# # response = one_bit_retrieval_chain.invoke({"input": "What does the paper introduce?" })
# # print(response["answer"])
# # chat_history = []
# # question = 'i want to book ticket'
# # response = rag_chain.invoke({'input':question, "chat_history": chat_history})
# # chat_history.extend(
# #     [
# #         HumanMessage(content=question),
# #         AIMessage(content=response["answer"]),
# #     ]
# # )
# # print(response['answer'])


# from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter

# from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain, LLMChain
from langchain.chains import create_history_aware_retriever, ConversationChain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage, HumanMessage

# from langchain.memory import ConversationBufferMemory
# from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
import os

# from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

# model = ChatOllama(
#     model="llama3.1",
#     temperature=0.4,
#     # other params...
# )


groq_api_key = "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"


embeddings = HuggingFaceEmbeddings()
db_file_path = r".\full"
if os.path.exists(db_file_path):
    one_bit_vectorstore = FAISS.load_local(
        db_file_path, embeddings, allow_dangerous_deserialization=True
    )
else:
    loader = CSVLoader(r"Copy of Book1(1).csv")
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)

    one_bit_vectorstore = FAISS.from_documents(documents, embeddings)
    one_bit_vectorstore.save_local(db_file_path)

one_bit_retriever = one_bit_vectorstore.as_retriever(search_kwargs={"k": 3})

contextualize_q_system_prompt = """
 "You are an chatbot for musuem ticket booking tasks. "
    "do not move away from musuem ticket assistant"
    "answer in a crisp and proficiently short chat"
    "try to answer within 2 lines"
    "do not say to collect tickets ffrom counter"
    "if you get the details (date,number of tickets) then ask them to click the link below to book ticket otherwise do not give them link"
    "the link is book now"
    "Use the following pieces of retrieved context to answer "
    "do not do away from instructions be precious"
    "please give response within a line"
    "answer concise."
"""

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
# from langchain_openai import ChatOpenAI
# model =
model = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")
# model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0,api_key='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')
# model = ChatOpenAI(model="gpt-4o-mini", temperature=0.2,api_key='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')
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase

template = """
    "you are an indian musuem ticket booking chatbot as well as good recommendation agent"
    "Brief explain the response within 20 words"
    "if there is any discount or any offer please tell the user"
    "if the user wants to know about the events kindly response accordingly"
    "if user asked musuem is not in the database , please reply them accordingly (say not in db)"
    "dont halucinate i am only a ai assisstant for museum"
    "you are an event researcher"
    
    user: hi
    bot: give some greetings and ask them how to assist
    user:recommand me places to visit for one day within a budget of rupees 1000 in mumbai
    bot: help them to book the ticket within the budget within the constraints
    user: what are the upcoming events in chennai?
    bot: give them the evnts from the knowledge based
    user: if they query about booking ticket
    bot: ask them and retreive details such as no_of_tickets,date and musuem (if they chose in recommendations avoid asking name of musuem)
    user: if they ask about booking link (if they gave everything needed give response: BOOK_NOW)
    bot: if they miss any information (ask them kindly those missed information alone)
    user: if they ask booking link
    bot: do not send them any links (instead if you got everything then sent BOOK_NOW)
    
    user: asks anything outside the box(musuem related)
    bot: reply concernly that you are an ai assistant for musuem alone! 
{chat_history}
Human: {human_input}
Chatbot: """

# Here it is by default set to "AI"
# Now we can override it and set it to "AI Assistant"
from langchain_core.prompts.prompt import PromptTemplate

# Now we can override it and set it to "Friend"
from langchain_core.prompts.prompt import PromptTemplate

template = """"you are an indian musuem ticket booking chatbot"
    "do not hallucinate the response"
    "response should not exceed 10 words"
    "if user asked musuem is not in the database , please reply them accordingly (say not in db)"

    user: hi
    bot: give some greetings and ask them how to assist
    user: if they ask about recommendations or suggestions 
    bot: reply them acording and suggest them the musuems
    user: if they query about booking ticket
    bot: ask them and retreive details such as no_of_tickets,date and musuem (if they chose in recommendations avoid asking name of musuem)
    user: if they ask about booking link (if they gave everything needed give response: BOOK_NOW)
    bot: if they miss any information (ask them kindly those missed information alone)
    user: if they ask booking link
    bot: do not send them any links (instead if you got everything then sent BOOK_NOW)
    
    user: asks anything outside the box(musuem related)
    bot: reply concernly that you are an ai assistant for musuem alone! 

Current conversation:
{history}
Friend: {input}
AI:"""
PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
conversation = ConversationChain(
    prompt=PROMPT,
    llm=model,
    verbose=True,
    memory=ConversationBufferMemory(human_prefix="Friend"),
)

print(conversation.predict(input="Hi there!"))
# db = SQLDatabase.from_uri("sqlite:///sql.db")
# from langchain_community.tools.sql_database.tool import (
#     InfoSQLDatabaseTool,
#     ListSQLDatabaseTool,
#     QuerySQLCheckerTool,
#     QuerySQLDataBaseTool,
# )
# tools = [ InfoSQLDatabaseTool(),
#     ListSQLDatabaseTool(),
#     QuerySQLCheckerTool(),
#     QuerySQLDataBaseTool()]
# model.bind_tools(tools)
# document_chain = create_stuff_documents_chain(model, prompt)
# one_bit_retrieval_chain = create_retrieval_chain(one_bit_retriever, document_chain)
history_aware_retriever = create_history_aware_retriever(
    model, one_bit_retriever, contextualize_q_prompt
)

system_prompt = (
    "you are an indian musuem ticket booking chatbot"
    "do not hallucinate the response"
    "response should not exceed 10 words"
    "if user asked musuem is not in the database (use your own knowledge) to answer the queries"
    "do not ask the timings or time slots from user"
    """ 
    user: hi
    bot: give some greetings and ask them how to assist
    user: if they ask about recommendations or suggestions 
    user: suggest me places to visit
    bot: ask for which area if no area is provided, ask like cities like goa, mumbai, chennai
    user : suggest me any event in mumbai
    bot: there are number of events happening one includes ex : fire show , stand up comedy (please retreive from database)
    user:if user ask about the discount of musuems
    bot:response the musuems with discounts accordingly 
    user: if they ask about recommendations or suggestions 
    bot: reply them acording and suggest them the musuems
    bot: reply them acording and suggest them the musuems
    user: if they query about booking ticket
    bot: ask them and retreive details such as no_of_tickets,date and musuem (if they chose in recommendations avoid asking name of musuem)
    user: if they ask about booking link (if they gave everything needed give response: BOOK_NOW)
    bot: if they miss any information (ask them kindly those missed information alone)
    user: if they ask booking link
    bot: do not send them any links (instead if you got everything then sent BOOK_NOW)
    
    user: asks anything outside the box(musuem related)
    bot: reply concernly that you are an ai assistant for musuem alone!

"""
    "\n\n"
    "{context}"
)
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
question_answer_chain = create_stuff_documents_chain(model, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
# response = one_bit_retrieval_chain.invoke({"input": "What does the paper introduce?" })
# print(response["answer"])
# chat_history = []
# question = 'i want to book ticket'
# response = rag_chain.invoke({'input':question, "chat_history": chat_history})
# chat_history.extend(
#     [
#         HumanMessage(content=question),
#         AIMessage(content=response["answer"]),
#     ]
# )
# print(response['answer'])
