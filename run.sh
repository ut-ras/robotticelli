cd src

# Stopping old pigpiod process, if they exist and reinitializing them
pigpiod &

# Execute the entry point script
python2 main.py
