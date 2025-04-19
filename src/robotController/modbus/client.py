from pymodbus.client.sync import ModbusTcpClient
from time import sleep

class ModbusClient:
    def __init__(self, ip='192.168.141.1', port=1502):
        self.client = ModbusTcpClient(ip, port)
        if not self.client.connect():
            raise ConnectionError(f"Unable to connect to Modbus server at {ip}:{port}")

    def send_command(self, address, value, reset=True):
        """Write to a coil with optional auto-reset"""
        try:
            result = self.client.write_coil(address, value)
            if result.isError():
                raise RuntimeError(f"Error writing to coil at address {address}")
                
            if reset:
                sleep(0.1)  # Wait for command to process
                result = self.client.write_coil(address, False)
                if result.isError():
                    raise RuntimeError(f"Error resetting coil at address {address}")
                    
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to send command to address {address}: {str(e)}")

    def close(self):
        self.client.close()