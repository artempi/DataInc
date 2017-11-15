import pandas as pd
import numpy as np
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AffinityPropagation

punctuation_map = dict((ord(char), None) for char in string.punctuation)
stemmer = nltk.stem.snowball.EnglishStemmer()

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize)

def get_clusters(sentences):
    tf_idf_matrix = vectorizer.fit_transform(sentences)
    similarity_matrix = (tf_idf_matrix * tf_idf_matrix.T).A
    affinity_propagation = AffinityPropagation(affinity="precomputed", damping=0.5)
    affinity_propagation.fit(similarity_matrix)

    labels = affinity_propagation.labels_
    cluster_centers = affinity_propagation.cluster_centers_indices_
    

    tagged_sentences = zip(sentences, labels)
    clusters = {}

    for sentence, cluster_id in tagged_sentences:
        clusters.setdefault(sentences[cluster_centers[cluster_id]], []).append(sentence)

    return clusters


for m in range(150):
    df = pd.read_csv('./week'+str(m+1)+'.csv')
    clusters = get_clusters(df.text.values)


    retweet=0
    favorite=0
    focus_retweet=''
    focus_favorite=''
    list_retweet=[]
    news_retweet=[]
    list_favorite=[]
    dictionary=[]
    week=[]


    for cluster in clusters:
    #    print(cluster, ':')
        week_str=''
        for element in clusters[cluster]:
    #        print('  - ', element)
             new_list = element.lower()
             week_str=week_str+new_list+" "
             new_list = new_list.split()
             dictionary.append(new_list)
        week.append(week_str)
        retweet_count=pd.DataFrame()
        favorite_count=pd.DataFrame()
        for element in clusters[cluster]:
            n=df.text[df.text == element].index
            retweet_count = retweet_count.append(df.loc[n,'retweet_count'])
            favorite_count = favorite_count.append(df.loc[n,'favorite_count'])
        list_retweet.append(np.nanmedian(retweet_count.values))
        news_retweet.append(cluster)
        list_favorite.append(np.nanmedian(favorite_count.values))
    #    print(np.nanmedian(favorite_count.values))
        if np.nanmedian(retweet_count.values)>retweet:
            retweet=np.nanmedian(retweet_count.values)
            focus_retweet=cluster
            cluster_retweet=pd.DataFrame()
            for k in range(0,len(clusters[cluster])):
                cluster_retweet=cluster_retweet.append(df.loc[df.text == clusters[cluster][k]])
        
        if np.nanmedian(favorite_count.values)>favorite:
            favorite=np.nanmedian(favorite_count.values)
            focus_favorite=cluster
            cluster_favorite=pd.DataFrame()
            for k in range(0,len(clusters[cluster])):
                cluster_favorite=cluster_favorite.append(df.loc[df.text == clusters[cluster][k]])
            
#week.to_csv('/home/artem/TEST3/Trump/clusters.csv')

#print(week)


    df1=pd.DataFrame(
        {'retweet': list_retweet,
         'favorite': list_favorite,
         'text': week
        })


    df1.to_csv('./week'+str(m+1)+'_clust.csv', index=False)
