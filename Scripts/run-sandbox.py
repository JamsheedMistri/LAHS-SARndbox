import readline
import subprocess
import sys
from collections import OrderedDict

# Default directory for SARndbox project
SARNDBOX_DEFAULT_DIR = '/home/user/arsandbox/SARndbox'

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
    'rain_strength': '1', # default: 0.25
    'evaporation_rate': '-0.005', # default: 0.0 # Note: must be a negative number, or water will explode out of the ground!
    'water_opacity': '2.0', # default: 2.0
    'disable_contour_lines': True, # default: False | Note: If set to True, contour_line_distance must be set to False
    'contour_line_distance': 0.75, # 0.75
    'enable_hill_shading': True, # Random rectangular terrain lines will appear
    'enable_shadows': False, # This doesn't seem to do anything.
    # '': '',
    # '': '',
    # '': '',
    
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
    # ('', ''),
    # ('', ''),
    # ('', ''),
])
flag_to_option = {flag: option for option, flag in option_to_flag.items()}

# Make options order consistent with option_to_flag
options = OrderedDict([
    (option, options[option]) for option in option_to_flag
])


# Requests user input with pre-filled data
# https://stackoverflow.com/a/36607077
def raw_input_default(prompt, default=''):
    readline.set_startup_hook(lambda: readline.insert_text(default))
    try:
        return input(prompt) or default
    finally:
        readline.set_startup_hook()


# Allows running of system commands
# https://stackoverflow.com/a/13135985
def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')


if (len(sys.argv) > 1 and (sys.argv[1] == "fast" or sys.argv[1] == "--fast")):
    # Run using default values
    sarndbox_path = SARNDBOX_DEFAULT_DIR + '/bin/SARndbox'
else:
    # Get project directory
    sarndbox_dir = raw_input_default('Enter the path to your SARndbox directory (FULL PATH): ', SARNDBOX_DEFAULT_DIR)
    sarndbox_path = sarndbox_dir + '/bin/SARndbox'

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
    kinect_reset_process = None
    sarndbox_process = None

     # Run the Kinect reset command
    try:
        kinect_reset_process = subprocess.run("KinectUtil reset all", shell=True, timeout=1)
    except subprocess.TimeoutExpired:
        if kinect_reset_process is not None: kinect_reset_process.kill()
        print('Failed to connect to Kinect. Trying again...')
        continue
        
    # Run the generated SARndbox command and print output
    sarndbox_process = subprocess.run(commands, shell=True, timeout=5)
    """
    try:
        sarndbox_process = subprocess.run(commands, shell=True, timeout=5)
    except subprocess.TimeoutExpired:
        if sarndbox_process is not None: sarndbox_process.kill()
        print('Failed to run SARndbox. Trying again...')
        continue
    """
    
    # Exit infinite loop
    break
