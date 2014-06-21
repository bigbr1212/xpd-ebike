"""\
Scan for serial ports. Linux specific variant that also includes USB/Serial
adapters.

Part of pySerial (http://pyserial.sf.net)
(C) 2009 <cliechti@gmx.net>
"""

import serial
import glob

def comports(available_only=True):
    """This generator scans the device directory for com ports and yields
    (order, port, desc, hwid).  available_only is ignored for Windows compatibility,
    Order is a helper to get sorted lists. it can be ignored otherwise."""
    order = 1
    # Common Unix USB serial device names
    for port in sorted (glob.glob('/dev/ttyUSB*') + glob.glob('/dev/tty.usbserial*')):
        # this would give wrong results on opened com ports
        #if available_only:
        #    try:
        #        serial.Serial(port) # test open
        #    except serial.serialutil.SerialException:
        #        continue

        yield order, port, "", ""
        order += 1
