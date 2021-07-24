import uvicorn
from fastapi import FastAPI, File, UploadFile
from typing import List
import pandas as pd
import numpy as np
import sqlite3
from io import StringIO
import sklearn
import pickle



# joblib to load serialized ML model
# joblib.load()

# init app
app = FastAPI()

# Routes
@app.get('/')
async def index():
    return {"Roger":"Welcome !"}

# sqlite functions
def create_sqlite_con(db_file):
     conn = sqlite3.connect(db_file)
     return conn

def insert_classified_results(conn, new_input):
    sql = ''' INSERT INTO music(trackID, title, genre)
              VALUES{} '''.format(new_input)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid

def delete_duplicates(conn):
    sql = '''DELETE FROM music
             WHERE rowid NOT IN (
             SELECT MIN(rowid) 
             FROM music 
             GROUP BY trackID,title )'''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid

def get_genre_titles(conn, genre_name):
    sql = ''' SELECT title FROM music
              WHERE genre = '{}' '''.format(genre_name)
    cur = conn.cursor()
    cur.execute(sql)
    results_list = []
    for rows in cur.execute(sql):
        results_list.append(list(rows)[0])
    return results_list

def get_classified_genres(conn):
    sql = ''' SELECT * FROM music '''
    cur = conn.cursor()
    results_list = []
    for rows in cur.execute(sql):
        t_list = list(rows)
        if t_list[0] == None:
            results_list.append(t_list[2])
    
    return results_list


# Load trained scaler
with open("models/final_scaler.p", "rb") as f:
    data_scaler = pickle.load(f)

# Load trained ML Classifier model
with open("models/final_model.p", "rb") as f:
    ml_classifier = pickle.load(f)


# Load selected features
with open("models/selected_features.p", "rb") as f:
    selected_features = pickle.load(f)


# To get a list of titles to the provided genre
@app.get("/titles/{name}")
async def get_titles_of_selected_genre(name: str):
    conn = create_sqlite_con('music.db')
    results_list = get_genre_titles(conn, name)
    conn.close()
    return {"Provided genre": [name], 
            "Number of titles under the genre": [len(results_list)],
            "Titles under the genre": results_list}


# To get a list of classified genres
@app.get("/classifiedGenres/")
async def list_of_classified_genres():
    conn = create_sqlite_con('music.db')
    results_list = get_classified_genres(conn)
    conn.close()
    
    return {"Number of classified genres":[len(results_list)],"List of classified genres": results_list}


@app.post("/predict/")
async def predict(files: List[UploadFile] = File(...)):
    df_input = pd.read_csv(StringIO(str(files[0].file.read(), 'utf-8')), encoding='utf-8')

    selected_features_temp = selected_features.copy()
    selected_features_temp.remove('pop_tags')
    selected_features_temp = selected_features_temp + ['tags']
    # Check if current input dataframe has all required selected features. If not, stop the process
    try:
        check_columns = df_input[selected_features_temp]
        check_columns = None
    except KeyError:
        return {"Error": "Uploaded file is missing some important feature columns"}

    df_input.dropna(subset=selected_features_temp, axis=0, how='any', inplace=True)

    # Count presence of top 5 frequent tags related to 'pop' genre
    df_input['pop_tags'] = 0
    df_input['pop_tags'] = df_input['pop_tags'] + df_input.tags.apply(lambda x: np.where('de' in x.replace(" ","").split(","),1,0))
    df_input['pop_tags'] = df_input['pop_tags'] + df_input.tags.apply(lambda x: np.where('que' in x.replace(" ","").split(","),1,0))
    df_input['pop_tags'] = df_input['pop_tags'] + df_input.tags.apply(lambda x: np.where('y' in x.replace(" ","").split(","),1,0))
    df_input['pop_tags'] = df_input['pop_tags'] + df_input.tags.apply(lambda x: np.where('el' in x.replace(" ","").split(","),1,0))
    df_input['pop_tags'] = df_input['pop_tags'] + df_input.tags.apply(lambda x: np.where('la' in x.replace(" ","").split(","),1,0))

    df_input = df_input[['trackID','title']+selected_features]

    # Normalize numeric features through trained scaler
    scaled_features_test = data_scaler.transform(df_input[selected_features])
    scaled_feature_names = ['scaled_'+x for x in selected_features]
    scaled_features_test = pd.DataFrame(scaled_features_test, columns=scaled_feature_names)

    df_input.reset_index(drop=True, inplace=True)
    df_input.drop(selected_features, axis=1, inplace=True)
    df_input = pd.concat([df_input, scaled_features_test], axis=1)

    # Predict with data input
    test_preds = ml_classifier.predict(df_input[scaled_feature_names])

    # Tabulate results
    test_preds = pd.DataFrame({'trackID':df_input.trackID,
                            'title':df_input.title,
                            'genre':test_preds})

    # Persists the results and titles into sqlite DB
    conn = create_sqlite_con('music.db')
    preds_list_tuples = list(test_preds.to_records())
    capture_duplicates = []
    for ittr in range(len(preds_list_tuples)):
        t_new_insert = preds_list_tuples[ittr]
        t_new_insert = tuple(list(t_new_insert)[1:])
        try:
            insert_classified_results(conn, t_new_insert)
        except:
            return {'Error': 'Attempt to insert duplicate records'}

    delete_duplicates(conn)
    conn.close()
    
    return {'Number of new classfications computed and added to database': test_preds.shape[0]}




if __name__ == '__main__':
    uvicorn.run(app,host="0.0.0.0",port=8000)