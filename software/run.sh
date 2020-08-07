#!/bin/bash

cd ui
make clean
make
cd ..
python3 main.py
