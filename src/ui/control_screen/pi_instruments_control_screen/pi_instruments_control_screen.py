import logging
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton
from pi_instruments.pi_intruments import pi_control

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class PiInstrumentsControlScreen(QWidget):
    def __init__(self, parent=None, output_widget=None): # Add output_widget parameter
        super(PiInstrumentsControlScreen, self).__init__(parent)
        print("!!!! PiInstrumentsControlScreen initialized")

        # Check if output_widget is provided
        if output_widget is None:
            raise ValueError("output_widget must be provided to PiInstrumentsControlScreen")
        self.output_widget = output_widget # Assign to self

        self.load_ui()
        # Pass the output widget during pi_control initialization
        self.pi_control = pi_control(self.output_widget)
        self.pi_setup_connections()

    def load_ui(self):
        try:
            # Use absolute path to ensure UI file is found
            import os
            ui_file = os.path.join(os.path.dirname(__file__), 'pi_instruments_control_screen.ui')
            uic.loadUi(ui_file, self)
            print("PiInstrumentsControlScreen UI loaded successfully")
        except Exception as e:
            print(f"Failed to load PiInstrumentsControlScreen UI: {e}")
            raise  # This will help see the full error traceback

    def pi_setup_connections(self):
        # Assign each button to an object
        self.piConnectButton = self.findChild(QPushButton, 'piConnect')
        self.piEnableButton = self.findChild(QPushButton, 'piEnableButton')
        self.piBeforeLayerStartButton = self.findChild(QPushButton, 'piBeforeLayerStart')
        self.piAfterLayerStartButton = self.findChild(QPushButton, 'piAfterLayerStart')
        self.piBeforeVatChangeButton = self.findChild(QPushButton, 'piBeforeVatChange')
        self.piAfterVatChangeButton = self.findChild(QPushButton, 'piAfterVatChange')
        self.macro1Button = self.findChild(QPushButton, 'Macro1Button')
        self.macro2Button = self.findChild(QPushButton, 'Macro2Button')
        self.piMoveZMButton = self.findChild(QPushButton, 'piMoveZMButton')
        self.piHomeZButton = self.findChild(QPushButton, 'piHomeZButton')
        self.piMoveZPButton = self.findChild(QPushButton, 'piMoveZPButton')
        self.piMoveXMButton = self.findChild(QPushButton, 'piMoveXMButton')
        self.piMoveXPButton = self.findChild(QPushButton, 'piMoveXPButton')
        self.piHomeXYButton = self.findChild(QPushButton, 'piHomeXYButton')
        self.piMoveYMButton = self.findChild(QPushButton, 'piMoveYMButton')
        self.piMoveYPButton = self.findChild(QPushButton, 'piMoveYPButton')

        # Debug prints to check if buttons are found
        print(f"piConnectButton: {self.piConnectButton}")
        print(f"piEnableButton: {self.piEnableButton}")
        print(f"piBeforeLayerStartButton: {self.piBeforeLayerStartButton}")
        print(f"piAfterLayerStartButton: {self.piAfterLayerStartButton}")
        print(f"piBeforeVatChangeButton: {self.piBeforeVatChangeButton}")
        print(f"piAfterVatChangeButton: {self.piAfterVatChangeButton}")
        print(f"macro1Button: {self.macro1Button}")
        print(f"macro2Button: {self.macro2Button}")
        print(f"piMoveZMButton: {self.piMoveZMButton}")
        print(f"piHomeZButton: {self.piHomeZButton}")
        print(f"piMoveZPButton: {self.piMoveZPButton}")
        print(f"piMoveXMButton: {self.piMoveXMButton}")
        print(f"piMoveXPButton: {self.piMoveXPButton}")
        print(f"piHomeXYButton: {self.piHomeXYButton}")
        print(f"piMoveYMButton: {self.piMoveYMButton}")
        print(f"piMoveYPButton: {self.piMoveYPButton}")

        # Check if all buttons are found
        if not all([
            self.piConnectButton, self.piEnableButton, self.piBeforeLayerStartButton,
            self.piAfterLayerStartButton, self.piBeforeVatChangeButton, self.piAfterVatChangeButton,
            self.macro1Button, self.macro2Button, self.piMoveZMButton, self.piHomeZButton,
            self.piMoveZPButton, self.piMoveXMButton, self.piMoveXPButton, self.piHomeXYButton,
            self.piMoveYMButton, self.piMoveYPButton
        ]):
            raise ValueError("One or more buttons not found in the UI file")

        # Connect buttons to their respective functions
        self.piConnectButton.clicked.connect(self.pi_connect)
        self.piEnableButton.clicked.connect(self.pi_enable)
        self.piBeforeLayerStartButton.clicked.connect(self.pi_before_layer_start)
        self.piAfterLayerStartButton.clicked.connect(self.pi_after_layer_start)
        self.piBeforeVatChangeButton.clicked.connect(self.pi_before_vat_change)
        self.piAfterVatChangeButton.clicked.connect(self.pi_after_vat_change)
        self.macro1Button.clicked.connect(self.macro1)
        self.macro2Button.clicked.connect(self.macro2)
        self.piMoveZMButton.clicked.connect(self.pi_ZM)
        self.piHomeZButton.clicked.connect(self.pi_Zhome)
        self.piMoveZPButton.clicked.connect(self.pi_ZP)
        self.piMoveXMButton.clicked.connect(self.pi_XM)
        self.piMoveXPButton.clicked.connect(self.pi_XP)
        self.piHomeXYButton.clicked.connect(self.pi_XYhome)
        self.piMoveYMButton.clicked.connect(self.pi_YM)
        self.piMoveYPButton.clicked.connect(self.pi_YP)

    # Placeholder methods for button actions
    def pi_connect(self):
        # pi_control now manages its own widget after initialization
        self.pi_control.pi_connect()
        print("Connecting to PI controller...")

    def pi_enable(self):
        # pi_control now manages its own widget
        self.pi_control.pi_enable()
        print("Enabling PI controller...")

    def pi_ZM(self):
        # pi_control now manages its own widget
        self.pi_control.pi_ZM()
        print("Moving Z axis down...")

    def pi_Zhome(self):
        # pi_control now manages its own widget
        self.pi_control.pi_Zhome()
        print("Homing Z axis...")

    def pi_ZP(self):
        # pi_control now manages its own widget
        self.pi_control.pi_ZP()
        print("Moving Z axis up...")

    def pi_XYhome(self):
        # pi_control now manages its own widget
        self.pi_control.pi_XYhome()
        print("Homing XY axes...")

    def pi_XM(self):
        # pi_control now manages its own widget
        self.pi_control.pi_XM()
        print("Moving X axis left...")

    def pi_XP(self):
        # pi_control now manages its own widget
        self.pi_control.pi_XP()
        print("Moving X axis right...")

    def pi_YM(self):
        # pi_control now manages its own widget
        self.pi_control.pi_YM()
        print("Moving Y axis down...")

    def pi_YP(self):
        # pi_control now manages its own widget
        self.pi_control.pi_YP()
        print("Moving Y axis up...")

    def pi_before_layer_start(self):
        # pi_control now manages its own widget
        self.pi_control.pi_before_layer_start()
        print("Before layer start...")

    def pi_after_layer_start(self):
        # pi_control now manages its own widget
        self.pi_control.pi_after_layer_start()
        print("After layer start...")

    def pi_before_vat_change(self):
        # pi_control now manages its own widget
        self.pi_control.pi_before_vat_change()
        print("Before vat change...")

    def pi_after_vat_change(self):
        # pi_control now manages its own widget
        self.pi_control.pi_after_vat_change()
        print("After vat change...")

    def macro1(self):
        # pi_control now manages its own widget
        self.pi_control.macro1()
        print("Executing Macro 1...")

    def macro2(self):
        # pi_control now manages its own widget
        self.pi_control.macro2()
        print("Executing Macro 2...")

