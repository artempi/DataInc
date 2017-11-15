import gensim
import numpy as np
import simplejson

model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)


model.init_sims(replace=True)

def document_vector(model, doc):
    doc = [word for word in doc if word in model.vocab]
    return np.mean(model[doc], axis=0)

from sklearn.metrics.pairwise import cosine_similarity



import pandas as pd
df1 = pd.read_csv("./week1_clust.csv")
df2 = pd.read_csv("./week3_clust.csv")
list1=df1.as_matrix(columns=df1.columns[2:3])
list_all1=[]
list2=df2.as_matrix(columns=df2.columns[2:3])
list_all2=[]
for element in range(len(list1)):
    list1a=list1[element][0]
    list1b=str(list1a).lower()
    list_all1.append(list1b.split())
for element in range(len(list2)):
    list2a=list2[element][0]
    list2b=str(list2a).lower()
    list_all2.append(list2b.split())




#A=cosine_similarity(np.array([document_vector(model, list_all[k])
#                                  for k in range(len(list_all))]))

V1=np.array([document_vector(model, list_all1[k])
                              for k in range(len(list_all1))])

V2=np.array([document_vector(model, list_all2[k])
                              for k in range(len(list_all2))])


dfV1=pd.DataFrame(V1)
dfV1.to_csv("./V_week1.csv")

dfV2=pd.DataFrame(V2)
dfV2.to_csv("./V_week3.csv")

