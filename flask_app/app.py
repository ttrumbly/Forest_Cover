from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import numpy as np
import pandas as pd
import os

#Model for Forest Identifying#
#put stuff here about modeling a forest#
train = pd.read_csv('train 3.csv')
train['Id'] = train['Id'].apply(str)
train['Cover_Type'] = train['Cover_Type'].apply(str)
X_train = train.drop(['Cover_Type', 'Id', 'Dist_To_Water'],1)
y_train = train['Cover_Type']
FOREST = ExtraTreesClassifier(n_estimators=200, random_state=42).fit(X_train, y_train)



app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

def viz_page():
    """
    Visualization page for the app
    """
    with open('visualization.html', 'r') as viz_file:
        return viz_file.read()

@app.route('/score', methods=['POST'])
def score():
    '''
    Make a prediction and return that as a response
    '''
    data = flask.request.json
    x = np.matrix(data['example'])
    score = FOREST.predict_proba(x)

#app.config.from_object(os.environ['APP_SETTINGS'])
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

#from models import Result

@app.route('/<name>')
def hello_name(name):
    return 'Hello {}!'.format(name)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.run(debug=True)
