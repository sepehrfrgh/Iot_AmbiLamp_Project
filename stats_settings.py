import time
import requests

from libraries.DHT22 import DHT22
from libraries.MCP300X import MCP300X


dht22_pin=16
dht22 = DHT22(dht22_pin)


mcp3004 = MCP300X.MCP3004
mcp = MCP300X(mcp3004)

ldr = mcp.CH2

dataUrl='http://intro-to-iot-196.herokuapp.com/api/data'
statUrl='http://intro-to-iot-196.herokuapp.com/api/statistics'
settingUrl='http://intro-to-iot-196.herokuapp.com/api/settings'

dataPacket = {}
statPacket = {}

delay = 10 * 60

while True:

        stats = requests.get(statUrl)
        stats = stats.json()

        settings = requests.get(settingUrl)
        settings = settings.json()

        humidity, temperature = dht22.get_temperature_and_humidity()

        brightness = mcp.read(ldr)

        dataPacket['temperature'] = round(temperature, 3)
        dataPacket['humidity'] = round(humidity, 3)
        dataPacket['brightness'] = brightness

        statPacket['timeTotal'] = stats['timeTotal'] + 1

        statPacket['avgTemperature'] = stats['avgTemperature'] + (round(temperature, 3) - stats['avgTemperature'])/statPacket['timeTotal']
        statPacket['avgHumidity'] = stats['avgHumidity'] + (round(humidity, 3) - stats['avgHumidity'])/statPacket['timeTotal']
        statPacket['avgBrightness'] = stats['avgBrightness'] + (brightness - stats['avgBrightness'])/statPacket['timeTotal']

        if (temperature > settings['hotThreshold']):
            statPacket['timeInHot'] = stats['timeInHot'] + 1

        if (temperature < settings['coldThreshold']):
            statPacket['timeInCold'] = stats['timeInCold'] + 1

        if (humidity < settings['dryThreshold']):
            statPacket['timeInDry'] = stats['timeInDry'] + 1

        if (humidity > settings['humidThreshold']):
             statPacket['timeInHumid'] = stats['timeInHumid'] + 1

        if (settings['lightIsOn']):
            statPacket['timeOn'] = stats['timeOn'] + 1

        r = requests.post(dataUrl,json=dataPacket)
        s = requests.put(statUrl, json=statPacket)

        time.sleep(delay)
