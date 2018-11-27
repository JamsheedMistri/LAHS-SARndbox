import readline
import subprocess
import sys
from collections import OrderedDict
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

# Default directory for SARndbox project
SARNDBOX_DEFAULT_DIR = '/home/user/arsandbox/SARndbox'
CALIBRATE_SCRIPT_LOCATION = '/bin/CalibrateProjector'

TITLE = 'Augmented Reality Sandbox at LAHS'
BLURB = 'Wave your hand with your fingers spread to create rain.\nPress F to flood the sandbox and D to drain.\nMove the light source by dragging, flicking, or scrolling with the mouse.\nAdditional options can be configured below or in the right-click menu.\n\nHave fun! - Adam Weingram & Darryl Yeo, LAHS Class of 2018\n\nModified and improved by Jamsheed Mistri, Nathan MacLeod, Jasper Meggitt, & Kyle Marino, LAHS Class of 2019'

# Default options, can be changed at runtime via command line
options = {
    'verbose': True,    # vruiVerbose
    'use_projector_transform': True, # Always set this to True
    'use_elevation_coloring': True, # Default: True
    'scale_factor': '100', # Default: 100.0
    # 'surface_elevation_range': '-1000 0',   # er
    # 'override_base_plane': '0 0 -100 -1000',    # hmp
    'averaging_slots': '30',    # nas
    'water_speed': '1.0 200', # speed, steps | default: 1.0 30 # Note: you can change this dynamically via the GUI
    'shadows': True,  # us
    'hysteresis_envelope': 0.1,
    'rain_elevation_range': '',
    'rain_strength': '0.5', # default: 0.25
    'evaporation_rate': '-0.008', # default: 0.0 # Note: must be a negative number, or water will explode out of the ground!
    'water_opacity': '1.8', # default: 2.0
    'disable_contour_lines': False, # default: False | Note: If set to True, contour_line_distance must be set to False
    'contour_line_distance': 0.75, # 0.75
    'enable_hill_shading': True, # Random rectangular terrain lines will appear
    'enable_shadows': True, # This doesn't seem to do anything.
}

# Notes to display on the options GUI (comment out to hide)
options_gui_notes = {
    # 'verbose': 'More verbose output on the command line', 
    # 'use_projector_transform': '',
    'use_elevation_coloring': 'Colors the height map.',
    'scale_factor': '100', # Default: 100.0
    # 'surface_elevation_range': '',
    # 'override_base_plane': '',
    # 'averaging_slots': '30',
    'water_speed': 'Format: speed [space] steps\nDefault: 1.0 30\nNote: you can change this dynamically via the GUI.',
    'shadows': '',
    'hysteresis_envelope': 'Makes the water jitter?',
    # 'rain_elevation_range': '',
    'rain_strength': 'How much water flows out of your hand.',
    'evaporation_rate': 'How fast water disappears. Must be a negative number, or water will explode out of the ground!',
    'water_opacity': 'Decrease for more translucent water, increase for more opaque water.',
    'disable_contour_lines': 'If checked, be sure to uncheck "contour line distance" below.',
    'contour_line_distance': 'Height difference between contour lines.',
    'enable_hill_shading': 'Turn on shadows.',
    'enable_shadows': 'This doesn\'t seem to do anything.',
}


# Map nice option name to flag name, and vice versa
option_to_flag = OrderedDict([
    ('verbose', 'vruiVerbose'),
    ('use_projector_transform', 'fpv'),
    ('use_elevation_coloring', 'uhm'),
    ('scale_factor', 's'),
    # ('surface_elevation_range', 'er'),
    # ('override_base_plane', 'hmp'),
    ('averaging_slots', 'nas'),
    ('water_speed', 'ws'),
    ('shadows', 'us'),
    ('hysteresis_envelope', 'he'),
    ('rain_elevation_range', 'rer'),
    ('hysteresis_envelope', 'rs'),
    ('rain_elevation_range', 'evr'),
    ('rain_strength', 'rs'),
    ('evaporation_rate', 'evr'),
    ('water_opacity', 'wo'),
    ('disable_contour_lines', 'ncl'),
    ('contour_line_distance', 'ucl'),
    ('enable_hill_shading', 'uhs'),
    ('enable_shadows', 'us'),
    # ('', ''),
    # ('', ''),
])
flag_to_option = {flag: option for option, flag in option_to_flag.items()}

# Make options order consistent with option_to_flag
options = OrderedDict([
    (option, options[option]) for option in option_to_flag
])


# Read flag form command line
def has_flag(flag):
    return bool(len(sys.argv) > 1 and (flag in sys.argv or '--' + flag in sys.argv))


# Requests user input with pre-filled data
# https://stackoverflow.com/a/36607077
def raw_input_default(prompt, default=''):
    readline.set_startup_hook(lambda: readline.insert_text(default))
    try:
        return input(prompt) or default
    finally:
        readline.set_startup_hook()


# Horizontal line
# https://stackoverflow.com/a/41068447
class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


