from gensim import corpora, models, similarities
from pykafka import KafkaClient
import pandas as pd
import heapq
import jieba
import sys

TOPIC_P = 'politics3'
TOPIC_E = 'entertainment4'

jieba.set_dictionary('dict.txt.big')
stop_flag  = ['.','．','〔','〕','〝','〞','『 ','』','〈','〉','\\\\','（', '）','～','u3000','\"','&gt','&lt',';','，', '。', '、', '；', '：', '?', '「', '」', '%', '.', ',', '？', '-', '~','!','！', '&nbsp', '<BR>', '“', '”', '【', '】', '《', '》','：','(',')','；']
stop_flag += ['和','的','是','了','也','延伸閱讀','相關報導','更多 NOWnews 今日新聞報導','Line讀者觀看影片','【點我看】','【延伸閱讀】']
stop_flag += ['▲','★','●','2018','04','05','06','07','08','09']

def analysis(subject):

    data = getNews(subject) #拿出在kafka中的新聞

    corpus=[]
    for each in data:
        corpus.append(tokenization(each))

    dictionary = corpora.Dictionary(corpus) #建立詞袋模型
    doc_vectors = [dictionary.doc2bow(text) for text in corpus]
    
    #建立TF-IDF模型
    tfidf = models.TfidfModel(doc_vectors)
    tfidf_vectors = tfidf[doc_vectors]
    print(dictionary)

    def articleSim(article):
        query = tokenization(article) #建立query文本
        query_bow = dictionary.doc2bow(query)
        
        #用TF-IDF計算相似度
        index = similarities.MatrixSimilarity(tfidf_vectors)
        sims = index[query_bow]
        return sims

    result =[]
    for idx,val in enumerate(data):
        row = []
        row.append('Id_'+str(idx+1))

        for i in range(1,6):
            row.append('sid_'+str(idx+1)+str(i))
        data_row = []
        for i in articleSim(val):
            data_row.append(str(i))
        data_row = heapq.nlargest(7,data_row)#找出相似度最高的前五
        result.append(row)
        result.append(data_row)

    return result

def tokenization(news): #用jieba分詞詞並去除停用詞
    result = []
    for word in jieba.cut(news, cut_all=False):
        if word not in stop_flag:
            result.append(word)
    return result

def getNews(topicsname):
    client = KafkaClient(hosts="127.0.0.1:9092")
    topic = client.topics[topicsname]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,consumer_timeout_ms=5000)

    data = []
    for message in consumer:
        if message is not None:
            print(message.offset, (message.value).decode('utf-8'))
            data.append((message.value).decode('utf-8'))
    return data


if __name__ == '__main__':
    topic = ""
    if(sys.argv[1]=='p'):
        topic = TOPIC_P
    elif(sys.argv[1]=='e'):
        topic = TOPIC_E
    else:
        print("input the topic")

    result = analysis(bytes(topic,'utf-8'))
    pd.DataFrame(result).to_csv(topic+'_top5.csv',index=False,header=False)
