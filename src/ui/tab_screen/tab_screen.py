from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QApplication
from ui.home_screen.home_screen import HomeScreen
from ui.control_screen.control_screen import ControlScreen
from PyQt5.QtWidgets import (QWidget, QPushButton, QSpinBox, QProgressBar, QSizePolicy, QVBoxLayout, QMessageBox, QLabel)
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QTimer
from PyQt5.QtGui import QImage
import numpy as np
from ui.custom_widgets import ImageWidget
from utils.helpers import run_async
import time
from processAutomationController.processAutomationController import ProcessAutomationController
from ui.robot_testing_screen.robot_testing_screen import RobotTestingScreen


class TabScreen(QWidget):
    def __init__(self, main_window):
        super(TabScreen, self).__init__()
        self.main_window = main_window
        # Load the .ui file for tab screen
        try:
            uic.loadUi('src/ui/tab_screen/tab_screen.ui', self)
            print("TabScreen UI loaded successfully")
        except Exception as e:
            print(f"Failed to load TabScreen UI: {e}")

        # Find the QTabWidget
        self.tabWidget = self.findChild(QTabWidget, 'tabWidget')

        # Populate the tabs using the existing containers in the UI file
        self.load_home_tab()
        self.load_parameters_tab()
        self.load_control_tab()
        self.load_robot_testing_tab()

        # Change this line to use QApplication's aboutToQuit signal
        QApplication.instance().aboutToQuit.connect(self.cleanup)

    def load_home_tab(self):
        # Find the existing home tab
        home_tab = self.findChild(QWidget, 'home_tab')
        if home_tab:
            self.home_screen = HomeScreen(self.main_window)
            self.main_window.home_screen = self.home_screen  # Store reference in main_window
            layout = QVBoxLayout(home_tab)
            layout.addWidget(self.home_screen)
            home_tab.setLayout(layout)
        else:
            print("Home tab not found in TabScreen UI")

    def load_parameters_tab(self):
        # Locate the existing parameters tab container (set objectName to "parameters_tab" in Qt Designer)
        parameters_tab = self.findChild(QWidget, 'parameters_tab')
        if parameters_tab:
            from ui.parameters_screen.parameters_screen import ParametersScreen
            self.parameters_screen = ParametersScreen(self.main_window)
            layout = QVBoxLayout(parameters_tab)
            layout.addWidget(self.parameters_screen)
            parameters_tab.setLayout(layout)
        else:
            print("Parameters tab not found in TabScreen UI")

    def load_control_tab(self):
        # Find the existing control tab by its object name as set in Qt Designer (e.g., "controlTab")
        control_tab = self.findChild(QWidget, 'control_tab')
        if control_tab:
            # Import ControlScreen only when needed
            self.control_screen = ControlScreen(self.main_window)
            self.main_window.control_screen = self.control_screen  # Store reference in main_window
            layout = QVBoxLayout(control_tab)
            layout.addWidget(self.control_screen)
            control_tab.setLayout(layout)
        else:
            print("Control tab not found in TabScreen UI")

    def load_robot_testing_tab(self):
        """Create and load the robot testing tab."""
        try:
            robot_testing_tab = QWidget()
            robot_testing_tab.setObjectName('robot_testing_tab')
            
            # Pass the Modbus client from main window
            self.robot_testing_screen = RobotTestingScreen(
                self, 
                modbus_client=self.main_window.modbus_client
            )
            
            layout = QVBoxLayout(robot_testing_tab)
            layout.addWidget(self.robot_testing_screen)
            robot_testing_tab.setLayout(layout)
            
            tab_index = self.tabWidget.addTab(robot_testing_tab, "Robot Testing")
            print(f"Robot Testing tab added successfully at index {tab_index}")
            
        except Exception as e:
            print(f"Failed to load Robot Testing tab: {e}")

    def cleanup(self):
        """Clean up resources for all tabs."""
        if hasattr(self, 'robot_testing_screen'):
            self.robot_testing_screen.cleanup()