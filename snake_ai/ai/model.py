import torch
import torch.nn as nn


class QNet(torch.nn.Module):
    def __init__(self) -> None:
        super(QNet, self).__init__()
        self.input_layer = nn.Linear(16, 256)
        self.hidden_layer = nn.Linear(256, 256)
        self.output_layer = nn.Linear(256, 4)
    
    def forward(self, data) -> int:
        data = self.input_layer(data)
        data = self.hidden_layer(data)
        return self.output_layer(data)
