from torch import nn

class MySTTnet(nn.Module):
    def __init__(self):
        super(MySTTnet, self).__init__()

        self.conv1 = nn.Conv2d(in_channels=1, out_channels=64, kernel_size=(3,5), padding=(1,0)) # (160, 100)
        self.act1  = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=(2,2), stride=(2,2)) # (160, 96)
        self.drop1 = nn.Dropout2d(p=0.2)

        self.conv2 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=(5,1), padding=(2,0)) # (80, 48)
        self.act2  = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=(4,2), stride=(4,2)) # (80, 48)
        self.drop2 = nn.Dropout2d(p=0.2)

        self.conv3 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=(7,1), padding=0) # (20, 24)
        self.act3  = nn.ReLU()
        self.conv4 = nn.Conv2d(in_channels=256, out_channels=512, kernel_size=(1,5), padding=0) # (14, 24)
        self.act4  = nn.ReLU()
        self.pool3 = nn.MaxPool2d(kernel_size=(14,20), stride=(14,20)) # (14, 20) --> (1, 1)
        self.drop3 = nn.Dropout2d(p=0.2)

        self.fc1   = nn.Linear(512, 128) # (1728,)
        self.act6  = nn.ReLU()

        self.fc2   = nn.Linear(128, 15) # (1728,)

    def forward(self, x):

        x = self.conv1(x)
        x = self.act1(x)
        x = self.pool1(x)
        x = self.drop1(x)

        x = self.conv2(x)
        x = self.act2(x)
        x = self.pool2(x)
        x = self.drop2(x)

        x = self.conv3(x)
        x = self.act3(x)
        x = self.conv4(x)
        x = self.act4(x)
        x = self.pool3(x)
        x = self.drop3(x)

        x = x.view(x.size(0), x.size(1) * x.size(2) * x.size(3))

        x = self.fc1(x)
        x = self.act6(x)
        x = self.fc2(x)

        return x