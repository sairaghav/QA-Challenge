# QA Streaming ML Pipeline Challenge - Solution

To use this solution, use the docker-compose.yml file to start the frontend and backend servers (the servers will be hosted locally). Once the servers are running, go to http://localhost:3000/ to view the app.

To run the models, click on the "update" button. This button simulates new data added to the models after it has been collected by an external entity (an equivalent way to do this would to be to call the api after a designated time - say, 1 second). Note that you may have to wait for a few seconds before the UI updates.

I treated the assignment as if /api/v1/data was an external API that I needed to call within my application. In order to do so, I created my own route /api/v1/run_script to run the ingestion script, which runs on the backend server. The backend server then queries /api/v1/data to get the necessary data.

The ingestion script is defined in ingestion_script.py and it gets the next 100 pages of results every time a call is made to /api/v1/run_script. This data is then fed into the machine learning models and the appropriate model indicators are returned via JSON.

## ML Models
For the classification model, I chose to construct a neural network that functions as a binary classifier. The network takes two parameters - competence and network ability - and then predicts whether or not that user is promoted. The output node returns a value in the range [0,1], which can be interpreted as the probability that a user is promoted. The tanh function is used as the activation function since it tends to work well for binary classifiers. Stochastic gradient descent is used to train the network.

In order to determine how well the model is functioning, the data is randomly split into a training set (80\% of the data) and a validation set (20\% of the data). The model is trained on the training set. The trained model is then run on the validation set to determine how well it predicts the outcomes from the validation set. This information is displayed to the user each time the model is updated with new data.

For the regression model, I started by running different simulations with a linear regression model to determine the strength of the relationship between competence and network ability and promoted and network ability (note that, by the nature of how id's are created, there should be no correlation between id's and network ability). When running the models, the correlation coefficient r^2 between competence and network ability was never above 10^-3, which indicates almost no correlation between the two variables. Therefore, a linear regression model was chosen where promoted is the independent variable and network ability is the dependent variable. The correlation coefficient is shown in the graph, which indicates how strongly the two variables are related.

## Improvements
Note that there are certain features of this solution that could be improved. 

### UI Improvements
Ideally, it would be good to disable the "Update" button when the app is refreshing, or perhaps remove the button altogether and replace it with a call to the api that happens every second and automatically refreshes the model. Also, the design of the UI could be improved to be more aesthetic.

### ML Model Improvements
For the classification model, certain hyperparameters may be able to be adjusted in order to be able to increase the accuracy of the model. Also, experimenting with the method of training the model (how many batches and epochs to use, etc) could help improve the results.

More could be done to improve the regression model. A linear regression model is often over-simplistic and assumes a linear relationship between the independent and dependent variables, which is not strongly present in the data. Also, the preliminary results about the correlation between competence and network ability, while sensible from a qualitative point of view, may still be important to model, perhaps using a technique such as Lasso Regression.

For all the models, the way in which the data is ingested could also be improved. For efficiency reasons, the model only ingests a small amount of data at a time. Running these models on the full dataset should greatly increase their accuracy.