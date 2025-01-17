from flask import Flask, render_template
import flask
#from flask.ext.sqlalchemy import SQLAlchemy
import numpy as np
import pandas as pd
import os
from sklearn.ensemble import ExtraTreesClassifier
import modify_data

#Model for Forest Identifying#
train = pd.read_csv('full_cols.csv')
train['Cover_Type'] = train['Cover_Type'].apply(str)
X_train = train.drop(['Cover_Type', 'Unnamed: 0'],1)
y_train = train['Cover_Type']
FOREST = ExtraTreesClassifier(n_estimators=200, random_state=42).fit(X_train, y_train)
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
    x = data['example']
    df = modify_data.modify_list(x,X_train.columns)
    result = FOREST.predict(df)
    #result = modify_data.modify_result(FOREST.predict(df))
    return result[0]

#testing offline
def result_off(data):
    result = modify_data.modify_result(FOREST.predict(data))
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
    app.run(debug=True)
