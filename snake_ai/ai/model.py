import torch.nn as nn
import torch.nn.functional as F


class QNet(nn.Module):
    def __init__(self):
        super(QNet, self).__init__()
        self.input_layer = nn.Linear(10, 128)
        self.hidden1 = nn.Linear(128, 64)
        self.output_layer = nn.Linear(64, 3)
    
    def forward(self, data):
        data = F.relu(self.input_layer(data))
        data = F.relu(self.hidden1(data))
        return self.output_layer(data)
        data = F.relu(self.hidden2(data))
        return self.output_layer(data)
