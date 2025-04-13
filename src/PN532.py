import serial
import time

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