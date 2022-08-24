# code-dojo

This repository is meant to store Jupyter Notebooks going over various special topics in Python.

## Environment

You can use whichever virtual environment you prefer. I personally use conda, so my environment is set up as follows:

```bash
(base) ~/code/code-dojo conda create -n code-dojo python=3.10 -y
(base) ~/code/code-dojo conda activate code-dojo
(code-dojo) ~/code/code-dojo python3 -m pip install -r requirements.txt
```

I recommend you use Python v3.10 as I will be going over more recent changes to Python in later sessions

## Running Notebooks

All sessions are stored in Jupyter Notebooks that can be cloned and run locally. After installing the dependencies in `requirements.txt`
you will have access to Jupyter Notebooks, so to run any session, all you have to do is:

```bash
(code-dojo) ~/code/code-dojo cd modules 
(code-dojo) ~/code/code-dojo/modules jupyter-notebook
```
