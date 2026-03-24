from langchain_openai import AzureOpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import jieba

OPENAI_API_KEY = '7dd702067e0f4faf89f278f50ecda262'
PersisPath = 'localdb'

# 加载txt文件
def load_txt(file_name):
    url = 'uploadfiles/' + file_name
    loader = TextLoader(url, encoding='utf=8')
    return loader.load()

# 加载pdf文件
def load_pdf(file_name):
    url = 'uploadfiles/' + file_name
    loader = PyPDFLoader(url)
    return loader.load()

# 加载md文件
def load_md(file_name):
    url = 'uploadfiles/' + file_name
    loader = UnstructuredMarkdownLoader(url)
    return loader.load()

# 向量数据库检索方法
def save_file_chroma(doc):
    # 1.构建分片器，将文件进行切分
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,)
    chunks = text_splitter.split_documents(doc)

    # 2.实例化openai的词嵌入模型api
    embeddings = AzureOpenAIEmbeddings(openai_api_key=OPENAI_API_KEY,
                                       azure_endpoint='https://embeddingdemo.openai.azure.com/',
                                       openai_api_type='azure',
                                       deployment='EmbeddingDemo')

    # 3.实例化chroma类, 将文件向量化，存入本地的向量数据库
    vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory=PersisPath)
    vectorstore.persist()


# 使用BM25检索方法
def save_file_db(doc):
    # 1.构建分片器，将文件进行切分
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,)
    chunks = text_splitter.split_documents(doc)
    # 2.对切片句子进行处理，分词
    docs = [do.page_content for do in chunks]  # 去除chunks中每个句子的元数据，只保留句子文本信息
    return docs
