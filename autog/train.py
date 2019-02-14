import torch
import numpy as np 


def train(model, environment, epochs = 20, lr = 0.01, batch_size = 32):

    criterion = nn.NLLLoss()
    optimizer = optim.Adam(model.parameters(), lr)

    for e in range(epochs):
        running_loss = 0
        for images, labels in trainloader:
            log_ps = model(images)
            loss = criterion(log_ps, labels)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
        else:
            print(f"Training loss: {running_loss/len(trainloader)}")

