from autog.env_setup import Mouse_Control_Env
from autog.train_pytorch import train_mouse
import cv2
import torch
import numpy as np 
from torch import nn, optim
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 10 * 10, 500)
        self.fc2 = nn.Linear(500,500)
        self.fc3 = nn.Linear(500, 2)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(-1, 64 * 10 * 10)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

env = Mouse_Control_Env(mouse_control=True)

env.set_screen()

env.start_recording(t=200)
env.save_memory("sliter")

env.load_memory("sliter")

x_states, y_mouse = env.memory()

print(x_states.shape, y_mouse.shape)
print("Training")

train_mouse(env, Net(), x_states, y_mouse, epochs=30)

print("Play")
env.play()