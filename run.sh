cd ./src

cp conf.py ./hardware/motor/

if pgrep -x "python" > /dev/null; then
  killall python
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

python main.py
