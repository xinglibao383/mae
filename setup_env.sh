#!/bin/bash

conda create --name mae python=3.8 -y
conda activate mae

conda install pytorch==1.13.0 torchvision==0.14.0 torchaudio==0.13.0 pytorch-cuda=11.7 -c pytorch -c nvidia

pip install timm==0.3.2
pip install tensorboard==2.4.0
pip install protobuf==3.20.3
pip install numpy==1.19.5
pip install scipy

pip install matplotlib==3.3.4
pip install matplotlib-inline

pip install jupyter