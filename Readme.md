
Overview:
This repository contains working  on a relative big application  called pipeline. The process has been divided in several classes such as dataset_loader, pipeline_model, pipeline_production that work independently and are used as module in the main script. In the classed definition we used interface seggregation, inheritance, lisko substituion principle, Dependency inversion principle, paralization and generator.
The pipeline data has been loaded by data_loader moduel following by spliting the data in train and test sections, transforming the trained data following by training  the model. After evaluating the model, it will be used as a model to predict the future data.


Purpose:
Develop a functional anomaly detection pipeline that can process new incoming data, make predictions, and produce visualizations while maintaining a detailed log of its operations.

Methodology:
- Business understanding
- Data underestanding
- Data prepration
- Modeling
- Evalution
- Development

Data process:
- Data Preparation(Download, removing nan values, Split Data,Save these splits as separate files)

- Model Creation and Transformation(Train the Model,Use the training data (April to June) to train a model for anomaly detection,transformations, training model and saving)

- Refactor Plotting Function(Refactor to Remove dependency on global variables,Return the plot instead of displaying it)
 
- Model Evaluation

- Production Pipeline



Files:
kaggle.jason
application.jason
dataset_loader.py(as module)
pipeline_model.py(as module)
pipeline_production.py(as module)
model.joblib
main_modified.ipynb

'sensor.csv'  can be loaded by:
https://www.kaggle.com/datasets/nphantawee/pump-sensor-data



Conclusion:
By creating independent developed classes we could do all the process such as loading, splitting, transforming the data and training the  the model for  pipeline and use this model for detecting anomalies for future data.

How to Use:
Clone the repository.
Ensure required dependencies are installed.
Execute 'main_modified.ipynb' in a Jupyter Notebook environment.

#install required packages:
import os
import joblib
import pandas as pd
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
from dataset_loader import DatasetDownloader
from pipeline_model import ModelPipeline
from production_pipeline import ProductionPipeline
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pipeline_model import ModelPipeline
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional




Author
F. Monfared f.monfared@st.hanze.nl
  

