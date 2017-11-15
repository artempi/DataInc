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
df1 = pd.read_csv("/home/artem/TEST3/Trump/dict_week1.csv")
df2 = pd.read_csv("/home/artem/TEST3/Trump/dict_week2.csv")
list1=df1['6'].values
list2=df1['0'].values
print(list1.tolist())
#print(df1)
print(len(df1.columns)-3)



#A=cosine_similarity(np.array([document_vector(model, list_all[k])
#                                  for k in range(len(list_all))]))

V1=np.array([document_vector(model, df1[str(k)].values)
                              for k in range(len(df1.columns)-3)])

V2=np.array([document_vector(model, df2[str(k)].values)
                              for k in range(len(df2.columns)-3)])


dfV1=pd.DataFrame(V1)
dfV1.to_csv("./V2_week1.csv")

dfV2=pd.DataFrame(V2)
dfV2.to_csv("./V2_week2.csv")

