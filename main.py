import os
import py_compile
import re
import shutil
import subprocess
import sys
from tkinter import filedialog, messagebox
import tkinter


def checkPackageStatus():
    try:
        pyinstaller_version_result = subprocess.run("python -m PyInstaller --version", capture_output=True, text=True)
        if "No module named PyInstaller" in pyinstaller_version_result.stderr:
            print("PyInstaller is not installed.")

        outdated_packages_result = subprocess.run("pip list --outdated", capture_output=True, text=True)
        for package in outdated_packages_result.stdout.splitlines():
            if "pyinstaller" in package:
                print("New version of PyInstaller is available.")
            if "pip" in package:
                print("New version of pip is available.")

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        messagebox.showerror("Package error", "Error: {e}")
        # In case of errors, show message box and return nothing (stop the process)
        return


def getPythonVersion():
    python_version_version = subprocess.run("python --version", capture_output=True, text=True)
    extract_version = re.search(r"Python (\d+\.\d+)", python_version_version.stdout)
    return extract_version.group(1)


def generateEXEfile(pyfile_path):
    checkPackageStatus()

    # Regexp for a python file
    regexp_pyfile = re.compile(".*.py$")

    # If python file is selected
    if regexp_pyfile.search(pyfile_path):
        try:
            # Check if selected python file has got no syntax errors
            py_compile.compile(pyfile_path, doraise=True)
        except py_compile.PyCompileError as e:
            messagebox.showerror("Syntax Error", f"Error: {e}.")
            # In case of errors, show message box and return nothing (stop the process)
            return

        working_directory = os.path.join(os.path.expanduser("~"), r"Documents\VSCode\_exe", os.path.splitext(os.path.basename(pyfile_path))[0])

        # If working directory exists, remove with all its content
        if os.path.exists(working_directory):
            shutil.rmtree(working_directory)

        os.makedirs(working_directory)
        # Change the working directory
        os.chdir(working_directory)

        python_version = getPythonVersion()
        python_version_without_dot = python_version.replace(".", "")
        pyinstaller_path = rf"C:\Users\doria\AppData\Local\Packages\PythonSoftwareFoundation.Python.{python_version}_qbz5n2kfra8p0\LocalCache\local-packages\Python{python_version_without_dot}\Scripts\pyinstaller.exe"

        # Run the command
        subprocess.run(f"{pyinstaller_path} --onefile {pyfile_path}")
        custom_messagebox(working_directory)

    # If no file is selected
    elif pyfile_path == "No file selected":
        messagebox.showerror("Error", "Select a file first.")

    # If selected file is not a python file
    elif not regexp_pyfile.search(pyfile_path):
        messagebox.showerror("Error", "Only python files can be processed (extension '.py').")


def openFileExplorer(label):
    # Open the file explorer, save file path as a variable
    file_path = filedialog.askopenfilename()
    if file_path:
        # Set the file path as new text for the label
        label.config(text=file_path)


# Open the file explorer with the directory of the generated EXE file
def openFileLocation(pyfile_path):
    os.startfile(os.path.dirname(pyfile_path))
    sys.exit()


# Custom message box with buttons to close and open the file explorer
def custom_messagebox(pyfile_path):
    # Top-level pop-up window
    msg_box = tkinter.Tk()
    msg_box.title("Info")

    # Label
    lbl_message = tkinter.Label(msg_box, text="The EXE file was created successfully.")
    lbl_message.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Button - close the message box
    btn_ok = tkinter.Button(msg_box, text="OK", command=lambda: sys.exit())
    btn_ok.grid(row=1, column=0, padx=10, pady=10)

    # Button - open directory in the file explorer with the generated EXE file
    btn_open_explorer = tkinter.Button(msg_box, text="Open EXE file location", command=lambda: openFileLocation(pyfile_path))
    btn_open_explorer.grid(row=1, column=1, padx=10, pady=10)


def appWindow():
    window = tkinter.Tk()
    window.title("Create an EXE file")

    # Label with the file path
    label_dir = tkinter.Label(window, text="No file selected")
    label_dir.grid(row=0, column=0, padx=10, pady=10)

    # Button - execute openFileExplorer; search for a file
    btn_brow_file = tkinter.Button(window, text="Browse", command=lambda: openFileExplorer(label_dir))
    btn_brow_file.grid(row=0, column=1, padx=10, pady=10)

    # Button - execute createEXEfile; create the EXE file; value in the label (file path) as an input
    btn_execute = tkinter.Button(window, text="Create the EXE file", command=lambda: generateEXEfile(label_dir.cget("text")))
    btn_execute.grid(row=1, column=0, padx=10, pady=10)

    # Loop the window, refresh after each change (e.g. change of value in label)
    window.mainloop()
