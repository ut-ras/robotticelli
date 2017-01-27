apt-get install python
apt-get install python-pip
apt-get install python-numpy
apt-get install python-scipy
apt-get install python-sklearn
pip install flask
pip install RPIO

if [ ! -d ./modules ]; then
	mkdir ./modules
fi

cd ./modules
git clone https://www.github.com/guyc/py-gaugette.git

