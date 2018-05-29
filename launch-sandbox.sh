#!/bin/bash

killall -w -q SARndbox

timeout 1.0s KinectUtil reset all

python3 /home/user/Desktop/lahs-sarndbox/run-sandbox.py --gui