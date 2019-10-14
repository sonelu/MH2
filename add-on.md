# Add-On Board for MH2

The MH2 robot uses the [FriendlyElec NanoPi Neo Core2 LTS](https://www.friendlyarm.com/index.php?route=product/product&path=69&product_id=211) main controller. To control the Dynamixel servomotors it uses a custom add-on board:

<img src="./img/IMG_2088.JPG?raw=true" width="500px">

This board provides the following:

* uses one of the USB from the NanoPi board and [FTDI4232H](https://www.ftdichip.com/Support/Documents/DataSheets/ICs/DS_FT4232H.pdf) chip to produce 4 UART channels (they will appear as /dev/ttyUSB0 to /dev/ttyUSB3 to the operating system)
* the FTDI chip is programmed using a [93LC46BT](http://www.microchip.com/mymicrochip/filehandler.aspx?ddocname=en550232) 1K EEPROM to configure it in RS485 mode (see page 20 in the FTDI4232 datasheet); this way we can easily convert the RX/TX dignals from the UARTs in a semi-duplex signal required by the Dynamixel bus
* the RX/TX pairs and TXDEN is then passed through a [74LVC2G241](http://www.ti.com/general/docs/suppproductinfo.tsp?distId=10&gotoUrl=http%3A%2F%2Fwww.ti.com%2Flit%2Fgpn%2Fsn74lvc2g241) buffer for each of the 4 UARTs, producing the 1 wire [semi-duplex](http://emanual.robotis.com/docs/en/dxl/x/xl320/#communication-circuit) serial signal used by the Dynamixel servos
* there are 8 Dynamixel XL-320 connectors ([Molex 53253-0370](https://www.molex.com/molex/products/datasheet.jsp?part=active/0532530370_PCB_HEADERS.xml)), 2 for each channel
* connected on the I2C there is a [LSM330](https://media.digikey.com/pdf/Data%20Sheets/ST%20Microelectronics%20PDFS/LSM330.pdf) 6 axis IMU (accelerometer and gyroscope) that the robot can use to evaluate the posture
* a 4 pin Molex connector for I2C (used by the OLED screen and the button I/O expander)
* 2 connectors for the cooling fans

On the back side of the board we have:

<img src="./img/IMG_2089.JPG?raw=true" width="500px">

* one USB connector for the WiFi dongle (the board does not have WiFi onboard)
* the 5V regulator (1.5A) [Murata OKI-78SR-5/1.5-W36-C](https://power.murata.com/data/power/oki-78sr.pdf)
* the connector the external power jack

The board is fitted directly on top of the GPIO pins of the NanoPi Neo Core2 board:

<img src="./img/IMG_2090.JPG?raw=true" width="500px">
