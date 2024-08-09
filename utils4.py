# 📑 AI智能PDF问答工具

from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os


def qa_agent(openai_api_key, memory, uploaded_file, question):
    temp_file_path = None
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key, base_url="https://api.aigc369.com/v1")
    try:
        file_content = uploaded_file.read()
        temp_file_path = "temp.pdf"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(file_content)
        loader = PyPDFLoader(temp_file_path)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=50,
            separators=["\n", "。", "!", "?", "，", "、", ""]
        )
        texts = text_splitter.split_documents(docs)
        embeddings_model = OpenAIEmbeddings(base_url="https://api.aigc369.com/v1")
        db = FAISS.from_documents(texts, embeddings_model)
        retriever = db.as_retriever()
        qa = ConversationalRetrievalChain.from_llm(
            llm=model,
            retriever=retriever,
            memory=memory
        )
        response = qa.invoke({"chat_history": memory, "question": question})
        return response
    except Exception as e:
        # 更具体的错误处理
        if isinstance(e, FileNotFoundError):
            print("指定的文件未找到")
        elif isinstance(e, PermissionError):
            print("权限错误，无法访问或操作文件")
        else:
            print(f"发生未知错误: {e}")
    finally:
        if os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception as remove_error:
                print(f"删除临时文件时出错: {remove_error}")
