import numpy as np
import requests
import torch
import torch.nn as nn
import torch.optim as optim

from collections import OrderedDict
from neural_network import Network
from sklearn.linear_model import LinearRegression

# set global parameters to keep track of the state of the app
page = 0
increment = 100

# parameter for the classification algorithm
net = Network()

# parameters for the regression algorithm
indep = []
indep_out = [] # temp fix - problem rending JSON for numpy arrays
depend = []

# linear regression model
# returns the r^2 value to measure the fit of the line
def linear_regression():
    reg = LinearRegression().fit(indep, np.array(depend))
    return reg.score(indep, depend)

# calculates the accuracy of the model on the given dataset
def validate_model(model, dataloader):
    total = 0.0
    num_correct = 0.0
    for data in dataloader:
        inputs, labels = data
        outputs = model(inputs)
        num_correct = num_correct + ((torch.round(outputs) - labels) == 0).sum().item()
        total = total + labels.numel()

    accuracy = 100 * num_correct / total
    return accuracy

# trains the nn based on an input dataset and a target dataset
# returns the accuracy of the model
def train_neural_network(nn_input, nn_target):

    # split the dataset - use 80% for training and 20% for validation
    dataset = torch.utils.data.TensorDataset(torch.FloatTensor(nn_input), torch.FloatTensor(nn_target))
    train_size = int(0.8 * len(dataset))
    validate_size = len(dataset) - train_size
    train_dataset, validate_dataset = torch.utils.data.random_split(dataset, [train_size, validate_size])
    dataloaders = OrderedDict([
        ('train', torch.utils.data.DataLoader(train_dataset, batch_size=increment * 10, shuffle=True)),
        ('validate', torch.utils.data.DataLoader(validate_dataset, batch_size=increment * 10, shuffle=True))
    ])

    # train the neural network using the provided loss and optimizer functions
    alpha = .1
    loss_funct = nn.BCELoss()
    optimizer = optim.SGD(net.parameters(), lr=alpha)
    dataloader = dataloaders['train'] # use the training data
    for epoch in range(100):  # loop over the dataset for the given number of epochs
        for ii, (inputs, labels) in enumerate(dataloader):

            # zero the parameter gradients
            optimizer.zero_grad()

            # run the inputs through the nn to get the nn output and compute the loss function
            outputs = net(inputs)
            loss = loss_funct(outputs, labels)

            # update the parameters of the nn
            loss.backward()
            optimizer.step()

    accuracy = validate_model(net, dataloaders['validate'])
    return accuracy

# run the script to ingest data from the api
def run_ingestion_script():

    # set parameters
    global page     # keeps track of the current page
    nn_input = []   # stores the input values used to train the nn
    nn_target = []  # stores the target values used to train the nn

    #  start from the last loaded page and pull data from all the pages in the range [page, page + increment)
    for i in range(page, page + increment):
        request = requests.get('http://localhost:5000/api/v1/data?page=' + str(i)).json() # get data from the api
        for data_point in request:  # iterate through the data received by the request

            # pull values from the json data
            data_competence = data_point['competence']
            data_network_ability = data_point['network_ability']
            data_promoted = data_point['promoted']

            # add the appropriate values to temp variables to be used when passing the data to the appropriate model
            nn_input.append([data_competence, data_network_ability])
            nn_target.append([data_promoted])
            indep.append([data_promoted])
            indep_out.append(data_promoted)
            depend.append(data_network_ability)

    page = page + increment      # remember the last page left off on for the next call

    # run the two ML models
    accuracy = train_neural_network(nn_input, nn_target)
    r2 = linear_regression()

    # store the results in a dictionary to be converted to JSON
    results = [{
    "accuracy": accuracy,
    "num_records_processed": page * 10,
    "indep": indep_out,
    "depend": depend,
    "r2": r2
    }]
    return results