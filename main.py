import urllib
import xml.etree.ElementTree as ET
import os
from langchain import hub
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.document_loaders import TextLoader, JSONLoader
from pathlib import Path
import json
import logging
fmt='json' # Choose 'txt' or 'json' format. The JSON format creates a document for every publication. The TXT format creates one long document.
# Make sure that you place the OPENAI_API_KEY in the .env file in this folder
load_dotenv()


def fetch_papers(fmt):

    """Fetches papers from the arXiv API and returns them as a list of strings."""
    url = 'http://export.arxiv.org/api/query?search_query=ti:llama&start=0&max_results=70'
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    root = ET.fromstring(data)
    papers_list = []
    # Iterate entries
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry' ):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
        paper_info = f"Title: {title} Summary: {summary}"
        papers_list.append(paper_info)
        
    # Check if the list has some content and save to either json or txt format
    if fmt == 'json':
        dic = {}
        dic['content'] = papers_list
        if papers_list != []:
            logging.info('Writing data to data.json')
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(dic, f)
        else:
            logging.info('Using existing data.json file')
                
    if papers_list != [] and fmt == 'txt':
        logging.info('Writing data to data.txt')
        file = open('data.txt','w')
        for item in papers_list:
            file.write(item)
        file.close()
    else:
        logging.info('Using existing data.txt file')

    return 

if __name__ == "__main__":
    # Fetch papers from the API
    fetch_papers(fmt)
    
    # Load data from file
    if fmt == 'json':
        loader = JSONLoader(
            file_path="./data.json",
            jq_schema='.content[]',
            text_content=True)
        docs = loader.load()
    else:
        loader = TextLoader("./data.txt")
        docs = loader.load()
        
    # Split text and create vector embeddings
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200, separators=["\n\n", "\n", " ", ""])
    splits = text_splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()
    
    # Potential alternative prompt, in case tweaks are necessary
    template = """Answer the question based only on the following context:
    {context}

     Question: {question}
     """
    #prompt = ChatPromptTemplate.from_template(template)
    prompt = hub.pull("rlm/rag-prompt") # Using default RAG prompt

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)


    def format_docs(docs):
        return "\n".join(doc.page_content for doc in docs)

    # Create RAG chain
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # Prompt user for input, and break when the input is an empty string
    while True:
        val = input("Enter your prompt: ")
        if val == '':
            break
        print(rag_chain.invoke(val))
        