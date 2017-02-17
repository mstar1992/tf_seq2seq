# encoding=utf-8
import re,os
import jieba
import codecs
import pymongo
import pdb
import jieba
from gensim import corpora, models, similarities
# os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
clinet = pymongo.MongoClient("localhost", 27017)
db = clinet["Sina_rachel"]
data_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fw_train = codecs.open(os.path.join(data_dir,'data/data0119/train.txt'),'w','utf-8')
fw_dev = codecs.open(os.path.join(data_dir,'data/data0119/dev.txt'),'w','utf-8')
fw_all = codecs.open(os.path.join(data_dir,'data/data0119/all_data.txt'),'w','utf-8')
# fw_all = open(os.path.join(data_dir,'data/data0119/all_data.txt'),'w')
stop_path = os.path.join(data_dir, "data/stopword.txt")
def clean_dialog_data(line):
    stop = [i.strip() for i in open(stop_path)]
    line = re.sub(r'http://.*','',line)
    # line = re.sub(r' \W{1,4}·.*','',line)
    line = re.sub(r'\s+| +|　+|️+|^:|\[(.*?)\]|#(.*?)#|《(.*?)》', '', line)
    line = list(jieba.cut(line))
    # for i in line:
    #     print type(i.encode('utf-8'))
    #     break
    line = [i for i in line if i != u'\u200b' and i.encode('utf-8') not in stop]
    return ' '.join(line)
    # new_line.append(' '.join(line))
def mongoData():
    result = db.Tweets.find()
    with open(os.path.join(data_dir,'data/data0119/huanji_clothes.txt'),'r') as f:
      close = [i.strip() for i in f.readlines()]
    print result.count()
    j = 0
    for i in result:
        content = ''.join(i['Content']).encode('utf-8')#(.*?)(?<!有)没(有)*衣服
        # if re.search('(?<!有)没(有)?衣服(.*)买',content) or re.search('换季(.*)衣服(.*)买',content):
        if re.search(r'换季(.*)衣服', content):
          # print type(content)
          # content = clean_dialog_data(content)
          if content not in close:
            content = re.findall(r'((.*?)换季(.*?)衣服(.*?)穿)', content)
            if content != []:
                content = content[0][0]
            # pdb.set_trace()
            # print content[0][0]
            # content = clean_dialog_data(content[0][0])
            # print type(b[0][0])
            # print content
                fw_all.write(content.decode('utf-8') + '\n')
                j += 1
          # print content
    print j
def sentence_similar():
    sentences = open(os.path.join(data_dir, 'data/data0119/all.txt'), 'r')
    words = []
    for doc in sentences:
        doc = clean_dialog_data(doc.strip())
        words.append(doc.split(' '))
    dic = corpora.Dictionary(words)
    # for word, index in dic.token2id.iteritems():
    #     print word
    #     print str(index)
    corpus = [dic.doc2bow(text) for text in words]
    # for i in corpus:
    #     print i
    tfidf = models.TfidfModel(corpus)
    query = clean_dialog_data('每次换季都感觉没有衣服穿')
    query_bow = dic.doc2bow(query.split(' '))
    print query_bow
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=874)
    sims = index[tfidf[query_bow]]
    sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
    print sort_sims

# def clean_dialog_data(data_dir):
#   data_path = os.path.join(data_dir, "data/data/mongodata.txt")
#   stop_path = os.path.join(data_dir, "data/data/stopword.txt")
#   stop = [i.strip() for i in open(stop_path)]
#   # if '哎呀' in stop:
#   #     print type('ok')
#   new_line = []
#   with open(data_path) as f:
#     for line in f.readlines():
#       if re.search('换季(.*?)(?<!有)没(.*?)衣服',line.strip()):
#         line = line.strip()
#         line = re.sub(r'http://.*','',line)
#         # line = re.sub(r' \W{1,4}·.*','',line)
#         line = re.sub(r'\s+| +|　+|️+|^:|\[(.*?)\]', '', line)
#         line = list(jieba.cut(line))
#         # for i in line:
#         #     print type(i.encode('utf-8'))
#         #     break
#         line = [i for i in line if i != u'\u200b' and i.encode('utf-8') not in stop]
#         fw_all.write(' '.join(line)+'\n')
#         fw_all.write(' '.join([u'想',u'买',u'衣服']) + '\n')
#         new_line.append(' '.join(line))
#   for i in list(set(new_line))[50:]:
#     fw_train.write(i+'\n')
#     fw_train.write(' '.join([u'想',u'买',u'衣服']) + '\n')
#   for i in list(set(new_line))[:50]:
#     fw_dev.write(i + '\n')
#     fw_dev.write(' '.join([u'想', u'买', u'衣服']) + '\n')
#         # break
sentence_similar()
# mongoData()