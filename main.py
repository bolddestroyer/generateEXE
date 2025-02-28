import ctypes
from datetime import *
import os
import py_compile
import re
import shutil
import subprocess
import sys
import time
from tkinter import filedialog, messagebox
import tkinter
import win32gui


def check_package_status():
    try:
        pyinstaller_version_result = subprocess.run("python -m PyInstaller --version", capture_output=True, text=True)
        if "No module named PyInstaller" in pyinstaller_version_result.stderr:
            print("PyInstaller is not installed.")

        outdated_packages_result = subprocess.run("pip list --outdated", capture_output=True, text=True)
        for package in outdated_packages_result.stdout.splitlines():
            if "pyinstaller" in package:
                print("A new version of PyInstaller is available.")
            if "pip" in package:
                print("A new version of pip is available.")

    except (subprocess.CalledProcessError, FileNotFoundError, Exception) as e:
        messagebox.showerror("Package error", "Error: {e}")
        return


def get_python_version():
    try:
        python_version_result = subprocess.run("python --version", capture_output=True, text=True)
        python_version = re.search(r"Python (\d+\.\d+)", python_version_result.stdout)
        return python_version.group(1)
    except (
        subprocess.CalledProcessError,
        FileNotFoundError,
        subprocess.SubprocessError,
        re.error,
    ) as e:
        messagebox.showerror("Python error", f"Error: {e}")
        return


def generate_exe_file(python_file_path):
    start_time = time.time()
    python_file_regexp = re.compile(".*.py$")

    check_package_status()

    if python_file_regexp.search(python_file_path):
        print(python_file_path)
        try:
            py_compile.compile(python_file_path, doraise=True)
        except py_compile.PyCompileError as e:
            messagebox.showerror("Error", f"Error with the selected file:\n{e}.")
            return

        output_file_name = os.path.splitext(os.path.basename(python_file_path))[0]
        working_directory = os.path.join(
            os.path.expanduser("~"),
            r"Documents\generateEXE",
            output_file_name,
        )

        if os.path.exists(working_directory):
            shutil.rmtree(working_directory)

        os.makedirs(working_directory)
        os.chdir(working_directory)

        if working_directory not in os.getcwd():
            messagebox.showerror("Error", f"Issue with the working directory: {working_directory}")
            return

        python_version = get_python_version()
        python_version_no_dot = python_version.replace(".", "")
        pyinstaller_executable_path = os.path.join(
            os.path.expanduser("~"),
            rf"AppData\Local\Packages\PythonSoftwareFoundation.Python.{python_version}_qbz5n2kfra8p0\LocalCache\local-packages\Python{python_version_no_dot}\Scripts\pyinstaller.exe",
        )

        if not os.path.exists(pyinstaller_executable_path):
            messagebox.showerror("Error", f"Issue with the PyInstaller directory:\n{pyinstaller_executable_path}")
            return

        subprocess.run(f"{pyinstaller_executable_path} --onefile --noconsole {python_file_path}")

        exe_output_directory = os.path.join(working_directory, "dist", "")
        exe_output_directory_log = os.path.join(working_directory, "dist")
        execution_timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
        processing_duration = time.time() - start_time
        with open(os.path.join(exe_output_directory, "info.txt"), "w") as info_file:
            info_file_content = (
                f"-----------------------------WELCOME TO generateEXE------------------------------\n"
                f"Execution date and time: {execution_timestamp}\n"
                f"Processing duration: {processing_duration:.0f} seconds\n\n"
                f"The EXE file {output_file_name}.py was generated successfully.\n"
                f"Path of the executable file: {exe_output_directory_log}.\n\n\n"
                f"GIT repository: https://github.com/bolddestroyer/generateEXE.git"
            )
            info_file.write(info_file_content)

        custom_messagebox(exe_output_directory)

    elif python_file_path == "No file selected":
        messagebox.showerror("Error", "Select a file.")

    elif not python_file_regexp.search(python_file_path):
        messagebox.showerror("Error", "Only Python files can be processed (extension '.py').")


def open_file_explorer(label):
    file_path = filedialog.askopenfilename()
    if file_path:
        label.config(text=file_path)


def open_exe_file_directory(python_file_path):
    os.startfile(os.path.dirname(python_file_path))
    sys.exit()


def custom_messagebox(python_file_path):
    window = tkinter.Tk()
    window.title("Info")
    window.attributes("-topmost", True)

    lbl_message = tkinter.Label(window, text="The EXE file was created successfully.")
    lbl_message.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    btn_ok = tkinter.Button(window, text="OK", command=lambda: sys.exit())
    btn_ok.grid(row=1, column=0, padx=10, pady=10)

    btn_open_explorer = tkinter.Button(
        window, text="Go to the file directory", command=lambda: open_exe_file_directory(python_file_path)
    )
    btn_open_explorer.grid(row=1, column=1, padx=10, pady=10)


def app_window():
    window_title = "generateEXE"

    window = tkinter.Tk()
    window.title(window_title)

    label_selected_file = tkinter.Label(window, text="Select a file")
    label_selected_file.grid(row=0, column=0, padx=10, pady=10)

    btn_browse = tkinter.Button(window, text="Browse", command=lambda: open_file_explorer(label_selected_file))
    btn_browse.grid(row=0, column=1, padx=10, pady=10)

    btn_generate = tkinter.Button(
        window, text="Generate", command=lambda: generate_exe_file(label_selected_file.cget("text"))
    )
    btn_generate.grid(row=1, column=0, padx=10, pady=10)

    window.mainloop()
