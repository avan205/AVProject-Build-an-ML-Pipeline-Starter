import argparse
import loggin
import json
import tempfile
import os 

import mlflow
import wandb
import pandas as pandas

from sklearn.compose import ColumnTransformer
from skleearn.impute import SimpleImputer
from sklearn.pipeline import pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO, format=%)