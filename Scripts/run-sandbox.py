import readline
import subprocess
import sys
from collections import OrderedDict

# Default directory for SARndbox project
SARNDBOX_DEFAULT_DIR = '/home/user/arsandbox/SARndbox'

# Default options, can be changed at runtime via command line
options = {
    'verbose': True,    # vruiVerbose
    'use_projector_transform': True,    # fpv
    'use_elevation_color_map': True,    # uhm
    'scale_factor': '100.0',    # s
    'surface_elevation_range': '-1000 0',   # er
    'override_base_plane': '0 0 -100 -1000',    # hmp
    'averaging_slots': '30',    # nas
    'water_speed': '0.8 10',    # ws
    'shadows': True,  # us
}


# Map nice option name to flag name, and vice versa
option_to_flag = OrderedDict([
    ('verbose', 'vruiVerbose'),
    ('use_projector_transform', 'fpv'),
    ('use_elevation_color_map', 'uhm'),
    ('scale_factor', 's'),
    ('surface_elevation_range', 'er'),
    ('override_base_plane', 'hmp'),
    ('averaging_slots', 'nas'),
    ('water_speed', 'ws'),
    ('shadows', 'us'),
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
commands = [
    '{} {}'.format(sarndbox_path, ' '.join(flags))
]
print('Will run: {}'.format(commands))

kinect_reset_process = subprocess.Popen("KinectUtil reset all".split(), stdout=subprocess.PIPE)
output, error = kinect_reset_process.communicate()

for line in run_command(commands):
    print(line)


# Run the command
# process = subprocess.Popen(commands.split(), stdout=subprocess.PIPE)
# output, error = process.communicate()
