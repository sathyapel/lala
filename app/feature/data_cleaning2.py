import pandas as pd
import ast

def get_country_name(code):
    for idx in range(len(country_code_list)):
        print(country_code_list[idx])
        print(country_code_list[idx].get('Dial'))
        if(country_code_list[idx].get('Dial') == str(code)):
            return country_code_list[idx].get('CLDR display name')
        else:
            return None




def filter_users_as_parents(users_csv_location):
    users=pd.read_csv(users_csv_location)
    droping_columns= ['number','new_number','mail_id','password','otp','otp_time','new_country_code',
                  'provider_id','provider_name','device_token','is_verified','deleted_at','name']
    users2 = users.drop(droping_columns,axis=1)
    country_code=pd.read_csv('country_code.csv') #'CLDR display name'
    country_code_list=country_code[["Dial","CLDR display name"]].to_dict(orient='records')
    missing_country_names_code = users2.loc[users2.country.isna(),"country_code"]
    missing_names=missing_country_names_code.apply(
    lambda code:[code_name.get('CLDR display name')
    for code_name in country_code_list if code_name.get('Dial')==str(code)])
    missing_names1 = missing_names.apply(lambda country_list: "".join(country_list))
    users2.loc[users2.country.isna(),"country"]=missing_names1
    users2.longitude.fillna('unknown',inplace=True)
    users2.latitude.fillna('unknown',inplace=True)
    users2.location.fillna('unkown',inplace=True)
    return users2
def cleanup_parents_kids_data(parent_csv_location,kids_csv_location):
    try:
        parents = pd.read_csv(parent_csv_location)
        parents = parents[parents.columns[1:]]
        parents_renamed=parents.rename(columns={"id":"parent_id"})
        kids_df = pd.read_csv(kids_csv_location)
        active_kids = kids_df[~(kids_df.deleted_at.notnull())].drop(["deleted_at","nick_name","status_flag","img"],axis=1)
        kids_parents_df = active_kids.merge(parents_renamed,on="parent_id",how="left")
        parent_kids_data = kids_parents_df.dropna().drop_duplicates()
        return parent_kids_data
    except:
        print("datum changed in csv")
        return None


def get_clean_stories(stories_csv_location):
    try:
        stories = pd.read_csv(stories_csv_location)
        active_stories=stories[stories.deleted_at.isnull()]
        active_stories2=active_stories.drop(["image_link","video_link",\
        "description","status_flag","new_comment","schedule","created_at",\
        "deleted_at","updated_at","keyword_old","youtube_id","extra_keyword_count",\
        "admin_id"],axis=1)
        return active_stories2
    except:
        print("data base error")
        return None
def get_comments_cleaned(comment_csv_location):
    try:
        comments = pd.read_csv(comment_csv_location)
        admin_comments_idx = comments[comments.user_id==0].index
        comments_between_kids_idx = comments[comments.at_user_id==0].index
        comments_by_kids=comments.drop(admin_comments_idx).drop(comments_between_kids_idx).drop(["image","comment_id","at_user_id"],axis=1)
        return comments_by_kids
    except:
        print("data base error")
        return None

def get_clean_categories(categories_csv_location):
    try:
        categories = pd.read_csv(categories_csv_location)
        active_categories=categories[categories.deleted_at.isnull()]
        active_categories2=active_categories.drop(["thum_pic","status_flag","create_at","update_at","deleted_at"],axis=1)
        return active_categories2
    except:
        print("data base error")
        return None
def get_category_mapper(category_df):
    pick_cat = category_df[["id","name"]]
    cat_map=list(pick_cat.itertuples(index=None,name=None))
    return cat_map

def map_cat_id_with_cat(row_list_value,cat_map):
    category =""
    for row_value in row_list_value:
          for cat in cat_map:
            if int(row_value)==int(cat[0]):
                if len(category) > 0:
                    category += "|" + cat[1]
                else:
                    category += cat[1]
    return category
def map_category_id_with_categories(stories,cat):
         stories_df = stories.copy()
         categories_df = cat.copy()
         stories_df.category=stories_df.category.apply(ast.literal_eval)
         stories_df["cat_category"]=stories_df.category.apply(map_cat_id_with_cat,args=(get_category_mapper(categories_df),))
         return stories_df

def get_lang_mapper(languages_df):
    pick_lang = languages_df[["id","name","code"]]
    lang_map=list(pick_lang.itertuples(index=None,name=None))
    return lang_map

def map_lang_id_with_lang(row_list_value,lang_map):
    languages =""
    for row_value in row_list_value:
          for lang in lang_map:
            if int(row_value)==int(lang[0]):
                if len(lang) > 0:
                    languages += "|" + lang[1]
                else:
                    languages += lang[1]
    return languages
def map_lang_id_with_lang_code(row_list_value,lang_map):
    languages =""
    for row_value in row_list_value:
          for lang in lang_map:
            if int(row_value)==int(lang[0]):
                if len(lang) > 0:
                    languages += "|" + lang[2]
                else:
                    languages += lang[2]
    return languages
def map_lang_id_with_languages(parent_kids_df,lang_df):
         parent_kids_df = parent_kids_df.copy()
         languages_df = lang_df.copy()
         parent_kids_df.language_json = parent_kids_df.language_json.apply(ast.literal_eval)
         parent_kids_df["lang_str"]=parent_kids_df.language_json.apply(map_lang_id_with_lang,args=(get_lang_mapper(languages_df),))
         parent_kids_df["lang_code"]=parent_kids_df.language_json.apply(map_lang_id_with_lang_code,args=(get_lang_mapper(languages_df),))
         return parent_kids_df


def save_parent_kids_cleaned(path_to_save:str):
    parents = filter_users_as_parents('users.csv')
    parents.to_csv('parents.csv')
    parent_kids_df =cleanup_parents_kids_data('parents.csv','kids.csv')
    parent_kids_df.to_csv(path_to_save+"/"+"parent_kids.csv")

import datetime
def get_age_per_today(dob):
    date_format = '%Y-%m-%d'
    today = datetime.datetime.today()
    diff = today - dob
    years = diff.days // 365
    months = (diff.days - years *365) // 30/10
    return  years