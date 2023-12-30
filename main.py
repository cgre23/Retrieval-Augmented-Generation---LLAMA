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

fmt='json'
# Make sure that you place the OPENAI_API_KEY in the .env file in this folder
load_dotenv()


def fetch_papers(fmt):

    """Fetches papers from the arXiv API and returns them as a list of strings."""
    url = 'http://export.arxiv.org/api/query?search_query=ti:llama&start=0&max_results=70'
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    root = ET.fromstring(data)
    papers_list = []

    for entry in root.findall('{http://www.w3.org/2005/Atom}entry' ):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
        paper_info = f"Title: {title}\n Summary: {summary}\n"

        papers_list.append(paper_info)
    # Check if the list has some content
    if fmt == 'json':
        dic = {}
        dic['content'] = papers_list
    
        if papers_list != []:
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(dic, f)
                
    if papers_list != [] and fmt == 'txt':
        file = open('data.txt','w')
        for item in papers_list:
            file.write(item)
        file.close()

    return 

if __name__ == "__main__":
    fetch_papers('json')
    
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
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()

    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    #prompt = hub.pull("rlm/rag-prompt")

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)


    def format_docs(docs):
        return "\n".join(doc.page_content for doc in docs)


    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    print(rag_chain.invoke("Name at least 5 domain-specific LLMs that have been created by fine-tuning Llama-2."))