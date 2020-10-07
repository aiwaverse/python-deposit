#%%
import shutil
import subprocess
import os
from glob import glob

#%%
racket_folder = "/home/maya/Documents/aiwita/codes/racket/correcao/LISTA6/"
script_folder = "/home/maya/Documents/aiwita/codes/racket/script/"
files_to_copy = [
    "wxme_converter.rkt",
    "insert.sh",
    "lista6/testesLista6.rkt",
    "lista6/insertTests.sh",
    "lista6/testesLista6Exc67.rkt",
]
files_to_delete = [
    "wxme_converter.rkt",
    "insert.sh",
    "testesLista6.rkt",
    "testesLista6.txt",
    "insertTests.sh",
    "testesLista6Exc67.rkt",
    "testesLista6Exc67.txt",
]
os.chdir(racket_folder)
students_folders = glob("**", recursive=False)

#%%
for student_folder in students_folders:
    os.chdir(os.path.join(os.getcwd(), student_folder, ""))
    for file_to_copy in files_to_copy:
        shutil.copy(os.path.join(script_folder, file_to_copy), os.getcwd())
    possible_files = glob("listaCap10*")
    if not possible_files:
        with open("message.txt", "w") as err_file:
            err_file.write("O aluno é burro pra caralho e não nomeou o arquivo certo.")
        continue
    student_file = possible_files[0]
    if " " in student_file:
        os.rename(student_file, student_file.replace(" ", ""))
        student_file = student_file.replace(" ", "")
    student_file_no_ext = student_file.replace(".rkt", "")
    subprocess.run(["sh", "insertTests.sh", student_file, "testesLista6Exc67.rkt"])
    subprocess.run(
        [
            "sh",
            "insert.sh",
            student_file,
            student_file_no_ext + "-testeExc1-5.rkt",
            "testesLista6.rkt",
        ]
    )
    for file_to_delete in files_to_delete:
        os.remove(file_to_delete)
    os.chdir("..")
# %%
