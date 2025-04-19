import os
import subprocess
from .modbus.client import ModbusClient
from .config.settings import MODBUS_ADDRESS, MODBUS_PORT
from .modbus.commands import convert_to_real  # Add this import

class RobotController:
    def __init__(self, modbus_client=None):
        self.modbus_client = modbus_client or ModbusClient(MODBUS_ADDRESS, MODBUS_PORT)

    def check_connection(self):
        """Check if Modbus connection is active."""
        return self.modbus_client and self.modbus_client.client.connect()

    def send_command(self, command):
        """Send a command via Modbus."""
        if not self.modbus_client:
            raise ConnectionError("No Modbus client available")
        return self.modbus_client.send_command(command['address'], True)

    def read_register(self, command):
        """Read a register value via Modbus."""
        if not self.check_connection():
            raise ConnectionError("Unable to connect to Modbus server")

        try:
            if command["type"] == "coil":
                response = self.modbus_client.client.read_coils(command["address"], 1)
                if response.isError():
                    raise RuntimeError(f"Error reading coil at address {command['address']}")
                return response.bits[0]
            elif command["type"] == "holding":
                # For real numbers, read two consecutive registers
                registers_to_read = 2 if command.get("tag_type") == "Real" else 1
                response = self.modbus_client.client.read_holding_registers(
                    command["address"], 
                    registers_to_read
                )
                
                if response.isError():
                    return None
                    
                if command.get("tag_type") == "Real":
                    return convert_to_real(response.registers)
                return response.registers[0]
            else:
                raise ValueError(f"Unsupported command type: {command['type']}")
        except Exception as e:
            raise RuntimeError(f"Failed to read {command['type']} at address {command['address']}: {str(e)}")

    def write_register(self, command, value):
        """Write to holding register with proper type conversion"""
        if not self.check_connection():
            raise ConnectionError("Unable to connect to Modbus server")
            
        try:
            if command["type"] != "holding":
                raise ValueError("This method only supports holding registers")
                
            if command.get("tag_type") == "Real":
                # Convert float to two 16-bit registers
                import struct
                packed = struct.pack('f', float(value))  # Convert float to bytes
                registers = struct.unpack('HH', packed)  # Unpack into two 16-bit integers
                
                # Write both registers
                result = self.modbus_client.client.write_registers(
                    command["address"],
                    list(registers)
                )
            else:
                # Write single register
                result = self.modbus_client.client.write_register(
                    command["address"],
                    int(value)
                )
                
            if result.isError():
                raise RuntimeError(f"Error writing to register at address {command['address']}")
                
            return True
                
        except Exception as e:
            raise RuntimeError(f"Failed to write to register at address {command['address']}: {str(e)}")

    def fetch_axis_data(self, commands):
        """Fetch all axis data from Modbus."""
        axis_data = {}
        for command_name, command in commands.items():
            if command["action"] == "read":
                try:
                    value = self.read_register(command)
                    axis_data[command_name] = value
                except Exception as e:
                    axis_data[command_name] = str(e)
        return axis_data

    def send_gcode(self, gcode_content=None, file_path=None):
        """Send G-code to the robot."""
        try:
            if gcode_content:
                # Create temp directory if it doesn't exist
                temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
                os.makedirs(temp_dir, exist_ok=True)
                temp_file = os.path.join(temp_dir, 'temp_gcode.ngc')
                with open(temp_file, 'w') as f:
                    f.write(gcode_content)
                file_path = temp_file

            if not file_path:
                raise ValueError("No G-code content or file path provided")

            # Get SFTP module path
            sftp_module_path = os.path.join(os.path.dirname(__file__), "sftp_module.exe")
            if not os.path.exists(sftp_module_path):
                raise FileNotFoundError(f"SFTP module not found at: {sftp_module_path}")

            result = subprocess.run(
                [sftp_module_path, "-i", file_path],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(__file__)
            )

            if gcode_content and os.path.exists(temp_file):
                os.remove(temp_file)

            return result
        
        except Exception as e:
            if gcode_content and 'temp_file' in locals() and os.path.exists(temp_file):
                os.remove(temp_file)
            raise e

    def cleanup(self):
        """Clean up resources."""
        if self.modbus_client:
            self.modbus_client.close()