import torch
import torch.nn as nn

class Network(nn.Module):

    def __init__(self):
        super(Network, self).__init__()
        self.inputSize = 2
        self.hidden1Size = 8
        self.hidden2Size = 8
        self.outputSize = 1

        # creates 2 layers with weights W and biases b in the form y=Wx+b
        self.hidden1 = nn.Linear(self.inputSize, self.hidden1Size)
        self.hidden2 = nn.Linear(self.hidden1Size, self.hidden2Size)
        self.output = nn.Linear(self.hidden2Size, self.outputSize)

        # initialize the weights and biases
        nn.init.xavier_uniform_(self.hidden1.weight)
        nn.init.zeros_(self.hidden1.bias)
        nn.init.xavier_uniform_(self.hidden2.weight)
        nn.init.zeros_(self.hidden2.bias)
        nn.init.xavier_uniform_(self.output.weight)
        nn.init.zeros_(self.output.bias)

    # given an input, run the nn to produce and output
    def forward(self, x):
        x = torch.tanh(self.hidden1(x))
        x = torch.tanh(self.hidden2(x))
        x = torch.sigmoid(self.output(x))
        return x

