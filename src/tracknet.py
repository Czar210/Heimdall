import torch
import torch.nn as nn

class TrackNet(nn.Module):
    def __init__(self, in_channels=9, out_channels=256):
        super(TrackNet, self).__init__()
        # VGG Layers
        self.conv1 = nn.Sequential(nn.Conv2d(in_channels, 64, 3, 1, 1), nn.ReLU(), nn.BatchNorm2d(64), nn.Conv2d(64, 64, 3, 1, 1), nn.ReLU(), nn.BatchNorm2d(64))
        self.pool1 = nn.MaxPool2d(2, stride=2)
        self.conv2 = nn.Sequential(nn.Conv2d(64, 128, 3, 1, 1), nn.ReLU(), nn.BatchNorm2d(128), nn.Conv2d(128, 128, 3, 1, 1), nn.ReLU(), nn.BatchNorm2d(128))
        self.pool2 = nn.MaxPool2d(2, stride=2)
        self.conv3 = nn.Sequential(nn.Conv2d(128, 256, 3, 1, 1), nn.ReLU(), nn.BatchNorm2d(256), nn.Conv2d(256, 256, 3, 1, 1), nn.ReLU(), nn.BatchNorm2d(256), nn.Conv2d(256, 256, 3, 1, 1), nn.ReLU(), nn.BatchNorm2d(256))
        self.pool3 = nn.MaxPool2d(2, stride=2)
        # Bottleneck
        self.conv4 = nn.Sequential(nn.Conv2d(256, 512, 3, 1, 1), nn.ReLU(), nn.BatchNorm2d(512), nn.Conv2d(512, 512, 3, 1, 1), nn.ReLU(), nn.BatchNorm2d(512), nn.Conv2d(512, 512, 3, 1, 1), nn.ReLU(), nn.BatchNorm2d(512))
        # Upsampling
        self.up5 = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        self.conv5 = nn.Sequential(nn.Conv2d(512, 256, 3, 1, 1), nn.ReLU(), nn.BatchNorm2d(256), nn.Conv2d(256, 256, 3, 1, 1), nn.ReLU(), nn.BatchNorm2d(256), nn.Conv2d(256, 256, 3, 1, 1), nn.ReLU(), nn.BatchNorm2d(256))
        self.up6 = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        self.conv6 = nn.Sequential(nn.Conv2d(256, 128, 3, 1, 1), nn.ReLU(), nn.BatchNorm2d(128), nn.Conv2d(128, 128, 3, 1, 1), nn.ReLU(), nn.BatchNorm2d(128))
        self.up7 = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        self.conv7 = nn.Sequential(nn.Conv2d(128, 64, 3, 1, 1), nn.ReLU(), nn.BatchNorm2d(64), nn.Conv2d(64, 64, 3, 1, 1), nn.ReLU(), nn.BatchNorm2d(64), nn.Conv2d(64, 1, 1, 1, 0), nn.Sigmoid())

    def forward(self, x):
        x = self.conv1(x)
        x = self.pool1(x)
        x = self.conv2(x)
        x = self.pool2(x)
        x = self.conv3(x)
        x = self.pool3(x)
        x = self.conv4(x)
        x = self.up5(x)
        x = self.conv5(x)
        x = self.up6(x)
        x = self.conv6(x)
        x = self.up7(x)
        x = self.conv7(x)
        return x
