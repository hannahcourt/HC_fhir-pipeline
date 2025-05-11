""" Module to set variables to be used throughout the project. """
import os
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RAW_DATA_DIR = os.path.join(ROOT_DIR, 'data/raw')
CURRENT_DATE = datetime.today().strftime('%Y-%m-%d')
PROCESSED_DATA_DIR = os.path.join(ROOT_DIR, f'data/processed/patients_{CURRENT_DATE}')


DATABASE_URL = 'postgresql://testuser:testpass@db:5432/testdb'
TABLE_NAME = "patients"

DATE_COLUMNS = ['birth_date', 'deceased_date']
BOOL_COLUMNS = ['multiple_birth_bool']
PATIENT_RESOURCE_TYPE = 'Patient'

COLUMN_RENAME_MAP = {
   "id": "patient_id",
   "name.0.family": "last_name",
   "name.0.given.0": "first_name",
   "name.0.prefix.0": "name_prefix",
   "name.0.suffix.0": "name_suffix",
   "name.0.use": "name_use",


   "telecom.0.value": "phone",
   "telecom.0.system": "phone_system",
   "telecom.0.use": "phone_use",


   "gender": "gender",
   "birthDate": "birth_date",
   "deceasedDateTime": "deceased_date",


   "address.0.line.0": "address_line",
   "address.0.city": "city",
   "address.0.state": "state",
   "address.0.postalCode": "postal_code",
   "address.0.country": "country",


   "maritalStatus.text": "marital_status",
   "multipleBirthBoolean": "multiple_birth_bool",
   "multipleBirthInteger": "multiple_birth_number",


   "communication.0.language.text": "preferred_language",
   "communication.0.language.coding.0.code": "language_code",
}