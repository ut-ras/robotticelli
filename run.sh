cd src

if pgrep -x "python2" > /dev/null; then
  killall python2
fi
if pgrep -x "pigpiod" > /dev/null; then
  killall pigpiod
fi
if pgrep -x "celery" > /dev/null; then
  killall celery
fi
if pgrep -x "redis" > /dev/null; then
  exec redis-server
fi

python2 main.py
