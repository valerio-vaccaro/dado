# Dado
A M5Atom based dice with configurable number of sides (2-9)

## Install the script

Set enviroment (ESPPORT can change on your operative system e.g. /dev/ttyUSB0 on Linux, /dev/cu.usbserial-00001014 on Mac or COM3 on Windows).

```
ESPPORT=/dev/ttyUSB0
BAUDRATE=115200
```

Download and install MicroPython on M5Atom using esptool.

```
wget https://micropython.org/resources/firmware/esp32-idf4-20200902-v1.13.bin
esptool.py --chip esp32 --port $ESPPORT erase_flash
esptool.py --chip esp32 --port $ESPPORT --baud $BAUDRATE write_flash -z 0x1000 esp32-idf4-20200902-v1.13.bin

Install scripts using ampy (if you don't have please install adafruit-ampy via pip3).

```
git clone https://github.com/valerio-vaccaro/dado.git
cd dado
ampy -p $ESPPORT -b $BAUDRATE put mpu6886.py
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

## Debugging

The serial port (via USB) offer some debug information, this is an example of a session with sides set to 4.

```
ets Jun  8 2016 00:22:57

rst:0x1 (POWERON_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
configsip: 188777542, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3fff0018,len:4
load:0x3fff001c,len:5148
load:0x40078000,len:12880
load:0x40080400,len:3484
entry 0x40080630
I (529) cpu_start: Pro cpu up.
I (529) cpu_start: Application information:
I (530) cpu_start: Compile time:     Mar 28 2020 00:44:29
I (533) cpu_start: ELF file SHA256:  0000000000000000...
I (539) cpu_start: ESP-IDF:          v4.0
I (544) cpu_start: Starting app cpu, entry point is 0x40083000
I (0) cpu_start: App cpu up.
I (554) heap_init: Initializing. RAM available for dynamic allocation:
I (561) heap_init: At 3FFAFF10 len 000000F0 (0 KiB): DRAM
I (567) heap_init: At 3FFB6388 len 00001C78 (7 KiB): DRAM
I (573) heap_init: At 3FFB9A20 len 00004108 (16 KiB): DRAM
I (579) heap_init: At 3FFBDB5C len 00000004 (0 KiB): DRAM
I (585) heap_init: At 3FFCCA50 len 000135B0 (77 KiB): DRAM
I (591) heap_init: At 3FFE0440 len 00003AE0 (14 KiB): D/IRAM
I (598) heap_init: At 3FFE4350 len 0001BCB0 (111 KiB): D/IRAM
I (604) heap_init: At 4009EA08 len 000015F8 (5 KiB): IRAM
I (610) cpu_start: Pro cpu start user code
I (629) spi_flash: detected chip: gd
I (629) spi_flash: flash io: dio
I (630) cpu_start: Starting scheduler on PRO CPU.
I (0) cpu_start: Starting scheduler on APP CPU.
I (470) wifi: wifi driver task: 3ffd2d2c, prio:23, stack:3584, core=0
I (1578) system_api: Base MAC address is not set, read default base MAC address from BLK0 of EFUSE
I (1588) system_api: Base MAC address is not set, read default base MAC address from BLK0 of EFUSE
I (1618) wifi: wifi firmware version: 581f422
I (1618) wifi: config NVS flash: enabled
I (1618) wifi: config nano formating: disabled
I (1618) wifi: Init dynamic tx buffer num: 32
I (1618) wifi: Init data frame dynamic rx buffer num: 32
I (1628) wifi: Init management frame dynamic rx buffer num: 32
I (1628) wifi: Init management short buffer num: 32
I (1638) wifi: Init static rx buffer size: 1600
I (1638) wifi: Init static rx buffer num: 10
I (1638) wifi: Init dynamic rx buffer num: 32
start
get_sides
         return 4
wait_for_a_shake
rolling ...
20(0.7719522): acc: -0.096924 0.042480 -0.915527 gyro: 28.778076 -8.361816 -25.634766 b759a5622254276449c12edb583f84a241fdf982f17e1e2de69c256a183eb20d -> e650ef5336f0507502e142f0293362302ac8b7d3ec4f72c59840ad0b05655306
19(0.1512392): acc: -0.086914 -0.031982 -0.989014 gyro: -15.747070 4.257202 -6.057739 447882419f7be6f48a5dfe20e7fddc7c65301933698ee1fbd443e668df101596 -> c36d0d3e67902136880db59cda9c5337c25e78ce218aef044b826307198f38d5
18(0.104613): acc: -0.089355 -0.018311 -0.969971 gyro: -0.259399 5.859375 0.732422 8ccce86b31b3746d4226c4a6bae01ff4b155562bc949025fffe02373e2ee30b6 -> b937bbd2f0bb249a38659cac246b9d7d0094778beeb002fdd975e8ca56caf99e
17(0.0750243): acc: -0.010254 -0.016357 -0.998779 gyro: -1.663208 -0.305176 0.381470 eb1b61bcb477c8e9630eca43add9357814e2c474fd24241cfd0633b71d773842 -> de115e218c7dae403db7a53891fedc8745967b906be52702b52f3930c8c3fc7b
16(0.05684441): acc: 0.014648 -0.039307 -1.018311 gyro: -1.632690 -1.861572 0.061035 e60c239412ed79e8dbd2e43b38fb9a3d6f7d4fa6dbde800b3fe56d4b7174c8f1 -> 7b375ebf2c558fa0a6619936eff959f1892d4bb300814b9d208fa88a94bac249
15(0.1541098): acc: 0.094971 0.011230 -0.864258 gyro: -2.227783 -5.020142 -6.195068 36bd1d07b9e48f475fb442a83f672bf79d400e44d85f987bf9bfcb3c48fd1f5b -> 2028d1243df5f2a7ea4362cd08da122c4a7ac7d281aaf93afe2418885171ba03
14(0.1031496): acc: -0.005127 -0.037109 -0.991455 gyro: -0.305176 -0.137329 0.534058 29bd90da07e4d2574079ad26d53a1505d057a370a60c96d82bcf8378c8bf0277 -> 6eb64dbbd217c9cc718a9f51e3c1b1dbf98fb9009d0cb9050f01ec4e45a916d3
13(0.004508346): acc: 0.001221 -0.038330 -0.987793 gyro: -0.366211 0.000000 0.564575 c94a8835692d355f1e3b6bc4fce586c48aa68ab8c243e42225228b1ab6f1a207 -> 1fd001772db121c847bf466e3cd2a2dcf82a24f13c340954311752b98705726a
12(0.00538218): acc: 0.001953 -0.034180 -0.990479 gyro: -0.335693 -0.076294 0.534058 601b9c09dbfde0eabc9fe849274bcf0e49ad8c38dae39bf9572790b641ec263f -> 492407da5fe357a2adfafd8ffe47fec8ec56d4e66ec9ed89f9a4afb7fbe3d1c9
11(0.003211169): acc: 0.000244 -0.037598 -0.989502 gyro: -0.396729 -0.137329 0.579834 41ddcf5d634c55878f0ddcb8add4fec8d2db35dea070a7dcd3b14ba72bc27958 -> c91a23ea1d452d75b2f1475da2da9ba774fea92472bcbfadc55626d6a3a48927
10(0.00252541): acc: 0.002441 -0.038086 -0.990967 gyro: -0.457764 -0.305176 0.625610 ed37fd6addc5f2ac49a680d66674d08f98799b1276fae848c3d5ef6d41881f4f -> ed99b6ace0a47e9c5d90410142c7061b8bb1ff737ceb5b587562d98ff30faa54
9(0.002142325): acc: 0.001709 -0.037598 -0.990479 gyro: -0.381470 -0.228882 0.610352 d3055c9987b2ca440822af17024f043e8e4b15f268a8ea7821e8bdd53dc27ea4 -> a4845f8906b7512017f0707ca615f28da4a7e3fda281db6f04aa285ab3d7309a
8(0.003790082): acc: 0.003174 -0.038574 -0.991699 gyro: -0.289917 -0.228882 0.564575 fda7217f94998fb171b879ce5ea64192875fecc8fd017c962094dba8445b255b -> 2539ee2b95a3e9e9e12b348429ffe7e0558147accb830e89bed0c78429a8761c
7(0.002548903): acc: -0.001465 -0.036377 -0.990479 gyro: -0.350952 -0.274658 0.610352 9b0de41588996717041c538a30d662a6e44877af502fc729b90ae01e126ebe75 -> b5f38874d20baa35ddfe95e7b341c333d03b877084a64aeeb416f74e11ed0940
6(0.001760523): acc: 0.002686 -0.036865 -0.989258 gyro: -0.366211 -0.259399 0.610352 bac9b7898c713c7aadbd5e73620c8094926c6175541828c7e078d3766ff51ecd -> 88157189c143606958f7a02178fa397f3a3a7beb5d914ab94769b7e7cc7abc09
5(0.002328953): acc: 0.002930 -0.037109 -0.989014 gyro: -0.396729 -0.259399 0.640869 c5b7e72d613627f1d4a1ec47185fcf6406a6ae957aaeed7f392b6d21ca011ec0 -> 75012fc93314d2a8f318f93032a588c864522da5e53725733a981b503a943575
4(0.002513582): acc: 0.000488 -0.037109 -0.989990 gyro: -0.442505 -0.213623 0.564575 0d13d6635b82a57e9168698c1232eb7bc10833b162860a37acc81c3436abd426 -> 31f2a2c7e233583a3753463132b898ef011d8522a480d8f225db52c55f362ae5
3(0.002085938): acc: 0.001953 -0.036377 -0.989258 gyro: -0.442505 -0.335693 0.595093 4b8515d20fde4f967c17dc6cd7150276a2f4fd86063e1cd2dc4e4ee1affc977d -> 8ca6a553b0901d92c152450d81af31ded23c0cfefffea86fd50a55fd953de592
2(0.002729575): acc: 0.000244 -0.037842 -0.990479 gyro: -0.335693 -0.320435 0.595093 b45a62b8633df94cf25166c04272accc5b08cabe2e707ac0c35b228034f91cd6 -> 55ad03f41a680b1f91ddeb3776c435bf06313c5e827e6ab207a67040227e4433
1(0.003694518): acc: 0.005859 -0.035645 -0.989990 gyro: -0.350952 -0.289917 0.640869 0d848f7f131d6414b0644719a0e6ea43a14f7134aa5c734db5c0b9ed56782bb1 -> 75a869c9884a0255def22488bf525247b23bc9b7fdd632c619a757fd87e6e878
         return 4
wait_for_a_shake
```

Now the board is ready for next roll.
