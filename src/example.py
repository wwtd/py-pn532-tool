from PN532 import *

if __name__ == '__main__':
    try:
        pn532 = PN532('/dev/ttyUSB0')

        ListPassiveTarget_resp = pn532.InListPassiveTarget()
        print(f"NbTg : {ListPassiveTarget_resp[7]}")
        print(f"Tg : {ListPassiveTarget_resp[8]}")
        print(f"SENS_RES : {hex(ListPassiveTarget_resp[10])} {hex(ListPassiveTarget_resp[9])} ")
        print(f"SEL_RES : {hex(ListPassiveTarget_resp[11])}")
        print(f"NFCIDLength : {hex(ListPassiveTarget_resp[12])}")
        print(f"NFCID : {hex(ListPassiveTarget_resp[13])} {hex(ListPassiveTarget_resp[14])} {hex(ListPassiveTarget_resp[15])} {hex(ListPassiveTarget_resp[16])}")

        pn532.close()

    except Exception as e:
        print("[ERROR]", str(e))