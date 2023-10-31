import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import TruncatedSVD

import ast



def get_category_mapper(category_df):
    pick_cat = category_df[["id","name"]]
    cat_map=list(pick_cat.itertuples(index=None,name=None))
    return cat_map

def map_cat_id_with_cat(row_list_value,cat_map):
    category =""
    for row_value in row_list_value:
          for cat in cat_map:
            try:   
                if int(row_value)==int(cat[0]):
                    if len(category) > 0:
                        category += "|" + cat[1]
                    else:
                        category += cat[1]
            except:
                #in case of category is string just attach the string once and continue
                 category += "|" + cat[1]
                 break
                
    return category

def create_bow(categories):
    bow = {}
    for category in categories:
        bow[category] = 1
    return bow

def create_lsa_trained_df(lsa_based_df):
        vectorizer = CountVectorizer()
        bow = vectorizer.fit_transform(lsa_based_df['content'])
        # Convert bag of words to TF-IDF
        tfidf_transformer = TfidfTransformer()
        tfidf = tfidf_transformer.fit_transform(bow)
        # Apply LSA or LSI
        lsa = TruncatedSVD(n_components=100, algorithm='arpack')
        lsa.fit(tfidf)
        return tfidf





    

def get__lsa_input_stories_df(stories,cat,onlyContentRequired=False):
     stories_df = stories.copy()
     categories_df = cat.copy()
     tf_idf_words= stories_df.keyword.str.replace(r"[\|[\]|\"|,]","")
     stories_df["keywords_str"] = tf_idf_words
     stories_df.category=stories_df.category.apply(ast.literal_eval)
     stories_df["cat_category"]=stories_df.category.apply(map_cat_id_with_cat,args=(get_category_mapper(categories_df),))
     titles = stories_df['title'].tolist()
     categories_list = stories_df['cat_category'].str.split("|").tolist()
     stories_df["categories_str"]=categories_list
     stories_df["cat_formated"]=stories_df["cat_category"].str.replace("|"," ")
     stories_df.loc[stories_df["description_1"].isnull(),"description_lsa"]=stories_df['title'].astype(str) +  ' ' + stories_df['language'].astype(str) +' ' + stories_df["cat_formated"].astype(str)
     stories_df.loc[stories_df["description_1"].notnull(),"description_lsa"]=stories_df["description_1"]   
     stories_df['content'] = stories_df['title'].astype(str) +  ' ' + stories_df['language'].astype(str) +' ' + stories_df["cat_formated"].astype(str) \
     + ' '+stories_df['keywords_str'] + stories_df['description_lsa']
     stories_df['content'] = stories_df['content'].fillna('')
     if onlyContentRequired:
        return (stories_df[["id","content"]])
     else:
        return stories_df
    
    


    
        
def get_content_based_lsa(story,no_of_recs,lsa_trained_df,lsa_input_stories_df):
     try:
        lsa_input_stories_df = lsa_input_stories_df.reset_index().drop(["index"],axis=1)
        story_index = lsa_input_stories_df[lsa_input_stories_df['title'] == story].index[0]
        similarity_scores = cosine_similarity(lsa_trained_df[story_index], lsa_trained_df)
        # Get the top 10 most similar stories
        similar_stories = list(enumerate(similarity_scores[0]))
        sorted_similar_stories = sorted(similar_stories, key=lambda x: x[1], reverse=True)[1:no_of_recs+1]
        stories_id_list =[]
        for i, score in sorted_similar_stories:
           print("{}: {}".format(lsa_input_stories_df.loc[i,'id'], lsa_input_stories_df.loc[i, 'title']))
           stories_id_list.append(lsa_input_stories_df.loc[i,'id'])
        return stories_id_list
     except:
        print("story not found")
        return None


        
def get_clean_stories(stories_csv_location):
    try:
        stories = pd.read_csv(stories_csv_location)
        active_stories=stories[stories.deleted_at.isnull()]
        active_stories=active_stories[active_stories["status_flag"]==1]
        active_stories2=active_stories.drop([
        "description","new_comment","schedule","created_at",\
        "deleted_at","updated_at","keyword_old","youtube_id","extra_keyword_count",\
        "admin_id"],axis=1)
        return active_stories2
    except:
        print("data base error")
        return None    
    
def get_clean_categories(categories_csv_location):
    try:
        categories = pd.read_csv(categories_csv_location)
        active_categories=categories[categories.deleted_at.isnull()]
        active_categories2=active_categories
        active_categories2=active_categories.drop(["thum_pic","create_at","update_at","deleted_at"],axis=1)
        return active_categories2
    except:
        print("data base error")
        return None 

def filter_by_lanaguage(stories_id_list,stories_df,language_id):
         selected_stories = stories_df[stories_df['id'].isin(stories_id_list)]
         if(language_id!=None):
             return selected_stories[selected_stories['language'] == str(language_id)];
         else:
             return selected_stories
        
def word2vec(word):
    from collections import Counter
    from math import sqrt

    # count the characters in word
    cw = Counter(word)
    # precomputes a set of the different characters
    sw = set(cw)
    # precomputes the "length" of the word vector
    lw = sqrt(sum(c*c for c in cw.values()))

    # return a tuple
    return cw, sw, lw

def cosdis(v1, v2):
    # which characters are common to the two words?
    common = v1[1].intersection(v2[1])
    # by definition of cosine distance we have
    return sum(v1[0][ch]*v2[0][ch] for ch in common)/v1[2]/v2[2]

def reorder_list(content_list_tuple,movie_name):
    try:
        vec_list=[]
        cos_dis_list =[]
        for word in content_list_tuple:
            vec_list.append(dict(s_id=word[0],word= word[1],vector= word2vec(word[1])))
        movie_vector = word2vec(movie_name)
        for item in vec_list:
            cos_dis_list.append(dict(s_id=item.get('s_id'),story_name = item.get('word'),distance = cosdis(item.get('vector'),movie_vector)))
            sorted_list = sorted(cos_dis_list,key= lambda x:x['distance'],reverse=True)
        return [ dict(s_id=cos_dis['s_id'],story_name= cos_dis['story_name']) for cos_dis in sorted_list]
    except:
        print("reordering went wrong")
        return None