cd src

if pgrep -x "python2" > /dev/null; then
  killall python2
fi
if pgrep -x "pigpiod" > /dev/null; then
  killall pigpiod
fi
python2 main.py
