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
import sys

#if sys.platform != 'win32':
#    print("This program works on win32 platforms only")
#    raise SystemExit(1)

if sys.platform == "win32":
    python_binary = pathlib.Path("h:/python/3.12.7/python.exe")
    run_dir = pathlib.Path("h:/Proj/sudoku/src_kivy")
elif sys.platform == "darwin" or sys.platform == "linux":
    python_binary = subprocess.run("which python", shell=True, capture_output=True, text=True).stdout.strip()
    run_dir = pathlib.Path(f"{pathlib.os.environ['HOME']}/Proj/sudoku/src_kivy")
    main_prog = run_dir.joinpath("main.py")
    #print(f"python_binary = {python_binary}")
    #print(f"run_dir = {run_dir}")
    #print(f"main_prog = {main_prog}")


# for k in range(2):
k = 0
while k < 10:
    try:
        k += 1
        print(f"k = {k}")
            # f"{python_binary} {main_prog} -a -f --size=1080x1920 --dpi=175 -- -n 1 --solution",
            # f"python {main_prog} -a -f --size=1080x1920 --dpi=175 -- -n 1 --solution",
        output = subprocess.run(
            f"python main.py -a -f --size=1080x1920 --dpi=175 -- -n 1 --solution",
            shell=True,
            cwd=run_dir,
            capture_output=True,
            text=True
        )
        print(output.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Received subprocess.CalledProcessError:", str(e))
        raise SystemExit(127)
    except OSError as e:
        print(f"Received subprocess.CalledProcessError:", str(e))
        raise SystemExit(126)