# Enter options via GUI
def gui_options():
    # Create app

    gui = QApplication(sys.argv)
    window = QWidget()

    grid = QGridLayout()
    grid.setSpacing(10)
    window.setLayout(grid)


    # Title, instructions

    title = QLabel(TITLE)
    title.setFont(QFont('system', 20, QFont.Bold))
    grid.addWidget(title)

    instructions = QLabel(BLURB)
    instructions.setFont(QFont('system', 11))
    grid.addWidget(instructions)


    # Buttons

    def on_calibrate_sandbox_click():
        subprocess.run(SARNDBOX_DEFAULT_DIR + CALIBRATE_SCRIPT_LOCATION, shell=True, stdout=subprocess.PIPE)

    def on_run_sandbox_click():
        window.close()
        run_sandbox()

    def on_exit_click():
        window.close()

    button_grid_widget = QWidget()
    button_grid = QGridLayout()
    button_grid.setSpacing(10)
    button_grid_widget.setLayout(button_grid)

    btn = QPushButton('Exit', window)
    btn.clicked.connect(on_exit_click)
    button_grid.addWidget(btn)

    btn = QPushButton('Calibrate Sandbox', window)
    btn.clicked.connect(on_calibrate_sandbox_click)
    button_grid.addWidget(btn, 0, 1)

    btn = QPushButton('Run Sandbox! (options below)', window)
    btn.clicked.connect(on_run_sandbox_click)
    button_grid.addWidget(btn, 0, 2)
    grid.addWidget(button_grid_widget)


    # Options Grid

    subgrid_widget = QWidget()
    subgrid = QGridLayout()
    subgrid.setSpacing(10)
    subgrid_widget.setLayout(subgrid)


    # Options methods

    def set_option(option, value):
        options[option] = value
        print(option, value)


    def bind_option_to_checkbox(option, checkbox):
        checkbox.stateChanged.connect(lambda: set_option(option, checkbox.isChecked()))


    def bind_option_to_textbox(option, textbox):
        textbox.textChanged.connect(lambda: set_option(option, textbox.text()))


    # Options

    y = 0
    for option, value in options.items():
        if option not in options_gui_notes: continue
        # Option name
        name = QLabel(' '.join(option.split('_')).title())
        subgrid.addWidget(name, y, 0)

        # Checkbox/Text box
        value_input = None
        if type(value) is bool:
            value_input = QCheckBox()
            value_input.setTristate(on=False)
            value_input.setCheckState(Qt.Checked if value is True else Qt.Unchecked)
            bind_option_to_checkbox(option, value_input)
        else:
            value_input = QLineEdit()
            value_input.setText(str(value))
            bind_option_to_textbox(option, value_input)
            value_input.setFixedWidth(50)
            # value_input.setGeometry(0, 0, 200, 50)
        subgrid.addWidget(value_input, y, 1)

        # Option note
        note = QLabel(options_gui_notes[option])
        subgrid.addWidget(note, y, 2)

        y += 1

        # Horizontal line
        subgrid.addWidget(QHLine(), y, 0, 1, 3)

        y += 1
    grid.addWidget(subgrid_widget)

    window.setGeometry(300, 300, 350, 300)
    window.setWindowTitle(TITLE)
    window.show()

    sys.exit(gui.exec_())


# Enter options via command line
def command_line_options():
    # Allows running of system commands
    # https://stackoverflow.com/a/13135985
    def run_command(command):
        p = subprocess.Popen(command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
        return iter(p.stdout.readline, b'')

    # Edit options
    while True:
        print('\nOPTIONS ' + '-' * 42)
        print('\n'.join([
            '{} ({}): '.format(option, option_to_flag[option]).ljust(32) + str(value)
            for option, value in options.items()
        ]))
        print('-' * 50)

        option = input('Press Enter to run, or option name to change option: ')
        if option == '':
            break
        if option not in options and option in flag_to_option:
            option = flag_to_option[option]
        if option in options:
            x = raw_input_default(option + ': ', str(options[option]))
            options[option] = True if x == 'True' else False if x == 'False' else x
            break

# Generate flags, run sandbox program
def run_sandbox(sarndbox_path=SARNDBOX_DEFAULT_DIR + '/bin/SARndbox'):
    # Format options as flags
    flags = [
        '' if not value else
        '-{}'.format(option_to_flag[option]) if value is True else
        '-{} {}'.format(option_to_flag[option], value)
        for option, value in options.items()
    ]


    # The command to be run in bash
    commands = '{} {}'.format(sarndbox_path, ' '.join(flags))
    print('Will run: {}'.format(commands))

    while True:
        # Run the generated SARndbox command and print output
        sarndbox_process = subprocess.run(commands, shell=True, stdout=subprocess.PIPE)
        # Exit infinite loop
        break


# Edit options
if has_flag('gui'):
    print('Running with GUI...')    
    gui_options()
elif has_flag('fast'):
    run_sandbox()
else:
    # Get project directory
    sarndbox_dir = raw_input_default('Enter the path to your SARndbox directory (FULL PATH): ', SARNDBOX_DEFAULT_DIR)
    sarndbox_path = sarndbox_dir + '/bin/SARndbox'
    command_line_options()
    run_sandbox()