from PyQt5 import uic
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                           QScrollArea, QTextEdit, QFileDialog, QHBoxLayout, QLineEdit, QGridLayout, QDoubleSpinBox)
from PyQt5.QtCore import QTimer
from robotController.modbus.client import ModbusClient
try:
    from robotController.modbus.commands import COMMANDS
except ImportError:
    print("Error: Could not import COMMANDS. Make sure robotController is in the correct location")
    COMMANDS = {}
from robotController.config.settings import MODBUS_ADDRESS, MODBUS_PORT
import subprocess
import os
from robotController.robot_controller import RobotController

class RobotTestingScreen(QWidget):
    def __init__(self, parent=None, modbus_client=None):
        super(RobotTestingScreen, self).__init__(parent)
        self.robot_controller = RobotController(modbus_client)
        self.setup_ui()
        self.setup_timers()

    def setup_ui(self):
        # Create main layout
        self.layout = QVBoxLayout(self)

        # Connection status label
        self.connection_status_label = QLabel("Connection Status: Checking...", self)
        self.layout.addWidget(self.connection_status_label)

        # Status label
        self.status_label = QLabel("Status: Ready", self)
        self.layout.addWidget(self.status_label)

        # Scroll area for buttons
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Create a grid layout for commands and their inputs
        self.scroll_content = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_content)
        
        # Track row number for grid layout
        row = 0
        
        self.command_inputs = {}  # Store input widgets
        
        for command_name, command in COMMANDS.items():
            # Add command label
            label = QLabel(command_name, self)
            self.scroll_layout.addWidget(label, row, 0)
            
            # Create input field and button based on command type
            if command.get("action") == "read_write":
                if command.get("tag_type") == "Real":
                    # For real numbers, use QDoubleSpinBox
                    input_widget = QDoubleSpinBox(self)
                    input_widget.setRange(-999999.99, 999999.99)
                    input_widget.setDecimals(3)
                elif command.get("type") == "coil":
                    # For boolean/coil values, use QPushButton with toggle
                    input_widget = QPushButton("OFF", self)
                    input_widget.setCheckable(True)
                    input_widget.toggled.connect(
                        lambda checked, btn=input_widget: 
                        btn.setText("ON" if checked else "OFF")
                    )
                else:
                    # For other types, use QLineEdit
                    input_widget = QLineEdit(self)
                
                self.scroll_layout.addWidget(input_widget, row, 1)
                self.command_inputs[command_name] = input_widget
                
                # Add send button
                send_button = QPushButton("Send", self)
                send_button.clicked.connect(
                    lambda checked, cmd=command, name=command_name:
                    self.handle_write_command(cmd, name)
                )
                self.scroll_layout.addWidget(send_button, row, 2)
            else:
                # For read-only commands, just add a read button
                read_button = QPushButton("Read", self)
                read_button.clicked.connect(
                    lambda checked, cmd=command: 
                    self.handle_read_command(cmd)
                )
                self.scroll_layout.addWidget(read_button, row, 1, 1, 2)
            
            row += 1

        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

        # Response area
        self.response_area = QTextEdit(self)
        self.response_area.setReadOnly(True)
        self.layout.addWidget(self.response_area)

        # Axis data label
        self.axis_data_label = QLabel("Axis Data: Not Available", self)
        self.layout.addWidget(self.axis_data_label)

        # Add G-code input section
        gcode_layout = QHBoxLayout()
        
        # Create line edit for G-code input
        self.gcode_input = QLineEdit(self)
        self.gcode_input.setPlaceholderText("Enter Gcode To Send...")
        gcode_layout.addWidget(self.gcode_input)
        
        # Create send G-code button
        self.send_gcode_button = QPushButton("Send Gcode", self)
        self.send_gcode_button.clicked.connect(self.send_gcode_input)
        gcode_layout.addWidget(self.send_gcode_button)
        
        self.layout.addLayout(gcode_layout)

        # File selection button
        self.send_gcode_file_button = QPushButton("Send G-code File", self)
        self.send_gcode_file_button.clicked.connect(self.send_gcode_file)
        self.layout.addWidget(self.send_gcode_file_button)

    def setup_timers(self):
        # Connection status timer
        self.connection_timer = QTimer(self)
        self.connection_timer.timeout.connect(self.check_connection_status)
        self.connection_timer.start(5000)

        # Axis data timer
        self.axis_data_timer = QTimer(self)
        self.axis_data_timer.timeout.connect(self.fetch_axis_data)
        self.axis_data_timer.start(1000)

    def check_connection_status(self):
        try:
            connected = self.robot_controller.check_connection()
            self.connection_status_label.setText(
                f"Connection Status: {'Connected' if connected else 'Disconnected'}"
            )
        except Exception as e:
            self.connection_status_label.setText(f"Connection Error: {str(e)}")

    def handle_command(self, command):
        try:
            if command["action"] == "read_write":
                value = self.robot_controller.read_register(command)
                self.response_area.append(f"{command['address']} Value: {value}")
            self.robot_controller.send_command(command)
            self.status_label.setText(f"Status: Command sent successfully")
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")

    def handle_write_command(self, command, command_name):
        """Handle writing values to writable commands"""
        try:
            input_widget = self.command_inputs[command_name]
            
            # Get value based on widget type
            if isinstance(input_widget, QDoubleSpinBox):
                value = input_widget.value()
            elif isinstance(input_widget, QPushButton):
                value = input_widget.isChecked()
            else:
                value = input_widget.text()
                
            if command["type"] == "holding":
                self.robot_controller.write_register(command, value)
            elif command["type"] == "coil":
                self.robot_controller.send_command(command)
                
            self.status_label.setText(f"Status: Value written successfully")
            self.response_area.append(f"Wrote {value} to {command_name}")
            
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            self.response_area.append(f"Error writing to {command_name}: {str(e)}")

    def handle_read_command(self, command):
        """Handle reading values from commands"""
        try:
            value = self.robot_controller.read_register(command)
            self.response_area.append(f"{command['address']} Value: {value}")
            self.status_label.setText("Status: Value read successfully")
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            self.response_area.append(f"Error reading: {str(e)}")

    def fetch_axis_data(self):
        try:
            axis_data = self.robot_controller.fetch_axis_data(COMMANDS)
            self.axis_data_label.setText("\n".join(
                f"{name}: {value}" for name, value in axis_data.items()
            ))
        except Exception as e:
            self.axis_data_label.setText(f"Error fetching axis data: {str(e)}")

    def send_gcode_file(self, file_path=None):
        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select G-code File", "", "G-code Files (*.ngc)")
        if file_path:
            try:
                result = self.robot_controller.send_gcode(file_path=file_path)
                if result.returncode == 0:
                    self.status_label.setText("Status: G-code file sent successfully")
                    self.response_area.append(f"File: {file_path}\n{result.stdout}")
                else:
                    self.status_label.setText("Error: Failed to send G-code file")
                    self.response_area.append(f"File: {file_path}\nError: {result.stderr}")
            except Exception as e:
                self.status_label.setText("Error: Failed to send file")
                self.response_area.append(f"Exception: {str(e)}")

    def send_gcode_input(self):
        gcode = self.gcode_input.text().strip()
        if not gcode:
            self.status_label.setText("Error: No G-code entered")
            return

        try:
            result = self.robot_controller.send_gcode(gcode_content=gcode)
            if result.returncode == 0:
                self.status_label.setText("Status: G-code sent successfully")
                self.response_area.append(f"G-code: {gcode}\n{result.stdout}")
            else:
                self.status_label.setText("Error: Failed to send G-code")
                self.response_area.append(f"G-code: {gcode}\nError: {result.stderr}")
        except Exception as e:
            self.status_label.setText("Error: Failed to send G-code")
            self.response_area.append(f"Exception: {str(e)}")

    def cleanup(self):
        """Clean up resources."""
        if hasattr(self, 'modbus_client'):
            self.modbus_client.close()
        if hasattr(self, 'connection_timer'):
            self.connection_timer.stop()
        if hasattr(self, 'axis_data_timer'):
            self.axis_data_timer.stop()