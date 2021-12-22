# EasySensirion

Easy interface for the [temperature and humidity sensors of Sensirion](https://www.sensirion.com/en/environmental-sensors/humidity-sensors/) from Python.

## Installation

```
pip3 install git+https://github.com/SengerM/EasySensirion
```
or clone in `my_favourite_directory` and then `pip3 install -e my_favourite_directory`.

### Additional requirements

You have to [install also the drivers from Sensirion](https://sensirion.github.io/python-i2c-sht/installation.html)using 
```
pip3 install sensirion-i2c-sht
```
You also have to install the [SensorBridge](https://sensirion.github.io/python-i2c-sht/quickstart.html) module with 
```
pip3 install sensirion-shdlc-sensorbridge
```

## Usage

```Python
import EasySensirion
import time

sensor = EasySensirion.SensirionSensor()
while True:
	print(f'Temperature: {sensor.temperature:.2f} °C | Humidity: {sensor.humidity:.2f} %RH')
	time.sleep(1)
```
