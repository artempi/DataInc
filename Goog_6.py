import gensim
import numpy as np
import simplejson

model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)


model.init_sims(replace=True)

doc1=['trum', 'wwwwwwwwwjhiocioj', 'election']
doc2=['north', 'korea', 'launched', 'misile']
doc3=['ilinois', 'voted', 'for', 'trump']

#doc_all=[['@trump', 'won', '#election'],['north', 'korea', 'launched', 'missile'],['illinois', 'voted', 'for', 'trump']]
def document_vector(model, doc):
    # remove out-of-vocabulary words
    doc = [word for word in doc if word in model.vocab]
    return np.mean(model[doc], axis=0)

from sklearn.metrics.pairwise import cosine_similarity

#print(cosine_similarity(np.array([document_vector(model, doc_all[k])
#                                  for k in range(3)])))

#print(model.similarity('trump won election', 'north korea launched missile'))


import pandas as pd
df00 = pd.read_csv("./week6.csv")
list1=df00.as_matrix(columns=df00.columns[1:2])
list_retweet=df00.as_matrix(columns=df00.columns[3:4])
list_favorite=df00.as_matrix(columns=df00.columns[4:5])


list_all=[]

for element in range(len(list1)):
    list2=list1[element][0]
    list3=str(list2).lower()
#    print(list3.split())
    list_all.append(list3.split())
#print(list_all)

A=cosine_similarity(np.array([document_vector(model, list_all[k])
                                  for k in range(len(list_all))]))




from sklearn.cluster import DBSCAN
B=DBSCAN(min_samples=2, eps=0.4).fit_predict(A)
#print(B)


text_dict = dict()
favorite_dict = dict()
retweet_dict = dict()
for i in range(len(B)):
    if B[i] in text_dict:
        # append the new number to the existing array at this slot
        text_dict.setdefault(B[i],[]).extend(list_all[i])
#        favorite_dict[B[i]].extend(retweet[i])
#	retweet_dict[B[i]].extend(retweet[i])
    else:
        # create a new array in this slot
        text_dict[B[i]] = list_all[i]
#        favorite_dict[B[i]] = list_favorite[i]
#        retweet_dict[B[i]] = list_retweet[i]
#print(text_dict)
#print(retweet_dict)
#print(favorite_dict)

df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in text_dict.items() ]))
df.to_csv("./dict_week6.csv")

#f=open('week1_sim.dat','w')
#simplejson.dump(B, f)
#f.close()

