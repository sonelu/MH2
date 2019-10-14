import smbus2
import time


class LSM330():

    def __init__(self, busno=0, addr_g=0x6a, addr_a=0x1e):
        self.busno = busno
        self.addr_g = addr_g
        self.addr_a = addr_a 

        self.bus = smbus2.SMBus(self.busno)
        # configure gyro
        # 0x20h is the control register
        # 0x0f is all axes ON and default 95Hz DR and 12.5Hz BW (see page 60 in manual)
        self.bus.write_byte_data(self.addr_g, 0x20, 0x0F)

        # configure accelerometer
        # 0x20 is the control register
        # 0x67 is 100Hz all axes on
        self.bus.write_byte_data(self.addr_a, 0x20, 0x67)
        time.sleep(0.5)

    def __read2bytes(self, dev_addr, reg_addr):
        d0 = self.bus.read_byte_data(dev_addr, reg_addr)
        d1 = self.bus.read_byte_data(dev_addr, reg_addr+1)
        val = d1 * 256 + d0
        if val > 32767:
            val -= 65536
        return val

    def get_acc(self):
        x_a = self.__read2bytes(self.addr_a, 0x28)
        y_a = self.__read2bytes(self.addr_a, 0x2A)
        z_a = self.__read2bytes(self.addr_a, 0x2C)
        return (x_a, y_a, z_a)

    def get_gyro(self):
        x_g = self.__read2bytes(self.addr_g, 0x28)
        y_g = self.__read2bytes(self.addr_g, 0x2A)
        z_g = self.__read2bytes(self.addr_g, 0x2C)
        return (x_g, y_g, z_g)