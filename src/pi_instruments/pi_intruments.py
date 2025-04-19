from PyQt5 import uic
from PyQt5.QtWidgets import (QWidget, QPushButton, QSpinBox, QProgressBar, QSizePolicy, QVBoxLayout, QMessageBox, QLabel)
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QTimer
from utils.helpers import run_async
import time
import socket  # Import socket for connection testing
from processAutomationController.processAutomationController import ProcessAutomationController

HOST = "10.0.0.100"  # Motion controller host
PORT = 701           # Motion controller port

class pi_control:
    def __init__(self, output_widget):
        """Initialize the pi_control class with an output widget."""
        if output_widget is None:
            raise ValueError("output_widget must be provided to pi_control")
        self.output_widget = output_widget
        self.pac = None # Placeholder for ProcessAutomationController if needed later

    @staticmethod
    def test_connection(output_widget):
        """Check connection to the motion controller."""
        # This can remain static if needed elsewhere, but pi_connect will use the instance's widget
        try:
            with socket.create_connection((HOST, PORT), timeout=5):
                output_widget.append(f"Connected to {HOST}:{PORT}")
                return True
        except Exception as e:
            output_widget.append(f"Connection failed: {e}")
            return False

    def send_command(self, command):
        """Send a command to the motion controller and display the response."""
        # Now uses self.output_widget
        try:
            # Display the G-code being sent
            self.output_widget.append(f"Sending G-code: {command}")
            print(f"Sending G-code: {command}")  # Print to console for debugging

            # Simulate sending the command (replace with actual implementation)
            # TODO: Replace simulation with actual hardware communication
            response = f"Simulated response for: {command}"
            if response:
                self.output_widget.append(f"Command Sent: {command}")
                self.output_widget.append(f"Response: {response}")

                # Wait for the movement to complete (adjust timing as needed)
                time.sleep(0.5) # Consider making this configurable or based on response

                # Send ?FPOS command to get current position - Recursive call needs fixing
                # For now, commenting out the recursive call to avoid infinite loops
                # position_response = self.send_command("?FPOS") # Recursive call!
                # self.output_widget.append(f"Current Position: {position_response}")
                self.output_widget.append(f"Current Position: Simulated (FPOS check commented out)")

        except Exception as e:
            self.output_widget.append(f"Error sending command '{command}': {e}")
            print(f"Error sending command '{command}': {e}")

    def send_gcode_file(self, file_path):
        """Read G-code from a file and send each line to the controller."""
        # Now uses self.send_command and self.output_widget
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    command = line.strip()
                    if command and not command.startswith(';'): # Ignore empty lines and comments
                        self.send_command(command)
                        # Consider adjusting delay based on command type (e.g., G4 P...)
                        time.sleep(0.2)
        except FileNotFoundError:
            self.output_widget.append(f"Error: G-code file {file_path} not found.")
            print(f"Error: G-code file {file_path} not found.")
        except Exception as e:
            self.output_widget.append(f"Error processing G-code file {file_path}: {e}")
            print(f"Error processing G-code file {file_path}: {e}")

    def pi_connect(self):
        """Connect to the PI controller."""
        # Uses the static test_connection but instance's output_widget
        if self.test_connection(self.output_widget):
            self.output_widget.append("Connected to PI controller")
            print("Connected to PI controller")
        else:
            self.output_widget.append("Failed to connect to PI controller")
            print("Failed to connect to PI controller")

    def pi_enable(self):
        """Enable all axes."""
        # Now uses self.send_command which uses self.output_widget
        self.send_command("ENABLE (X,Y)")
        self.send_command("ENABLE (Z)")

    # Z movements
    def pi_Zhome(self):
        # Corrected to use self.send_command
        self.send_command("N1 G01 Z0 F500 STOP") # Assuming N50 is a label, G-code might just be G01 Z0 F500

    def pi_ZM(self):
        self.send_command("N60 G01 Z-10 F500") # Move Z minus 10 units

    def pi_ZP(self):
        self.send_command("N70 G01 Z10 F500") # Move Z plus 10 units

    # XY movements
    def pi_XYhome(self):
        self.send_command("N70 G01 X0 Y0 F500") # Move to X0 Y0

    def pi_XM(self):
        self.send_command("N20 G01 X-10 F500") # Move X minus 10 units

    def pi_XP(self):
        self.send_command("N30 G01 X10 F500") # Move X plus 10 units

    def pi_YM(self):
        self.send_command("N40 G01 Y-10 F500") # Move Y minus 10 units

    def pi_YP(self):
        self.send_command("N10 G01 Y10 F500") # Move Y plus 10 units

    # --- Placeholder methods for missing functions ---
    def pi_before_layer_start(self):
        self.output_widget.append("Executing: Before Layer Start (Placeholder)")
        print("Executing: Before Layer Start (Placeholder)")
        # Add actual G-code or logic here
        # self.send_command("G-CODE FOR BEFORE LAYER START")

    def pi_after_layer_start(self):
        self.output_widget.append("Executing: After Layer Start (Placeholder)")
        print("Executing: After Layer Start (Placeholder)")
        # Add actual G-code or logic here
        # self.send_command("G-CODE FOR AFTER LAYER START")

    def pi_before_vat_change(self):
        self.output_widget.append("Executing: Before Vat Change (Placeholder)")
        print("Executing: Before Vat Change (Placeholder)")
        # Add actual G-code or logic here
        # self.send_command("G-CODE FOR BEFORE VAT CHANGE")

    def pi_after_vat_change(self):
        self.output_widget.append("Executing: After Vat Change (Placeholder)")
        print("Executing: After Vat Change (Placeholder)")
        # Add actual G-code or logic here
        # self.send_command("G-CODE FOR AFTER VAT CHANGE")

    def macro1(self):
        self.output_widget.append("Executing: Macro 1 (Placeholder)")
        print("Executing: Macro 1 (Placeholder)")
        # Add actual G-code or logic here, potentially using send_gcode_file
        # self.send_gcode_file("path/to/macro1.gcode")

    def macro2(self):
        self.output_widget.append("Executing: Macro 2 (Placeholder)")
        print("Executing: Macro 2 (Placeholder)")
        # Add actual G-code or logic here
        # self.send_gcode_file("path/to/macro2.gcode")
