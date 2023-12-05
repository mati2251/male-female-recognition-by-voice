import glob
import os
import subprocess

file_paths = sorted(glob.glob("train/*"))

test_number = 0
test_pass = 0

for i in range(2, 8):
    print("Testy dla i = " + str(i))
    test_number = 0
    test_pass = 0
    for file_path in file_paths:
        test_number += 1
        x = subprocess.check_output(["python", "gender-recognition-by-voice/main.py", file_path, str(i)])
        if 'M' in file_path:
            if 'M' in str(x):
                test_pass += 1
        if 'K' in file_path:
            if 'K' in str(x):
                test_pass += 1
    print("Testy zakończone dla i = " + str(i) + " . Wynik: " + str(test_pass) + "/" + str(test_number))