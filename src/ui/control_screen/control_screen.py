from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PyQt5.QtCore import pyqtSignal
from processAutomationController.processAutomationController import ProcessAutomationController
from ui.control_screen.pi_instruments_control_screen.pi_instruments_control_screen import PiInstrumentsControlScreen
from ui.control_screen.robot_control_screen.robot_control_screen import RobotControlScreen

class ControlScreen(QWidget):
    progress_update_signal = pyqtSignal(int)

    def __init__(self, main_window):
        super(ControlScreen, self).__init__(main_window)
        self.main_window = main_window

        # Load the control screen UI
        self.load_ui()

        # Initialize ProcessAutomationController
        self.process_automation_controller = ProcessAutomationController(main_window)

        # Load and add the pi_instruments_control_screen and robot_control_screen to the tabs
        self.load_tabs()

    def load_ui(self):
        try:
            uic.loadUi('src/ui/control_screen/control_screen.ui', self)
            print("ControlScreen UI loaded successfully")
        except Exception as e:
            print(f"Failed to load ControlScreen UI: {e}")

    def load_tabs(self):
        try:
            # Load pi_instruments_control_screen
            pi_tab = self.tabWidget.widget(0)
            # Create an output widget
            self.pi_output_widget = QTextEdit(pi_tab)
            self.pi_output_widget.setReadOnly(True) # Make it read-only

            # Create the control screen, passing the output widget
            self.pi_instruments_screen = PiInstrumentsControlScreen(self, output_widget=self.pi_output_widget)

            # Setup layout for the PI tab
            pi_layout = QVBoxLayout(pi_tab)
            pi_layout.addWidget(self.pi_instruments_screen) # Add the controls
            pi_layout.addWidget(self.pi_output_widget) # Add the output widget below controls
            pi_tab.setLayout(pi_layout)

            # Load robot_control_screen
            robot_tab = self.tabWidget.widget(1)
            self.robot_control_screen = RobotControlScreen(self)
            robot_layout = QVBoxLayout(robot_tab)
            robot_layout.addWidget(self.robot_control_screen)
            robot_tab.setLayout(robot_layout)

            print("Control screen tabs loaded successfully")
        except Exception as e:
            print(f"Failed to load control screen tabs: {e}")

