import os
import subprocess


folders = subprocess.check_output(["fdfind -t d"], shell=True).decode("utf-8").strip().split()
cwd = os.getcwd()
for folder in folders:
  os.chdir(cwd + "/" + folder)
  files_in_dir = subprocess.check_output(["ls"]).decode("utf-8").strip().split()
  files_single_string = " ".join(files_in_dir)
  command = f"convert {files_single_string} +append {os.getcwd()}.jpg"
  os.system(command)
  os.chdir("..")