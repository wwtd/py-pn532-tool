import serial
import time

MIFARE_CMD_AUTHENTICATE_A = 0x60
MIFARE_CMD_AUTHENTICATE_B = 0x61
MIFARE_CMD_16_BYTES_READ  = 0x30
MIFARE_CMD_16_BYTES_WRITE = 0xA0
MIFARE_CMD_4_BYTES_WRITE  = 0xA2
MIFARE_CMD_INCREMENT      = 0xC1
MIFARE_CMD_DECREMENT      = 0xC0
MIFARE_CMD_TRANSFER       = 0xB0
MIFARE_CMD_RESTORE        = 0xC2

class PN532:
    def __init__(self, port, baudrate=115200, timeout=1):
        try:
            self.ser = serial.Serial(port, baudrate, bytesize=8, parity='N', stopbits=1, timeout=timeout)
            print(f"[INFO] Serial {port} Opened")
        except Exception as e:
            print("Open Seaial failed:", str(e))
            raise

    def close(self):
        if self.ser.is_open:
            self.ser.close()
            print("[INFO] Serial Closed")

    def calculate_checksum(self, data):
        return (~sum(data) + 1) & 0xFF

    def build_frame(self, data_payload):
        frame = bytearray()

        # Preamble + Start Code
        frame += b'\x00\x00\xFF'

        # Length + Length Checksum
        length = len(data_payload)
        frame.append(length)
        frame.append((~length + 1) & 0xFF)

        # Data Payload
        frame += data_payload

        # Data Checksum
        data_checksum = self.calculate_checksum(data_payload)
        frame.append(data_checksum)

        # Postamble
        frame.append(0x00)

        return frame

    def pn532_data_exchange(self, data_payload):
        # 构建完整帧
        frame = self.build_frame(data_payload)

        # 发送
        print("[DEBUG] Send CMD:", frame.hex().upper())
        self.ser.write(frame)

        # 等待 ACK
        time.sleep(0.05)
        ack = self.ser.read(6)
        if ack:
            print("[DEBUG] Recv ACK:", ack.hex().upper())
        else:
            print("[WARN] NO ACK!!!")
            return None

        # 读取响应帧
        time.sleep(0.1)
        response = self.ser.read_all()
        if response:
            print("[DEBUG] Recv Resp:", response.hex().upper())
            return response
        else:
            print("[WARN] No Resp!!!")
            return None
    def GetFirmwareVersion(self):
        payload = bytes.fromhex("D4 02")
        response = self.pn532_data_exchange(payload)
        return response
    
    def InListPassiveTarget(self):
        payload = bytes.fromhex("D4 4A 01 00")
        response = self.pn532_data_exchange(payload)
        return response

    def FieldOn(self):
        payload = bytes.fromhex("D4 32 01 01")
        response = self.pn532_data_exchange(payload)
        return response

    def FielfOff(self):
        payload = bytes.fromhex("D4 32 01 00")
        response = self.pn532_data_exchange(payload)
        return response

    def GetGeneralStatus(self):
        payload = bytes.fromhex("D4 04")
        response = self.pn532_data_exchange(payload)
        return response

    def InDataExchange(self, data):
        payload = bytes.fromhex("D4 40") + data
        response = self.pn532_data_exchange(payload)
        return response

    def m1_authenticate(self, block, key, uid, card =0x01):
        assert len(key) == 6
        assert len(uid) == 4
        # auth rule: target + 60 + block + key + uid
        auth_cmd = bytes([card, MIFARE_CMD_AUTHENTICATE_A, block]) + key + uid
        response = self.InDataExchange(auth_cmd)
        if response and response[6] == 0x41 and response[7] == 0x00:
            print("[INFO] AUTH SUCCESS")
            return True
        else:
            print("[ERROR] AUTH FAIL", response)
            return False

    def m1_read_block(self, block, card =0x01):
        read_cmd = bytes([card, MIFARE_CMD_16_BYTES_READ, block])
        response = self.InDataExchange(read_cmd)
        return response[-18:-2]

    def m1_write_block(self, block, data, card =0x01):
        write_cmd = bytes([card, MIFARE_CMD_16_BYTES_WRITE, block]) + data
        response = self.InDataExchange(write_cmd)