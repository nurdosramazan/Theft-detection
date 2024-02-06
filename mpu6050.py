from machine import SoftI2C, Pin
import time

class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')  # Wake the sensor up

    def read_raw_data(self, reg):
        high = self.i2c.readfrom_mem(self.addr, reg, 1)
        low = self.i2c.readfrom_mem(self.addr, reg + 1, 1)
        value = (high[0] << 8) | low[0]
        if value > 32768:
            value -= 65536
        return value

    def get_accel_data(self):
        acc_x = self.read_raw_data(0x3B)
        acc_y = self.read_raw_data(0x3D)
        acc_z = self.read_raw_data(0x3F)
        return {'x': acc_x, 'y': acc_y, 'z': acc_z}
