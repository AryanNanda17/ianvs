# Copyright 2021 The KubeEdge Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tensorflow as tf
import keras


# Input--conv2D--BN--ReLU--conv2D--BN--ReLU--Output
#      \                              /
#       ------------------------------
class BasicBlock(keras.layers.Layer):
    def __init__(self, filter_num, stride=1):
        super(BasicBlock, self).__init__()

        self.conv1 = keras.layers.Conv2D(
            filter_num, (3, 3), strides=stride, padding="same"
        )
        self.bn1 = keras.layers.BatchNormalization()
        self.relu = keras.layers.Activation("relu")

        self.conv2 = keras.layers.Conv2D(filter_num, (3, 3), strides=1, padding="same")
        self.bn2 = keras.layers.BatchNormalization()

        if stride != 1:
            self.downsample = keras.models.Sequential()
            self.downsample.add(keras.layers.Conv2D(filter_num, (1, 1), strides=stride))
        else:
            self.downsample = lambda x: x

    def call(self, inputs, training=None):
        # [b, h, w, c]
        out = self.conv1(inputs)
        out = self.bn1(out, training=training)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out, training=training)

        identity = self.downsample(inputs)

        output = keras.layers.add([out, identity])
        output = tf.nn.relu(output)

        return output


class ResNet(keras.Model):
    def __init__(self, layer_dims, num_classes=10):  # [2, 2, 2, 2]
        super(ResNet, self).__init__()
        self.layer_dims = layer_dims
        self.num_classes = num_classes

        self.stem = keras.models.Sequential(
            [
                keras.layers.Conv2D(64, (3, 3), strides=(1, 1)),
                keras.layers.BatchNormalization(),
                keras.layers.Activation("relu"),
                keras.layers.MaxPool2D(
                    pool_size=(2, 2), strides=(1, 1), padding="same"
                ),
            ]
        )

        self.layer1 = self.build_resblock(64, layer_dims[0])
        self.layer2 = self.build_resblock(128, layer_dims[1], stride=2)
        self.layer3 = self.build_resblock(256, layer_dims[2], stride=2)
        self.layer4 = self.build_resblock(512, layer_dims[3], stride=2)

        # output: [b, 512, h, w],
        self.avgpool = keras.layers.GlobalAveragePooling2D()
        # self.fc = keras.layers.Dense(num_classes)

    def call(self, inputs, training=None):
        x = self.stem(inputs, training=training)

        x = self.layer1(x, training=training)
        x = self.layer2(x, training=training)
        x = self.layer3(x, training=training)
        x = self.layer4(x, training=training)

        # [b, c]
        x = self.avgpool(x)
        return x

    def build_resblock(self, filter_num, blocks, stride=1):
        res_blocks = keras.models.Sequential()
        # may down sample
        res_blocks.add(BasicBlock(filter_num, stride))
        for _ in range(1, blocks):
            res_blocks.add(BasicBlock(filter_num, stride=1))
        return res_blocks

    def get_config(self):
        return {"layer_dims": self.layer_dims, "num_classes": self.num_classes}

    @classmethod
    def from_config(cls, config):
        return cls(**config)


def resnet10(num_classes: int):
    return ResNet([1, 1, 1, 1], num_classes)


def resnet18(num_classes: int):
    return ResNet([2, 2, 2, 2], num_classes)


def resnet34(num_classes: int):
    return ResNet([3, 4, 6, 3], num_classes)
