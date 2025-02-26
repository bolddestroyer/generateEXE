# EXE File Generator for python files

This project provides a graphical user interface (GUI) application to convert Python scripts into standalone executable (EXE) files using PyInstaller. The application is built using the `tkinter` library for the GUI and leverages the `subprocess` module to run PyInstaller commands.

## Key Features:

- **GUI Interface**: The application provides a user-friendly interface to select Python files and generate EXE files.
- **Package Status Check**: The application checks if PyInstaller is installed and if there are any updates available for PyInstaller and pip.
- **Syntax Check**: Before generating the EXE file, the application checks the selected Python file for syntax errors.
- **Custom Message Box**: After generating the EXE file, a custom message box is displayed with options to close the message box or open the directory containing the generated EXE file.
- **File Explorer Integration**: The application allows users to browse for Python files and open the directory containing the generated EXE file directly from the GUI.

## How It Works:

- **Main Application**: The main application logic is contained in `main.py`. It includes functions for checking package status, getting the Python version, generating the EXE file, and handling file selection and message boxes.
- **GUI Setup**: The `app_window` function sets up the main application window with buttons for browsing files and generating the EXE file.
- **Execution**: The `generateEXE.py` file imports the necessary functions from `main.py` and runs the `app_window` function to start the application.

## Installation:

#### 1. Open the command prompt (CMD)

#### 2. Check if you have Python installed

Execute the following command in CMD:

```sh
python --version
```

If the output is `Python X.XX.X` (where X.XX.X are substituted by numbers indicating version, e.g. 3.13.2), then Python is installed on your machine.
Check if you have the newest available version.

```sh
winget search --id Python.Python
```

If a newer version is available, update using the following command (however, this is not mandatory):

```sh
winget install --id Python.Python.X.XX --source winget --upgrade
```

:grey_exclamation: (substitute `X.XX` by version, e.g. 3.13)

If the output does not indicate the version, then Python is not installed.
Install Python using the following command:

```sh
winget install Python.Python.X.XX --source winget
```

:grey_exclamation: (substitute `X.XX` by version, e.g. 3.13)

3. Navigate to the Documents directory:

```sh
cd C:\Users\<your_user_name>\Documents
```

4. Clone the repository:
   ```sh
   git clone https://github.com/bolddestroyer/generateEXE.git
   ```
5. Navigate to the directory where the repository is located:
   ```sh
   cd generateEXE
   ```
6. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Execution:

1. Run the **generateEXE.py** file:
   ```sh
   python generateEXE.py
   ```
2. Use the `Browse` button to select a Python file.
3. Click the `Generate` button to generate the EXE file.
4. A message box will appear indicating the success of the operation and providing options to close the message box or open the directory containing the generated EXE file.
