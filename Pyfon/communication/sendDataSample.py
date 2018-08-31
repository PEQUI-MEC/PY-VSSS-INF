import time
from digi.xbee.devices import XBeeDevice

# TODO: Replace with the serial port where your local module is connected to. 
PORT = "/dev/ttyUSB1"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 115200

DATA_TO_SEND = "0.8;0.7"
REMOTE_NODE_ID = "REMOTE"


def main():
    print(" +--------------------------------------+")
    print(" | XBee Python Library Send Data Sample |")
    print(" +--------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)

    try:    
        device.open()
        # Obtain the remote XBee device from the XBee network.
        xbee_network = device.get_network()
        remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
        if remote_device is None:
            print("Could not find the remote device")
            exit(1)
        device.set_sync_ops_timeout(15)

        print("Sending data to %s >> %s..." % (remote_device.get_64bit_addr(), DATA_TO_SEND))

        start_time = time.time()
        device.send_data(remote_device, DATA_TO_SEND)
        elapsed_time = time.time() - start_time

        print("Success with %s" % elapsed_time)

        print("Sending data to %s >> %s..." % (remote_device.get_64bit_addr(), "0.3;0.1"))

        start_time = time.time()
        device.send_data(remote_device, DATA_TO_SEND)
        elapsed_time = time.time() - start_time

        print("Success2 with %s" % elapsed_time)
    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()