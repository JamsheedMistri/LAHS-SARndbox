import subprocess

# run_sandbox_bash = """
# ./bin/SARndbox \\ \n
# -vruiVerbose \\ \n
# -fpv \\ \n
# -uhm \\ \n
# -s 100.0 \\ \n
# -er -1000 0 \\ \n
# -hmp 0 0 -100 -1000 \\ \n
# -nas 30 \\ \n
# -ws 0.8 10 \\ \n
# -us
# """
verbose = " -vruiVerbose"
projector_transform = " -fpv"
elevation_color_map = " -uhm"
scale_factor = " -s"    # NEEDS AN INPUT
surface_elevation_range = " -er"    # NEEDS AN INPUT
explicit_base_pane = " -hmp"    # NEEDS AN INPUT
averaging_slots = " -nas"   # NEEDS AN INPUT
water_speed = " -ws"    # NEEDS AN INPUT
enable_shadows = " -us"

sarnbox_path = input("Enter the path to your SARndbox directory: ")
options = verbose + projector_transform  # User "Editable"

# The command to be run in bash
run_sandbox_bash = "cd {} && ./bin/SARndbox {}".format(sarnbox_path, options)

# Actually run the command:
process = subprocess.Popen(run_sandbox_bash.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
