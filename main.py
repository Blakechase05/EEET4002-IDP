from machine import Pin, I2C, ADC
from time import sleep
import ssd1306

# I2C bus
i2c = I2C(0, scl=Pin(46), sda=Pin(18))
print("I2C devices found:", i2c.scan())

# Display
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Rain sensor
rain_adc = ADC(Pin(4))
rain_adc.atten(ADC.ATTN_11DB)
rain_digital = Pin(2, Pin.IN)

def read_rain():
    raw = rain_adc.read()
    # Remap 47-90% to 0-100%
    percent = 100 - int((raw / 4095) * 100)
    mapped = int((percent - 47) / (90 - 40) * 100)
    mapped = max(0, min(100, mapped))  # clamp to 0-100
    return mapped

def display_data(temp, hum, pres, lux, wind, rain_pct):
    oled.fill(0)
    oled.text("Tmp:{:.1f}C".format(temp), 0, 0)
    oled.text("Hum:{:.0f}%".format(hum), 70, 0)
    oled.text("Pres:{:.0f}hPa".format(pres), 0, 12)
    oled.text("Lux:{:.0f}".format(lux), 0, 24)
    oled.text("Wind:{:.1f}km/h".format(wind), 0, 36)
    oled.text("Rain:{}%".format(rain_pct), 0, 48)
    oled.show()

while True:
    rain_pct = read_rain()
    # Temporary test data for other sensors
    display_data(23.5, 61, 1013, 450, 12.3, rain_pct)
    sleep(1)