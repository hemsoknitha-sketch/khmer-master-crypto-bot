import sys, traceback
def excepthook(type, value, tb):
    print("UNHANDLED EXCEPTION:", file=sys.stderr)
    traceback.print_exception(type, value, tb)
    sys.__excepthook__(type, value, tb)

sys.excepthook = excepthook

from PyQt5.QtWidgets import QApplication
import main

app = QApplication(sys.argv)
window = main.BotDashboard()
window.start_system()
sys.exit(app.exec_())
