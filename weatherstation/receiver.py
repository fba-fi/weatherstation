"""API for USB radio receiver for initializing device and data I/O"""

import usb.core
import usb.util

MICROCHIP_VID = 0x04D8
EXAMPLE_PID = 0x003F
INTERFACE = 0

# Read / Write / Reply
READ = 0x00
WRITE = 0x01
REPLY = 0x02

# Message Types
ERROR = 0x00
CONFIG = 0x01
DATA = 0x02
RESETDEVICE = 0x03
RTC = 0x04
MESSAGETYPES = ['NONE', 'CONFIG', 'DATA', 'RESET DEVICE', 'RTC']


class ReceiverError(Exception):
    """Raised when receiver causes unrecoverable error"""
    pass


class MicrochipReceiver(object):

    """Simple API for Microchip Example USB device"""

    def __init__(self):
        """Initialize the class"""

        self.device = None
        self.kernel_driver_detached = False

    def init(self, vendor_id=MICROCHIP_VID, product_id=EXAMPLE_PID):
        """Initialize USB receiver device

        :vendor_id: USB vendor ID (optional)
        :product_id: USB product ID (optional)
        :returns: None

        """

        if self.device is not None:
            return

        self.device = usb.core.find(
            idVendor=vendor_id,
            idProduct=product_id)

        if self.device.is_kernel_driver_active(INTERFACE):
            self.device.detach_kernel_driver(0)
            self.kernel_driver_detached = True

        self.device.set_configuration()
        self.device.reset()

    def release(self):
        """Release the device and reattach kernel driver

        :returns: None

        """

        if self.device is None:
            return

        usb.util.release_interface(self.device, INTERFACE)

        if self.kernel_driver_detached:
            self.device.attach_kernel_driver(INTERFACE)
            self.kernel_detached = False

        self.device = None

    def write(self, message_type, message):
        """Write given message type and data to the device

        :returns: None

        """

        self.init()

        data = [message_type, WRITE, len(message)] + message

        bytes_written = self.device.write(1, data, 0)

        if bytes_written != len(data):
            raise ReceiverError(
                "Write failed! Sent %s bytes, but %s bytes "
                "was written" % (len(data), bytes_written))

        self.release()

        return bytes_written

    def read(self, message_type, message=''):
        """Read data from the device

        :returns: List of read bytes

        """

        self.init()

        data = [message_type, READ]

        if message != '':
            data += [len(message)] + message

        pipe_number = 0x01
        timeout = 0

        self.device.write(pipe_number, data, timeout)

        pipe_number = 0x81
        length = 64
        timeout = 100

        data = self.device.read(pipe_number, length, timeout)

        self.release()

        return data

    def read_rtc(self):
        """Helper method for writing to device real time clock (RTC)

        :returns: Current time as datetime instance

        """

        data = self.read(RTC)

        # TODO: why some other components should handle weird responses?
        # better to return datetime instances

        if(len(data) < 3):
            return []
        if(data[0] != RTC):
            return []
        if(data[1] != REPLY):
            return []
        if(data[2] != 7):
            return []

        return data

    def write_rtc(self, date):
        """Set device real time clock to given `date`.

        :date: New date as datetime instance
        :returns: None

        """
        self.write(RTC, date)

    def write_data(self, data):
        """Helper for writing data to device

        :data: List of bytes to write
        :returns: None

        """
        return self.write(DATA, data)

    def read_data(self):
        """Read data from device

        :returns: List of bytes that was read from device

        """
        return self.read(DATA)

    def read_config(address, length):
        """Read configuration from device

        :address: Configuration register address
        :length: Length of register
        :returns: Configuration register

        """

        data = [0 for x in range(length)]
        data[0] = address

        return self.read(CONFIG, data)
