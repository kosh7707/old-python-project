import wmi
import sys
from cryptography.fernet import Fernet

if __name__ == "__main__":
    key = b'3yAxkyG8snCR8rqpRuTaMejhxrkTpf1eNnrg7WHBkhw='
    cipher_suite = Fernet(key)

    c = wmi.WMI()
    diskdrive_serial_number = c.Win32_PhysicalMedia()[0].SerialNumber
    diskdrive_serial_number = diskdrive_serial_number.replace(" ", "")
    motherboard_product = c.Win32_BaseBoard()[0].Product
    motherboard_product = motherboard_product.replace(" ", "")
    if '/' in diskdrive_serial_number:
        diskdrive_serial_number = diskdrive_serial_number.replace('/', '')
    if '/' in motherboard_product:
        motherboard_product = motherboard_product.replace('/', '')

    with open('customer_info', 'wb') as f:
        plain_text = diskdrive_serial_number + '/' + motherboard_product
        plain_text = plain_text.encode()
        cipher_text = cipher_suite.encrypt(plain_text)
        f.write(cipher_text)

    sys.exit()

