# Metis_Bootcamp

Metis Datascience Bootcamp Repo Spring 2018

Project 3 was a classification project, I chose to investigate a Kaggle dataset to predict Forest Cover given cartographic variables. THis was a multiclass classification problem where I was trying to identify which of 7 tree cover types would be found in a given area. The provided training dataset had 15,000 data points and the test-set had more than 565,000 datapoints. While I tested a variety of models, I ended up finding best performance when using a gradient boosted random forest. The gradient boosted random forest best accounted for categorical features without requiring their conversion to dummy variables.

For this project, I also built and deployed a website to visualize the predictions made by the model. The application allowed users to select their own inputs and the visualization would provide real time predictions. The visualization was built using D3.js and deployed online through a flask webapp hosted on AWS. This is available online at www.travistrumbly.com/forest.html
