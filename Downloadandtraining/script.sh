#!/bin/bash
echo "******************************Download Images Process******************************"
python3 main.py

echo "Successful Download"

echo "******************************Training Process******************************"

python3 train.py
echo "Successful Training"
