#!/bin/bash

killall -w -q SARndbox

timeout 1.0s KinectUtil reset all

run="Run the sandbox!"
calibrate="Calibrate!"
quit="Quit"

result=$(zenity --question --title="AR Sandbox" --text "What would you like to do?" --ok-label="$run" --extra-button="$calibrate" --cancel-label="$quit")

echo $result
if [[ $result == $calibrate ]]; then
    /home/user/arsandbox/SARndbox/bin/CalibrateProjector
#elif [[ $result == $run ]]; then
else
#    /home/user/arsandbox/SARndbox/bin/SARndbox -vruiVerbose -fpv -uhm -s 100 -nas 30 -ws 1.0 200 -us -rs 0.1  -rs 1 -evr -0.005 -wo 2.0 -ncl -ucl 0.75 -uhs
    python3 /home/user/Desktop/lahs-sarndbox/run-sandbox.py --fast
fi
