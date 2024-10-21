"""
Author: Mikael Eriksson
Date: 2024-10-21

Run main.py as an infinite loop.

After each game, there is a
2 seconds pause so that the loop
can be broken (CTRL-C)

(Yes, this is an ugly way of implementing
'quit the program' functionality, but
that's life (i.e. ugly).


For win32, Python 3.12.7 must be installed as
h:/python/3.12.7/python.exe.

For *nix, the python binary that's in
the user's PATH is used (via the
'which python' shell command).


"""

import pathlib
import subprocess
import sys
import time

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
# while k < 10:
while True:
    try:
        k += 1
        print(f"k = {k}")
        output = subprocess.run(
            f"{python_binary} main.py "
            "-a -f --size=1080x1920 --dpi=175 "
            "-- -n 10 --solution",
            capture_output=True,
            check=True,
            cwd=run_dir,
            shell=True,
            text=True
        )
        print(output.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Received subprocess.CalledProcessError:", str(e))
        raise SystemExit(127)
    except OSError as e:
        print(f"Received subprocess.CalledProcessError:", str(e))
        raise SystemExit(126)
    time.sleep(2)
