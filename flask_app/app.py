from flask import Flask, render_template, jsonify
import flask
#from flask.ext.sqlalchemy import SQLAlchemy
import numpy as np
import pandas as pd
import os
from catboost import Pool, CatBoostClassifier
import modify_data
import pickle

#Model for Forest Identifying#
cat_tree_model = pickle.load(open('cat_model.model', 'rb'))
# End of Forest Model

app = Flask(__name__)

@app.route('/')
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

@app.route('/result', methods=['POST'])
def result():
    '''
    When A POST request with json data is made to this uri,
    Read the example from the json, predict probability and
    send it with a response
    '''
    data = flask.request.json
    print (data)
    cols_to_use = ['Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology', 'Vertical_Distance_To_Hydrology', 'Horizontal_Distance_To_Roadways', 'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm', 'Horizontal_Distance_To_Fire_Points', 'Wilderness_Area', 'Soil_Type']
    x = [data['example']]
    data_df = pd.DataFrame(x, columns=cols_to_use)
    # these series of commands works great to get a single digit result. trying to get predict_proba now
    result = cat_tree_model.predict(data_df)
    result = result.flatten()
    result = [str(int(i)) for i in result]
    #print(result)
    keys, values = cat_tree_model.classes_, (cat_tree_model.predict_proba(data_df)*100).flatten()
    dictionary = modify_data.modify_result(result, keys, values)
    print(dictionary)
    return jsonify(dictionary)

#testing offline
def result_off(data):
    result = modify_data.modify_result(FOREST.predict(data))
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
    app.run(debug=True)
