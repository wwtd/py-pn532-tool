from PN532 import *

if __name__ == '__main__':
    try:
        pn532 = PN532('/dev/ttyUSB0')

        ListPassiveTarget_resp = pn532.InListPassiveTarget()
        print(f"[INFO] NbTg : {ListPassiveTarget_resp[7]}")
        print(f"[INFO] Tg : {ListPassiveTarget_resp[8]}")
        print(f"[INFO] SENS_RES : {hex(ListPassiveTarget_resp[10])} {hex(ListPassiveTarget_resp[9])} ")
        print(f"[INFO] SEL_RES : {hex(ListPassiveTarget_resp[11])}")
        print(f"[INFO] NFCIDLength : {hex(ListPassiveTarget_resp[12])}")
        print(f"[INFO] NFCID : {hex(ListPassiveTarget_resp[13])} {hex(ListPassiveTarget_resp[14])} {hex(ListPassiveTarget_resp[15])} {hex(ListPassiveTarget_resp[16])}")

        pn532.m1_authenticate(0x00, bytes.fromhex("FFFFFFFFFFFF"), ListPassiveTarget_resp[13:17])
        print("Block 0:", pn532.m1_read_block(0x00).hex())
        print("Block 1:", pn532.m1_read_block(0x01).hex())
        print("Block 2:", pn532.m1_read_block(0x02).hex())
        print("Block 3:", pn532.m1_read_block(0x03).hex())

        print("Block 2:", pn532.m1_read_block(0x02).hex())
        pn532.m1_write_block(0x02, bytes.fromhex("000102030405060708090A0B0C0D0E0F"))
        print("Block 2:", pn532.m1_read_block(0x02).hex())

        pn532.close()

    except Exception as e:
        print("[ERROR]", str(e))