# Dado
A M5Atom based dice with configurable number of sides (2-9)

## Install the script

Set enviroment (ESPPORT can change on your operative system).

```
ESPPORT=/dev/cu.usbserial-00001014
BAUDRATE=115200
```

Download and install MicroPython on M5Atom using esptool.

```
wget https://micropython.org/resources/firmware/esp32-idf4-20200329-v1.12-317-g688323307.bin
esptool.py --chip esp32 --port $ESPPORT erase_flash
esptool.py --chip esp32 --port $ESPPORT --baud $BAUDRATE write_flash -z 0x1000 esp32-idf4-20200329-v1.12-317-g688323307.bin
```

Install scripts using ampy.

```
ampy -p $ESPPORT -b $BAUDRATE put .py
ampy -p $ESPPORT -b $BAUDRATE put boot.py
```

## Usage

### Select the number of sides
During background is blue you can configure the number of sides of your emulated dice, the board will show you values from 2 to 9, long press when you want select the value.

### Shake it
When you shake the board the background will become red and show some randomly generate value, until you will stop shaking for some seconds,

### Get the result
When the dice will stop the background will be green and you can read the result.

Shake again in order to generate a new value.

## Random number generator
Random number are generated following this steps:

- A buffer with information from accelerometer and gyroscope are created
- We add some random characters to the buffer 
- We calculate the sha256 of the generate buffer 
- We start to consider every character in the sha result encoded in hex
- If the char is bigger than number of sides of the dice we discard and read following char, if not we found our number
