import torch
import torch.nn as nn


class ConvBlock(nn.Module):
    """Convolution + LeakyReLU block used by YOLOv1."""

    def __init__(self, in_channels, out_channels, kernel_size, stride, padding):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(
                in_channels,
                out_channels,
                kernel_size=kernel_size,
                stride=stride,
                padding=padding,
            ),
            nn.LeakyReLU(0.1, inplace=True),
        )

    def forward(self, x):
        return self.block(x)


class YOLOv1(nn.Module):
    """
    YOLOv1 model.

    For VOC-style detection, the default output shape is:
        [batch_size, 7, 7, 30]

    30 = 20 classes + 2 boxes * (x, y, w, h, confidence)
    """

    def __init__(self, split_size=7, num_boxes=2, num_classes=20):
        super().__init__()
        self.split_size = split_size
        self.num_boxes = num_boxes
        self.num_classes = num_classes

        self.backbone = nn.Sequential(
            ConvBlock(3, 64, kernel_size=7, stride=2, padding=3),
            nn.MaxPool2d(kernel_size=2, stride=2),
            ConvBlock(64, 192, kernel_size=3, stride=1, padding=1),
            nn.MaxPool2d(kernel_size=2, stride=2),
            ConvBlock(192, 128, kernel_size=1, stride=1, padding=0),
            ConvBlock(128, 256, kernel_size=3, stride=1, padding=1),
            ConvBlock(256, 256, kernel_size=1, stride=1, padding=0),
            ConvBlock(256, 512, kernel_size=3, stride=1, padding=1),
            nn.MaxPool2d(kernel_size=2, stride=2),
            ConvBlock(512, 256, kernel_size=1, stride=1, padding=0),
            ConvBlock(256, 512, kernel_size=3, stride=1, padding=1),
            ConvBlock(512, 256, kernel_size=1, stride=1, padding=0),
            ConvBlock(256, 512, kernel_size=3, stride=1, padding=1),
            ConvBlock(512, 256, kernel_size=1, stride=1, padding=0),
            ConvBlock(256, 512, kernel_size=3, stride=1, padding=1),
            ConvBlock(512, 256, kernel_size=1, stride=1, padding=0),
            ConvBlock(256, 512, kernel_size=3, stride=1, padding=1),
            ConvBlock(512, 512, kernel_size=1, stride=1, padding=0),
            ConvBlock(512, 1024, kernel_size=3, stride=1, padding=1),
            nn.MaxPool2d(kernel_size=2, stride=2),
            ConvBlock(1024, 512, kernel_size=1, stride=1, padding=0),
            ConvBlock(512, 1024, kernel_size=3, stride=1, padding=1),
            ConvBlock(1024, 512, kernel_size=1, stride=1, padding=0),
            ConvBlock(512, 1024, kernel_size=3, stride=1, padding=1),
            ConvBlock(1024, 1024, kernel_size=3, stride=1, padding=1),
            ConvBlock(1024, 1024, kernel_size=3, stride=2, padding=1),
            ConvBlock(1024, 1024, kernel_size=3, stride=1, padding=1),
            ConvBlock(1024, 1024, kernel_size=3, stride=1, padding=1),
        )

        self.detector = nn.Sequential(
            nn.Flatten(),
            nn.Linear(1024 * split_size * split_size, 4096),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Dropout(p=0.5),
            nn.Linear(
                4096,
                split_size * split_size * (num_classes + num_boxes * 5),
            ),
        )

    def forward(self, x):
        x = self.backbone(x)
        x = self.detector(x)
        x = x.view(
            -1,
            self.split_size,
            self.split_size,
            self.num_classes + self.num_boxes * 5,
        )
        return x


if __name__ == "__main__":
    model = YOLOv1(split_size=7, num_boxes=2, num_classes=20)
    inputs = torch.randn(2, 3, 448, 448)
    outputs = model(inputs)
    print(outputs.shape)
