# A2-Project 40

Group leader: username, name
Members: username, name

## Introduction

TODO: Add a description of the intended use for the code and csv data files.

## File structure

TODO: Add a description of the file structure and use of each file.

| Folder   | Description                                                          |
|----------|----------------------------------------------------------------------|
| `report` | Contains the LaTeX source code for our `project_group40.pdf` report. |
| `src`    | Contains the source code for our project.                            |
| `data`   | Contains the data files used in our project.                         |

## Instructions

This project uses Python 3.11.3. See [Additional requirements for code to run](#additional-requirements) for instructions on setting up the correct Python environment and installing dependencies.

### Running the code

TODO: Add instructions on how to run the code.

## Additional requirements

### Set up Python environment and install dependencies

We will be using the current latest version of Python (v3.11.3 as of 24/04/2023). To install and use the correct version of Python in a virtual environment, follow the steps below on macOS.

1. Install `pyenv`, a Python version manager. See [pyenv's installation guide](https://github.com/pyenv/pyenv#installation).

    ```bash
    brew install pyenv
    ```

2. Install virtualenv, a tool to create isolated Python environments:

    ```bash
    pip install virtualenv
    ```

3. Install Python 3.11.3 using `pyenv`:

    ```bash
    pyenv install 3.11.3
    ```

4. Create a virtual environment using Python 3.11.3:

    ```bash
    virtualenv -p $(pyenv which python3.11.3) venv
    ```

5. Activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```

    Check that the Python version is correct:

    ```bash
    python --version
    ```

    You should see `Python 3.11.3`.

6. Now that you have the correct Python version, install the dependencies into the virtual environment:

    ```bash
    pip install -r requirements.txt
    ```

7. (Optional) To deactivate the virtual environment, run:

    ```bash
    deactivate
    ```
