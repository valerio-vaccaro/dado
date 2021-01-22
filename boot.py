# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
# import webrepl
# webrepl.start()

from neopixel import NeoPixel
from machine import Pin, I2C
from mpu6886 import MPU6886
from time import sleep
from math import *
from os import urandom
from ubinascii import hexlify, unhexlify
import hashlib
import network

def paint_dice(np, value, background):
    for i in range(0, 25):
        k = dice[value][i]
        if k == 1:
            np[i] = (20, 20, 20)
        else:
            np[i] = background
    np.write()

def get_sides(np, button_pin):
    while(True):
        for sides in range(2, 10):
            paint_dice(np, sides, BLUE)
            sleep(1)
            if (button_pin.value() == 0):
                return sides

def wait_for_a_shake():
    base_ax, base_ay, base_az = imu.getAccelData()
    sleep(0.5)
    while(True):
        ax,ay,az = imu.getAccelData()
        distance = sqrt((base_ax - ax)**2+(base_ay - ay)**2+(base_az - az)**2)
        if (distance > 1.5):
            return
        base_ax, base_ay, base_az = imu.getAccelData()
        sleep(0.1)

def rolling(np, imu):
    base_ax, base_ay, base_az = imu.getAccelData()
    sleep(0.5)
    quiet_interval = 20
    while True:
        candidate_found = False
        while(not candidate_found):
            ax,ay,az = imu.getAccelData()
            gx,gy,gz = imu.getGyroData()
            distance = sqrt((base_ax - ax)**2+(base_ay - ay)**2+(base_az - az)**2)
            sensor = "acc: %f %f %f gyro: %f %f %f "% (ax, ay, az, gx, gy, gz)
            random_bytes = sensor + str(hexlify(urandom(32)), 'ascii')
            candidates = str(hexlify(hashlib.sha256(random_bytes.encode('ascii')).digest()), 'ascii')
            print(str(quiet_interval) + '(' + str(distance) + '): ' + random_bytes+' -> '+candidates)

            for i in range(len(candidates)):
                candidate = int(candidates[i], 16)
                if candidate > sides:
                    continue
                elif candidate < 1:
                    continue
                else:
                    candidate_found = True
                    break

        paint_dice(np, candidate, RED)
        if (distance < 1.0):
            quiet_interval = quiet_interval - 1
        else:
            quiet_interval = 10
        base_ax, base_ay, base_az = imu.getAccelData()
        sleep(0.2)

        if quiet_interval < 1:
            return(candidate)


def color_chase(np, color, wait):
    for i in range(25):
        np[i] = color
        sleep(wait)
        np.write()
        sleep(wait)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def rainbow_cycle(np, wait):
    for j in range(255):
        for i in range(25):
            rc_index = (i * 256 // 25) + j
            (r, g, b) = wheel(rc_index & 255)
            np[i] = (round(r/10), round(g/10), round(b/10))
        np.write()

dice = {}
dice[0] = [
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,0,0,0,
]
dice[1] = [
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,1,0,0,
    0,0,0,0,0,
    0,0,0,0,0,
]
dice[2] = [
    0,0,0,0,1,
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,0,0,0,
    1,0,0,0,0,
]
dice[3] = [
    0,0,0,0,1,
    0,0,0,0,0,
    0,0,1,0,0,
    0,0,0,0,0,
    1,0,0,0,0,
]
dice[4] = [
    1,0,0,0,1,
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,0,0,0,
    1,0,0,0,1,
]
dice[5] = [
    1,0,0,0,1,
    0,0,0,0,0,
    0,0,1,0,0,
    0,0,0,0,0,
    1,0,0,0,1,
]
dice[6] = [
    1,0,0,0,1,
    0,0,0,0,0,
    1,0,0,0,1,
    0,0,0,0,0,
    1,0,0,0,1,
]
dice[7] = [
    1,0,0,0,1,
    0,0,0,0,0,
    1,0,1,0,1,
    0,0,0,0,0,
    1,0,0,0,1,
]
dice[8] = [
    1,0,1,0,1,
    0,0,0,0,0,
    1,0,0,0,1,
    0,0,0,0,0,
    1,0,1,0,1,
]
dice[9] = [
    1,0,1,0,1,
    0,0,0,0,0,
    1,0,1,0,1,
    0,0,0,0,0,
    1,0,1,0,1,
]

BLACK  = ( 0,  0,  0)
RED    = (10,  0,  0)
YELLOW = (25, 15,  0)
GREEN  = ( 0, 10,  0)
CYAN   = ( 0, 25, 25)
BLUE   = ( 0,  0, 10)
PURPLE = (18,  0, 25)
WHITE  = (25, 25, 25)

neopixel_pin = Pin(27, Pin.OUT)
np = NeoPixel(neopixel_pin, 25)
paint_dice(np, 0, BLACK)

rainbow_cycle(np, 0.01)

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)
button_pin = Pin(39, Pin.IN)
MPU6886_SCL = const(21)
MPU6886_SDA = const(25)
i2c = I2C(scl=Pin(MPU6886_SCL), sda=Pin(MPU6886_SDA))

AFS_2G      = const(0x00)
AFS_4G      = const(0x01)
AFS_8G      = const(0x02)
AFS_16G     = const(0x03)
GFS_250DPS  = const(0x00)
GFS_500DPS  = const(0x01)
GFS_1000DPS = const(0x02)
GFS_2000DPS = const(0x03)
imu = MPU6886(i2c, GFS_500DPS, AFS_4G)

print('start')
print('get_sides')
sides = get_sides(np, button_pin)
print('\t return '+str(sides))
paint_dice(np, sides, (0, 0, 0))
sleep(1)
paint_dice(np, 0, BLACK)

while(True):
    print('wait_for_a_shake')
    wait_for_a_shake()
    print('rolling ...')
    candidate = rolling(np, imu)
    print('\t return '+str(candidate))
    paint_dice(np, candidate, GREEN)
