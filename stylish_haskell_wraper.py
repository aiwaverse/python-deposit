import subprocess
import sys

def parse_composition(old_file,new_file):
    with open(old_file, "r") as f:
        f.read()


file_name = list(sys.argv)[1]
command   = ["stylish-haskell", file_name]
output    = subprocess.check_output(command)


