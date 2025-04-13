from PN532 import *

if __name__ == '__main__':
    try:
        pn532 = PN532('/dev/ttyUSB0')

        pn532.GetFirmwareVersion()
        pn532.InListPassiveTarget()

        pn532.GetGeneralStatus()

        pn532.FielfOff()
        pn532.GetGeneralStatus()
        pn532.FieldOn()
        pn532.GetGeneralStatus()

        pn532.close()

    except Exception as e:
        print("[ERROR]", str(e))