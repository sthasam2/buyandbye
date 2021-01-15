import pandas as pd
import sqlite3 as sq
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

# global conn, df, tf, tfidf_matrix, cosine_similarities, results
"""connecting the database with connect"""
conn = sq.connect("db.sqlite3")

"""creating a pandas data frame"""
df = pd.read_sql_query("select * from product_item;", conn)
user_df = pd.read_sql_query("select * from activity_activity;", conn)

"""creating a tfid vector"""
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3),
                     min_df=0, stop_words='english')

"""creating a matrix from the tfidf vector"""
tfidf_matrix = tf.fit_transform(df['content'])

"""finding the cosine similarities for all products with other products"""
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

"""declaring results"""
results = {}

for idx, row in df.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
    similar_items = [(cosine_similarities[idx][i], df['id'][i])
                     for i in similar_indices]
    results[row['id']] = similar_items[1:]


def calculate_similarity():
    print("init similarity calculator")
    """connecting the database with connect"""
    conn = sq.connect("db.sqlite3")

    """creating a pandas data frame"""
    global df
    df = pd.read_sql_query("select * from product_item;", conn)

    """creating a tfid vector"""
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3),
                         min_df=0, stop_words='english')

    """creating a matrix from the tfidf vector"""
    tfidf_matrix = tf.fit_transform(df['content'])

    """finding the cosine similarities for all products with other products"""
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    """declaring results"""
    global results
    results = {}

    for idx, row in df.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
        similar_items = [(cosine_similarities[idx][i], df['id'][i])
                         for i in similar_indices]
        results[row['id']] = similar_items[1:]

    print("calculation ended")


def item(id):
    return df.loc[df['id'] == id]['title'].tolist()[0].split(' - ')[0]


def recommend(item_id, num):
    """ recommends num items similar to item_id"""
    recs = results[item_id][:num]
    product_id = []
    for rd in recs:
        """iteraring each result obtained from cosine similarity and assigning them from tuple"""
        product_id.append(rd[1])
    print("detail")
    return product_id


def user_recommend(req_user_id):
    user_df.user_id = req_user_id  # filtering based on the user id
    user_df.verb = "Viewed item"    # filtering to 'viewed item' only
    mode = user_df.target_id.mode()  # getting the most repeated item
    mode_id = mode[0]  # extracting the id of mode from the mode table
    return recommend(mode_id, 20)
