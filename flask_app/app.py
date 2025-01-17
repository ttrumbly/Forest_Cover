from flask import Flask, render_template, jsonify
import flask
#from flask.ext.sqlalchemy import SQLAlchemy
import numpy as np
import pandas as pd
import os
from catboost import Pool, CatBoostClassifier
import modify_data
import pickle
from sqlalchemy import create_engine
import json

#Model for Forest Identifying#
#loaded from a file. I can update this model in my jupyter notebook and reload it here as needed (as ground truth increases)
cat_tree_model = pickle.load(open('cat_model.model', 'rb'))
# End of Forest Model
#create a link to my sql server for sql interactions
cnx = create_engine('postgresql://ubuntu@18.236.157.230:5432/ubuntu')
app = Flask(__name__)

#set the homepage
@app.route('/')
def home_page():
    """
    Home page for the app
    """
    with open('index.html', 'r') as home_page:
        return home_page.read()

#make it so the page can route to index.html as well as /
@app.route('/index.html')
def index_page():
    """
    Home page for the app
    """
    with open('index.html', 'r') as index_page:
        return index_page.read()

#set the visulization page
@app.route('/visualization.html')
def viz_page():
    """
    Visualization page for the app
    """
    with open('visualization.html', 'r') as viz_file:
        return viz_file.read()

@app.route('/test.html')
def test_page():
    with open('test.html', 'r') as test_file:
        return test_file.read()

@app.route('/info.html')
def info_page():
    with open('info.html', 'r') as info_file:
        return info_file.read()

#update the prediction by running it through my model
@app.route('/result', methods=['POST'])
def result():
    '''
    When A POST request with json data is made to this uri,
    Read the example from the json, predict probability and
    send it with a response
    '''
    data = flask.request.json
    #print (data) useful for testing
    cols_to_use = ['Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology', 'Vertical_Distance_To_Hydrology', 'Horizontal_Distance_To_Roadways', 'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm', 'Horizontal_Distance_To_Fire_Points', 'Wilderness_Area', 'Soil_Type']
    x = [data['example']]
    data_df = pd.DataFrame(x, columns=cols_to_use)
    # these series of commands works great to get a single digit result. trying to get predict_proba now
    result = cat_tree_model.predict(data_df)
    result = result.flatten()
    result = [str(int(i)) for i in result]
    #print(result) useful for testing
    keys, values = cat_tree_model.classes_, (cat_tree_model.predict_proba(data_df)*100).flatten()
    dictionary = modify_data.modify_result(result, keys, values)
    #print(dictionary) useful for testing
    return jsonify(dictionary)

#employee landing page to input new datapoints
@app.route('/employee.html')
def employee_page():
    with open('employee.html', 'r') as employee_page:
        return employee_page.read()

#redirect to success website after successful sql load
@app.route('/success.html')
def success():
    with open('success.html', 'r') as success:
        return success.read()

#load new data into the sql database, I use a query to find the last item and set my id to 1 more than that so as to not overwrite any existing data.
@app.route('/add', methods=['POST'])
def add():
    '''
    When A POST request with json data is made to this uri,
    Read the example from the json, and upload it to the sql server
    '''
    data = flask.request.json
    cols_to_use2 = ['elevation', 'aspect', 'slope', 'horizontal_distance_to_hydrology', 'vertical_distance_to_hydrology', 'horizontal_distance_to_roadways', 'hillshade_9am', 'hillshade_noon', 'hillshade_3pm', 'horizontal_distance_to_fire_points', 'cover_type', 'wilderness_area', 'soil_type']
    y = [data['example']]
    data_df = pd.DataFrame(y, columns = cols_to_use2)
    int_id = pd.read_sql_query('''SELECT id FROM forest_cover ORDER BY id desc LIMIT 1''',cnx)
    max_id = int_id['id'][0]
    data_df['id'] = max_id+1
    data_df.to_sql('forest_cover',cnx, if_exists='append', index=False)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

#testing offline was able to call this function from other python files without being online for some basic testing.
def result_off(data):
    result = modify_data.modify_result(FOREST.predict(data))
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
    app.run(debug=True)
