# The MIT License (MIT)
#
# Copyright (c) 2016 Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Modified by Thomas Upfold on 13/12/2018 to work with the LSM303C device. The original file can be found here https://github.com/adafruit/Adafruit_Python_LSM303/blob/master/Adafruit_LSM303/LSM303.py

# These values are the default device addresses and can be found in the datasheet on page 26. Additionally, you can check these addresses in raspbian with sudo i2cdetect -y 1

LSM303_ADDRESS_ACCEL = (0x3a >> 1)  # yields 1D
LSM303_ADDRESS_MAG   = (0x3c >> 1)  # yields 1E
                                         
LSM303_REGISTER_ACCEL_CTRL_REG1_A = 0x20  # HR,     ODR2,   ODR1,   ORD0,   BDU,    ZEN,    YEN,    XEN     what I want: 0x27 50Hz, all axis
LSM303_REGISTER_ACCEL_CTRL_REG2_A = 0x21  # -,      DFC1,   DFC0,   HPM1,   HPM0,   FDS,    HPIS2,  HPIS1   what I want: 0x00 default is fine
LSM303_REGISTER_ACCEL_CTRL_REG3_A = 0x22  # stuff I prob dont want                                          what I want: 0x00 default is fine
LSM303_REGISTER_ACCEL_CTRL_REG4_A = 0x23  # BW2,    BW1,    FS1,    FS0,    stuff I prob dont want          what I want: 0x24 (+- 4g)
LSM303_REGISTER_ACCEL_CTRL_REG5_A = 0x24  # DBG,    RST,    DEC1,   DEC0,   ST2,    ST1,    HLA,    PPOD    what I want: 0x00 default is fine
LSM303_REGISTER_ACCEL_OUT_X_L_A   = 0x28  # where the data at

LSM303_REGISTER_MAG_CTRL_REG1_M    = 0x20 # TEN,    OM1,    OM0,    DO2,    DO1,    DO0,    0,      ST      what I want: 0x10 default is fine
LSM303_REGISTER_MAG_CTRL_REG2_M    = 0x21 # 0,      FS1,    FS0,    0,      RBT,    RST,    0,      0       what I want: 0x60 +- 16 gauss
LSM303_REGISTER_MAG_CTRL_REG3_M    = 0x22 # I2CD,   0,      LP,     0,      0,      SIM,    MD1,    MD0     what I want: 0x00 Continuous-conversion mode
LSM303_REGISTER_MAG_CTRL_REG4_M    = 0x23 # 0,      0,      0,      0,      OMZ1,   OMZ0,   BLE,    0       what I want: 0x00 default is fine (little endian)
LSM303_REGISTER_MAG_CTRL_REG5_M    = 0x24 # 0,      BDU,    0,      0,      0,      0,      0,      0       what I want: 0x00 default is fine
LSM303_REGISTER_MAG_OUT_X_L_M      = 0x28 # where the data at


class LSM303C(object):
    """LSM303C accelerometer & magnetometer."""

    def __init__(self, accel_address=LSM303_ADDRESS_ACCEL,
                 mag_address=LSM303_ADDRESS_MAG, i2c=None, **kwargs):
        """Initialize the LSM303 accelerometer & magnetometer. """
        # Setup I2C interface for accelerometer and magnetometer.
        if i2c is None:
            import Adafruit_GPIO.I2C as I2C
            i2c = I2C
        self._accel = i2c.get_i2c_device(accel_address, **kwargs)
        self._mag = i2c.get_i2c_device(mag_address, **kwargs)

        # Enable the accelerometer
        self._accel.write8(LSM303_REGISTER_ACCEL_CTRL_REG1_A, 0x97)
        self._accel.write8(LSM303_REGISTER_ACCEL_CTRL_REG1_A, 0x04)
        self._accel.write8(LSM303_REGISTER_ACCEL_CTRL_REG4_A, 0x24)
        # Enable the magnetometer
        #self._mag.write8(LSM303_REGISTER_MAG_CTRL_REG1_M, 0x10)
        self._mag.write8(LSM303_REGISTER_MAG_CTRL_REG2_M, 0x60)
        self._mag.write8(LSM303_REGISTER_MAG_CTRL_REG3_M, 0x00)

    def read(self):
        """Read the accelerometer and magnetometer value.  A tuple of tuples will
        be returned with:
          ((accel X, accel Y, accel Z), (mag X, mag Y, mag Z))
        """
        # Read the accelerometer as signed 16-bit little endian values.
        ax = self._accel.readS16(0x28) * 0.122 # 0.122 mg/LSB or 
        ay = self._accel.readS16(0x2A) * 0.122
        az = self._accel.readS16(0x2C) * 0.122

        accel = (ax, ay, az)
        # # Read the magnetometer as signed 16-bit little endian values.
        mx = self._mag.readS16(0x28) *  0.58 # 0.58 mgauss/LSB
        my = self._mag.readS16(0x2A) *  0.58
        mz = self._mag.readS16(0x2C) *  0.58

        mag = (mx, my , mz)
        return (accel, mag)