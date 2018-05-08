cd ~/arsandbox/SARndbox/

# KinectUtil reset all
timeout --signal=SIGINT 2 KinectUtil reset all


# ./bin/SARndbox -fpv -vruiVerbose -ws 0.8 10 -uhm -us
# ./bin/SARndbox -fpv -vruiVerbose -ws 1 10 -rs 5 -uhs -us -evr 0.005 -uhm
# ./bin/SARndbox -fpv -vruiVerbose -ws 1 10 -rs 5 -uhs -us -evr 0.005
# ./bin/SARndbox -fpv -vruiVerbose -ws 1 10 -rs 5 -uhs -us -evr 0.005 -ncl -uhm
# ./bin/SARndbox -fpv -vruiVerbose -ws 0 0 -rs 5 -uhs -us -evr 0.005 -ncl -uhm -rer 10 100


# ./bin/SARndbox -vruiVerbose -fpv -uhm -er 0 -100


# Run SARndbox simulation!
./bin/SARndbox \
\
# OPTIONS
\
# Verbose Mode
-vruiVerbose \
\
# Use the calibration file (important!)
-fpv 
\
# Enable elevation color mapping (-nhm to disable)
-uhm \
\
# Scale factor <scale factor>
-s 100.0 \ # Default: 100.0
\
# Elevation Range <min elevation> <max elevation>
-er -1000 0 \
\
# Height Map Base Plane <x> <y> <z> <offset> - sets an explicit base plane equation to use for height color mapping
# -hmp 0 0 -100 -1000 \
\
# <num averaging slots> - Sets the number of averaging slots in the frame filter; latency is <num averaging slots> * 1/30 s
#-nas 30 \ # Default: 30
\
# Water speed
#-ws 0.8 10 \
\
# 
#-us

