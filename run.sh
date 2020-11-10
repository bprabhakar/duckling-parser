#!/bin/bash

# Start the duckling server
cd /home/duckling &&
stack exec duckling-example-exe > /dev/null 2>&1 &
# sleep 5 && # making sure the duckling server is up

# Start the flask job
cd /home/aarzoo-mvp &&
python duckling_app.py > /dev/null 2>&1 &