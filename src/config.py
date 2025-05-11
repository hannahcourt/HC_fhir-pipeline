""" Module to set variables to be used throughout the project. """
import os
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RAW_DATA_DIR = os.path.join(ROOT_DIR, 'data/raw')
CURRENT_DATE = datetime.today().strftime('%Y-%m-%d')
PROCESSED_DATA_DIR = os.path.join(ROOT_DIR, f'data/processed/patients_{CURRENT_DATE}')

PATIENT_RESOURCE_TYPE = 'Patient'
