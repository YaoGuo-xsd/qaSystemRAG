import math
from collections import Counter


class BM25:
    def __init__(self, documents, k1=1.5, b=0.75):
        self.documents = documents
        self.k1 = k1
        self.b = b
        self.avgdl = sum(len(doc) for doc in documents) / len(documents)   # 平均文档长度（平均每个文档中包含词语个数）
        self.idf = self.calculate_idf()  # 计算词语的逆文档频率（idf）

    def calculate_idf(self):
        idf = {}
        doc_count = len(self.documents)   # 文档数量
        for doc in self.documents:  # 遍历每个文档
            for term in set(doc):  # 遍历文档中的每个词语，使用set函数去重。
                idf[term] = idf.get(term, 0) + 1  # 将词语的idf值加1，并将结果存储在idf字典中，键为词语，值为包含该词语的文档个数
        for term, freq in idf.items(): # 遍历idf字典中的每个键值对。
            idf[term] = math.log(doc_count + 0.5) - math.log(freq + 0.5)  # 计算词语的idf值，使用BM25算法的公式，将结果存储在idf字典中。
        return idf # 返回计算得到的idf字典， 文档中所有词，每个词对应一个idf值，

    # 对提问中的每一个词，依次与documents中的所有文档进行评分，然后将每个文档针对每个词的评分相加，获得这个文档的评分
    def calculate_score(self, query):
        scores = Counter()  # 创建一个空的Counter对象，用于存储文档的得分
        for term in query: # 遍历查询词语
            if term in self.idf: # 判断查询词语是否在idf字典中。
                for i, doc in enumerate(self.documents): # 遍历每个文档的索引和内容。
                    tf = doc.count(term) # 计算词语在某一个文档中的出现次数，并将结果赋值给变量tf。
                    # 根据BM25算法计算当前文档与查询的匹配得分。其中，self.idf[term]表示词语的逆文档频率（idf），tf表示词语的词频，self.k1和self.b为BM25算法的调节参数，len(doc)表示当前文档的长度（即词语个数），self.avgdl表示平均文档长度。
                    score = self.idf[term] * tf * (self.k1 + 1) / (
                                tf + self.k1 * (1 - self.b + self.b * len(doc) / self.avgdl))
                    scores[i] += score # 将当前文档的得分加到对应索引的计数器中。
        return scores
