from langchain_openai import AzureOpenAIEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import jieba
from langchain_core.documents.base import Document
from rag.bm25Class import BM25
import re

def filter_words(words):
    result = []
    for item in words:
        sentence = []
        for seg in item:
            seg = re.sub(r"[^\w\s]", "", seg)  # 去除标点符号
            if seg:
                sentence.append(seg)
        result.append(sentence)
    return result

def get_answer_radarbm25(query, chunks):
    load_dotenv()

    # 1.实例化大模型
    llm = AzureChatOpenAI(deployment_name="gpt-35", model_name="gpt-3.5-turbo")

    # 2.构造提示模板
    template = """You are a chatbot having a conversation with a human.
        Given the following extracted parts of a long document and a question, create a final answer.
        {context}
        {chat_history}
        Human: {human_input}
        Chatbot:"""
    prompt = PromptTemplate(
        input_variables=["chat_history", "human_input", "context"],
        template=template
    )

    # 3 记忆相关
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="human_input")

    # 4.构造链 （大模型，记忆模块，提示模板）
    chain = load_qa_chain(llm, chain_type="stuff", memory=memory, prompt=prompt)

    # 5.获取与提问相关的文档
    words = [list(jieba.cut(sentence)) for sentence in chunks]  # 将docs中的句子进行分词
    words = filter_words(words)  # 分词后的结果去除标点符号
    print(chunks)   # 纯文本段
    print(len(words))

    bm25 = BM25(words)
    query_words = jieba.cut(query)
    scores = bm25.calculate_score(query_words)
    print(scores)
    document = []
    for index, _ in scores.most_common(3):
        doc_item = Document(page_content=chunks[index])
        document.append(doc_item)
    print(document)

    # 6.使用langchain构造链，传入大模型，问题，以及对应文本信息
    result = chain({"input_documents": document, "human_input": query}, return_only_outputs=True)
    return result['output_text']

def get_answer_radar(query):
    load_dotenv()

    OPENAI_API_KEY = '7dd702067e0f4faf89f278f50ecda262'
    PersisPath = 'D:\Python IDE\GraduateDesign\localdb'

    # 1.实例化openai的词嵌入模型api，用于将向量数据库的向量还原成文本信息
    embeddings = AzureOpenAIEmbeddings(openai_api_key=OPENAI_API_KEY,
                                       azure_endpoint='https://embeddingdemo.openai.azure.com/',
                                       openai_api_type='azure',
                                       deployment='EmbeddingDemo')

    # 2.从本地向量数据库中加载文本
    vectordb = Chroma(persist_directory=PersisPath, embedding_function=embeddings)

    # 3.实例化大模型
    llm = AzureChatOpenAI(deployment_name="gpt-35",
                          model_name="gpt-3.5-turbo")

    # 4.构造提示模板
    template = """You are a chatbot having a conversation with a human.

        Given the following extracted parts of a long document and a question, create a final answer.

        {context}

        {chat_history}
        Human: {human_input}
        Chatbot:"""

    prompt = PromptTemplate(
        input_variables=["chat_history", "human_input", "context"],
        template=template
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="human_input")
    chain = load_qa_chain(llm, chain_type="stuff", memory=memory, prompt=prompt)

    # 5.设置问题，并从数据库中匹配最相似的三条文本
    docs = vectordb.similarity_search(query, 3)

    # 6.使用langchain构造链，传入大模型，问题，以及对应文本信息
    result = chain({"input_documents": docs, "human_input": query}, return_only_outputs=True)
    return result['output_text']

def get_answer_gpt(query):
    load_dotenv()
    llm = AzureChatOpenAI(deployment_name="gpt-35",
                          model_name="gpt-35-turbo")

    prompt = PromptTemplate(
        template="你是一个智能助手，请回答一下问题，{question} ?",
        input_variables=["question"])
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(query)