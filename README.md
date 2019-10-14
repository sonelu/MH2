# MH2

<img src="./img/IMG_2580.jpg?raw=true" width="500px">

Miha 2 (Mini Humanoid Gen 2) is a 22 Degrees of Freedom (DOF) Humanoid Robot intended for research and learning.

The main features of the robot are:

* 22 high performance daisy chained actuators [XL-320](http://emanual.robotis.com/docs/en/dxl/x/xl320/) from Robotis
* Main controller: [FriendlyElec NanoPi Neo Core2 LTS](https://www.friendlyarm.com/index.php?route=product/product&path=69&product_id=211) with:
  - Quad-Core Allwinner H5 processor at 1.5GHz
  - 1GB RAM
  - only 7g weight
* Custom add-on board with:
  - 4 channels Dynamixel bus (provided by a [FTDI4232H](https://www.ftdichip.com/Support/Documents/DataSheets/Modules/DS_FT4232H_Mini_Module.pdf) (USB to UART 4 channels)
  - [LSM330](https://media.digikey.com/pdf/Data%20Sheets/ST%20Microelectronics%20PDFS/LSM330.pdf) 6 axis IMU (accelerometer and gyroscope)
  - [Murata 5V 1.A high performance DC/DC convertor](https://power.murata.com/data/power/oki-78sr.pdf)
* 5MP USB camera (in the head)
* 1.5" 128x128 pixel OLED display (I2C SSD1327 chip)
* 8 tactile switches controlled with a TCA9538 I2C I/O expander providing easy interation with the menues on display
* Power provided by 4 18650 industry standard rechargeable batteries located in the feet and hotswappable; the hotswap capability is provided by a pair of small cicuits that provide a "smart diode" functionality, preventing rush current while chainging the batteries. **A full charge allows aproximatelly 4 hours of operation**.

The [software](./mh2/) is based on the [pypot](https://github.com/poppy-project/pypot) library and I have plans to include ROS support by leveraging the [ROBOTIS-Framework](https://github.com/ROBOTIS-GIT/ROBOTIS-Framework) packages.

The [robot parts](./stl) are 3D printed.
