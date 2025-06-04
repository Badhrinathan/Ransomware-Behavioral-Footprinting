# Project Setup Guide

Follow the steps below to set up and run the project in a Python virtual environment.

## 1. Create a Virtual Environment

First, install a virtual environment using Python:

python -m venv finalpro

Note: If you encounter an error related to execution policy on Windows, run the following command in PowerShell as Administrator:

Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

## 2. Activate the Virtual Environment
On Windows (PowerShell or Command Prompt):

.\finalpro\Scripts\activate

## 3. Install Required Packages
Once the virtual environment is activated, install all dependencies with:

pip install -r requirements.txt
## 4. Run the Application
To run the application, execute:

python app.py
