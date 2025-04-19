from PyQt5.QtCore import QObject, pyqtSignal
from utils.helpers import run_async
import time
import  pi_instruments

# TBD clean play pause process. use printer printing status to diferentiate between control and main printing sequence

class ProcessAutomationController(QObject):
    progress_update_signal = pyqtSignal(int)
    
    def __init__(self, main_window):
        super(ProcessAutomationController, self).__init__()
        self.main_window = main_window
        self.process_running = False

        # Connect the progress update signal to the slot
        self.progress_update_signal.connect(self.update_progress_bar)

    def update_progress_bar(self, value):
        """Slot to update the progress bar value."""
        self.main_window.home_screen.printProgressBar.setValue(value)

    def stop_process(self):
        """Stop the recoat process."""
        self.process_running = False
        self.main_window.home_screen.playPauseButton.setChecked(False)
        self.progress_update_signal.emit(0)

