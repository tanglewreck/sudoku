"""
From a Python shell (3.12.7), do:
    1. import subprocess
    2. import pathlib
    3. python_binary = pathlib.Path("h:/python/3.12.7/python.exe")
    4. run_dir = pathlib.Path("h:/Proj/sudoku/src_kivy")
    5. loop_main = pathlib.Path(f"{run_dir}/loop_main.py")
    6. subprocess.run(f"{python_binary} {loop_main}", shell=True, cwd=run_dir, capture_output=True, text=True)

"""

import pathlib
import subprocess

python_binary = pathlib.Path("h:/python/3.12.7/python.exe")
run_dir = pathlib.Path("h:/Proj/sudoku/src_kivy")

# for k in range(2):
k = 0
while True:
    try:
        k += 1
        print(f"k = {k}")
        output = subprocess.run(f"{python_binary} main.py -a -f --size=1080x1920 --dpi=175 -- -n 1 --solution", cwd=run_dir, capture_output=True, text=True)
        print(output.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Received subprocess.CalledProcessError:", str(e))
        raise SystemExit(127)
    except OSError as e:
        print(f"Received subprocess.CalledProcessError:", str(e))
        raise SystemExit(126)
