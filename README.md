# TellCo-Data-Analysis

**Table of Contents**

- [TellCo-Data-Analysis](#TellCo-Data-Analysis)
  - [Overview](#overview)
  - [Scenario](#scenario)
  - [Approach](#approach)
  - [Project Structure](#project-structure)
    - [data:](#data)
    - [models](#models)
    - [notebooks](#notebooks)
    - [scripts](#scripts)
    - [root folder](#root-folder)
  - [Installation guide](#installation-guide)

## Overview
In this repository I have analyzed a telecomunications dataset of a company called TellCo. This project is part of 10 academy's training week 1 challenge. The project's objective is to analyze opportunities for growth and make a recommendation on whether TellCo is worth investing.

## Scenario
You are working for a wealthy investor that specializes in purchasing assets that are undervalued. The investor is interested in purchasing TellCo, an existing mobile service provider in the Republic of Pefkakia. You will analyze a telecommunication dataset that contains useful information about the customers & their activities on the network.

## Approach
The project is divided and implemented by the following phases
1. User Overview analysis
2. User Engagement analysis
3. User Experience analysis
4. User Satisfaction analysis
5. Serving results of the analyses on a web dashboard

## Project Structure
The repository has a number of files including python scripts, jupyter notebooks, pdfs and text files. Here is their structure with a brief explanation.

### data:
- the folder where the dataset csv files are stored

### models:
- the folder where models' pickle files are stored

### notebooks:
- `User Overview analysis.ipynb`: a jupyter notebook that analyzes general users' behaviours
- `User Engagement analysis.ipynb`: a jupyter notebook that analyzes the engagement of users
- `User Experience analysis.ipynb`: a jupyter notebook that analyzes users' network experience
- `User Satisfaction analysis.ipynb`: a jupyter notebook that analyzes the satisfaction of users

### scripts
- `df_cleaner.py`: a python script for cleaning pandas dataframes
- `df_selector.py`: a python script for selecting data from a pandas dataframe
- `df_visualizer.py`: a python script for plotting selected data
- `df_outlier_handler.py`: a python script for cleaning outliers in  a pandas dataframe

### root folder
- `10 Academy Batch 4 - Week 1 Challenge.pdf`: the challenge document
- `requirements.txt`: a text file lsiting the projet's dependancies
- `.gitignore`: a text file listing files and folders to be ignored
- `travis.yml`: a configuration file for Travis CI
- `setup.py`: a configuration file for installing the scripts as a package
- `tellco_analysis_dashboard.py`: a python script for streamlit dashboard
- `README.md`: Markdown text with a brief explanation of the project and the repository structure.

## Installation guide
```
git clone https://github.com/zelalemgetahun9374/TellCo-Data-Analysis
cd TellCo-Data-Analysis
pip install -r requirements.txt
```
