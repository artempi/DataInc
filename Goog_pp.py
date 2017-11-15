#! /usr/bin/python

import numpy as np
import pp
import gensim
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import simplejson

model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)
model.init_sims(replace=True)

nproc = 32

job_server = pp.Server(ncpus=nproc)
inmod = ("gensim","np","pd", "simplejson","cosine_similarity")



def document_vector(model, doc):
    # remove out-of-vocabulary words
    doc = [word for word in doc if word in model.vocab]
    return np.mean(model[doc], axis=0)



runs=100
proc=[0 for k in range(nproc+1)]
perproc=(runs/nproc)

def build_list(n):
        df00 = pd.read_csv('./week'+str(n+1)+'.csv')
        list1=df00.as_matrix(columns=df00.columns[1:2])
        list_all=[]

        for element in range(len(list1)):
                list2=list1[element][0]
                list3=str(list2).lower()
                list_all.append(list3.split())

        A=cosine_similarity(np.array([document_vector(model, list_all[k])
                                  for k in range(len(list_all))]))

	f=open('./week'+str(n+1)+'_sim.dat',"w")
	f.write(A)
	f.close()
	return 0

for i in range(0,nproc+1):
   proc[i] = job_server.submit(build_list, (perproc,), (document_vector,), inmod)
job_server.print_stats()
job_server.wait()
job_server.print_stats()

