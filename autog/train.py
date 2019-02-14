import torch
import numpy as np 
from torch import nn, optim
import torch.nn.functional as F



def train_mouse(env, model, states, mouse, epochs = 10, lr= 0.01, batch_size = 32):
    
    env.mouse_model = model
    criterion = nn.MSELoss()
    optimizer = optim.Adam(env.mouse_model.parameters(), lr)
    states = np.transpose(states, (0, 3, 1, 2))
    states = torch.from_numpy(states).float()
    mouse = torch.from_numpy(mouse).float()

    for e in range(epochs):
        print(e)
        permutation = torch.randperm(states.size()[0])
        for i in range(0,states.size()[0], batch_size):
            optimizer.zero_grad()
            indices = permutation[i:i+batch_size]
            batch_x, batch_y = states[indices], mouse[indices]

            outputs = env.mouse_model.forward(batch_x)
            loss = criterion(outputs,batch_y)

            loss.backward()
            optimizer.step()
    
