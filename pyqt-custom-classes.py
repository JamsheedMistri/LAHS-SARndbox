import sys
from PyQt5.QtWidgets import *


# Example function
def foo():
    print("foo!")


# Class for simple prompting for options
class Choice(QWidget):
    def __init__(self, question, window_title, options):
        super().__init__()
        buttons = []
        self.init_ui(question, window_title, options, buttons)
        print(buttons)

    def init_ui(self, question, window_title, options, buttons):
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(QLabel(question), 1, 0)

        for index, option in enumerate(options):
            new_button = QPushButton(option[0])
            new_button.clicked.connect(option[1])
            buttons.append(new_button)
            grid.addWidget(new_button, index + 2, 0)

        self.setLayout(grid) 
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle(window_title)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Choice("Would you like to run the sandbox?", "Testing", [["Ok", foo], ["Cancel", foo]])
    sys.exit(app.exec_())