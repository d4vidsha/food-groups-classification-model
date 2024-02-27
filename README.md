# food-groups-classification-model

## Introduction

The goal of this project is to create a model that can predict what food group a specific food item belongs to based on its nutritional information. A $k$-nearest neighbour model is used for prediction and the model is trained on a dataset of food items from [Food Standards Australia New Zealand](https://www.foodstandards.gov.au/science/monitoringnutrients/afcd/Pages/downloadableexcelfiles.aspx).

## File structure

There are four main folders in this repository:

| Folder   | Description                                                          |
|----------|----------------------------------------------------------------------|
| `archive`| Contains old files that are no longer used.                          |
| `data`   | Contains the data files used in our project.                         |
| `report` | Contains the LaTeX source code for our `project_group40.pdf` report. |
| `src`    | Contains the main source code for our project.                       |

## Instructions to run `src` code

This project uses Python 3.11.3. See [Additional requirements](#additional-requirements) for instructions on setting up the correct Python environment and installing dependencies.

### Running the code

1. Run the `preprocessing.ipynb` notebook to preprocess the data.

   This will create a `data/generated` folder containing `preprocessed-data-classification-first.csv`, `preprocessed-data-classification-second.csv` and `preprocessed-data-classification-third.csv`, which are the preprocessed data files used in our project.

2. Run the `knn.ipynb` notebook to train and evaluate the $k$-nearest neighbour model.

   This will generate a few plots and saved to `report/figs`.

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

## Credits

- Victoria Lyngaae
- Mason Sebek
- David Sha
- William Spongberg
