from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection
from sensirion_shdlc_sensorbridge import SensorBridgePort, SensorBridgeShdlcDevice, SensorBridgeI2cProxy
from sensirion_i2c_driver import I2cConnection
from sensirion_i2c_sht.sht3x import Sht3xI2cDevice
from threading import RLock

# Code from Sensirion https://github.com/Sensirion/python-i2c-sht

class SensirionSensor:
	"""
	This class was created to wrap and ease the use of the example in this link: https://sensirion.github.io/python-i2c-sht/quickstart.html. It is to be used to control one SHT3x [1] sensor connected to a SEK Sensor Bridge [2]. For this to work, connect the sensor to the "port 1" in the sensor bridge and then the sensor bridge with the USB to the computer. 
	
	[1] https://www.sensirion.com/en/environmental-sensors/humidity-sensors/digital-humidity-sensors-for-various-applications/
	[2] https://www.sensirion.com/en/environmental-sensors/evaluation-kit-sek-environmental-sensing/
	
	NOTE: Before I was able to make this work, I had to open the graphical interface downloadable here https://www.sensirion.com/en/controlcenter/ and after this the computer was able to "detect" the `\dev\ttyUSB0`. I think it is a permission issue which is automatically solved by their software."""
	def __init__(self, bridge_port=1, port='/dev/ttyUSB0', baudrate=460800):
		"""Arguments:
		- bridge_port: int, either 1 or 2 depending on which output of the bridge you connect your sensor.
		- port: str, the port where the sensor bridge is available, e.g. in Linux '/dev/ttyUSB0'.
		
		To find what you should put in the `port` argument, in Linux you can use this https://unix.stackexchange.com/questions/144029/command-to-determine-ports-of-a-device-like-dev-ttyusb0/144735#144735"""
		port = ShdlcSerialPort(port='/dev/ttyUSB0', baudrate=460800)
		bridge = SensorBridgeShdlcDevice(ShdlcConnection(port), slave_address=0)
		# Configure SensorBridge port 1 for SHT3x
		if bridge_port not in {1,2}:
			raise ValueError(f'`bridge_port` must be 1 or 2, received {repr(bridge_port)}.')
		sensor_bridge_port = SensorBridgePort.ONE if bridge_port==1 else SensorBridgePort.TWO
		bridge.set_i2c_frequency(sensor_bridge_port, frequency=100e3)
		bridge.set_supply_voltage(sensor_bridge_port, voltage=3.3)
		bridge.switch_supply_on(sensor_bridge_port)
		# Create SHT3x device
		i2c_transceiver = SensorBridgeI2cProxy(bridge, port=sensor_bridge_port)
		self.sht3x = Sht3xI2cDevice(I2cConnection(i2c_transceiver))
		self._communication_lock = RLock() # To make a thread safe implementation.
	
	def measure(self):
		"""Performs a "single shot measurement" and returns both temperature and humidity in a dictionary of the form `{'Temperature (°C)': temperature, 'Humidity (%RH)': humidity}`."""
		with self._communication_lock:
			temperature, humidity = self.sht3x.single_shot_measurement()
		return {'Temperature (°C)': temperature.degrees_celsius, 'Humidity (%RH)': humidity.percent_rh}
	
	@property
	def temperature(self):
		"""Returns a single reading of the temperature in Celsius as a float number."""
		return self.measure()['Temperature (°C)']
	
	@property
	def humidity(self):
		"""Returns a single reading of the humidity in %RH as a float number."""
		return self.measure()['Humidity (%RH)']

if __name__ == '__main__':
	# Example program.
	import time
	
	sensor = SensirionSensor()
	while True:
		print(f'Temperature: {sensor.temperature:.2f} °C | Humidity: {sensor.humidity:.2f} %RH')
		time.sleep(1)
