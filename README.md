# Flow Rate Calculator for Medical Infusions

A simple and intuitive desktop application built with Python and `ttkbootstrap` to calculate the required flow rate (ml/h) for continuous medical infusions.

This tool is designed to assist healthcare professionals by simplifying the calculation of drug dosages based on patient weight, desired dose, and solution concentration.

![Screenshot of the application](https://ibb.co/6RpWJQ1z)


## Features

-   **Easy-to-use Interface:** A clean and modern UI for quick data entry.
-   **Accurate Calculations:** Implements the standard formula for calculating infusion flow rates in ml/h.
-   **Standard Infusions Table:** Includes a reference table with standard concentrations for common drugs like Dopamine, Noradrenaline, and more.
-   **Cross-platform:** Can be run on Windows, macOS, and Linux.
-   **Standalone Executable:** Can be easily packaged into a single executable file for distribution.

## Formula Used

The application calculates the required flow rate using the following formula:

$$ \text{Flow Rate (ml/h)} = \frac{\text{Dose (mcg/kg/min)} \times \text{Weight (kg)} \times 60 \text{ (min/h)}}{\text{Concentration (mcg/ml)}} $$

Where:

$$ \text{Concentration (mcg/ml)} = \frac{\text{Total Drug (mg)} \times 1000 \text{ (mcg/mg)}}{\text{Volume (ml)}} $$

## Technologies Used

-   **Python 3**
-   **Tkinter** (via `ttkbootstrap` for modern styling)
-   **ttkbootstrap:** For modern and themed Tkinter widgets.
-   **Pillow:** For image processing (used for the banner).

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Você precisará criar um arquivo `requirements.txt` com o conteúdo abaixo)*

4.  **Run the application:**
    ```bash
    python vazao.py
    ```

### `requirements.txt` file

Create a file named `requirements.txt` in the root of your project with the following content:

```
ttkbootstrap
Pillow
```

## Building the Executable

You can create a standalone executable file using **PyInstaller**.

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Build the .exe:**
    Run the following command from your terminal in the project's root directory. Make sure to include your icon and banner files.
    ```bash
    pyinstaller --onefile --windowed --icon=icone.ico --add-data "banner.png;." vazao.py
    ```
    -   `--onefile`: Creates a single executable file.
    -   `--windowed`: Prevents the command prompt from appearing when you run the app.
    -   `--icon=icone.ico`: Sets the application icon.
    -   `--add-data "banner.png;."`: Ensures the banner image is included in the executable.

The final executable will be located in the `dist` folder.

## Author

-   **Edvaldo** - *Project creator*
