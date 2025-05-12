""" Module to transfrom and process raw data."""
import pandas as pd
from config import PATIENT_RESOURCE_TYPE, COLUMN_RENAME_MAP
import pandera as pa 

def flatten_dict(d, parent_key='', sep='.'):
   """
   Recursively flattens a nested dictionary into a single-level dictionary.
  
   Args:
       d (dict): The dictionary to flatten.
       parent_key (str, optional): The base key to prefix nested keys. Defaults to an empty string.
       sep (str, optional): The separator used to join parent and child keys. Defaults to a period ('.').


   Returns:
       dict: A flattened version of the input dictionary with concatenated keys.
   """
   items = []
   for k, v in d.items():
       new_key = f"{parent_key}{sep}{k}" if parent_key else k
       if isinstance(v, dict):
           items.extend(flatten_dict(v, new_key, sep=sep).items())
       elif isinstance(v, list):
           for i, item in enumerate(v):
               if isinstance(item, dict):
                   items.extend(flatten_dict(item, f"{new_key}.{i}", sep=sep).items())
               else:
                   items.append((f"{new_key}.{i}", item))
       else:
           items.append((new_key, v))
   return dict(items)


def transform_resources(fhir_data):
   """
   Extracts and flattens the specified resource type from a list of FHIR bundles.
  
   Args:
       fhir_data (list): A list of FHIR bundles, where each bundle may contain the specified resource type.


   Returns:
       pd.DataFrame: A DataFrame containing the flattened resource data.
   """
   records = []
   for bundle in fhir_data:
       if bundle.get('resourceType') == 'Bundle':
           for entry in bundle.get('entry', []):
               resource = entry.get('resource', {})
               if resource.get('resourceType') == PATIENT_RESOURCE_TYPE:
                   flat_resource_type = flatten_dict(resource)
                   records.append(flat_resource_type)
   return pd.DataFrame(records)


def rename_and_filter_columns(df: pd.DataFrame, column_rename_map=COLUMN_RENAME_MAP) -> pd.DataFrame:
   """
   Renames columns in the DataFrame according to a provided mapping and filters out columns not in the map.
  
   Args:
       df (pd.DataFrame): The DataFrame whose columns need to be renamed and filtered.
       column_rename_map (dict, optional): A dictionary mapping old column names to new names. Defaults to `COLUMN_RENAME_MAP`.


   Returns:
       pd.DataFrame: A DataFrame with renamed columns and only the relevant columns retained.
   """
   renamed_cols = {k: v for k, v in column_rename_map.items() if k in df.columns}
   df_renamed = df.rename(columns=renamed_cols)
   filtered_cols = [v for v in column_rename_map.values() if v in df_renamed.columns]
   return df_renamed[filtered_cols].reset_index(drop=True)

def clean_null_values(df: pd.DataFrame) -> pd.DataFrame:
   """
   Cleans missing values in the DataFrame by filling null values based on the column type and removing duplicates.
  
   Args:
       df (pd.DataFrame): The DataFrame to clean.


   Returns:
       pd.DataFrame: A DataFrame with cleaned null values and removed duplicates based on specific columns.
   """
   df = df[df['patient_id'].notna() & (df['patient_id'] != '0')]
   for col in df.columns:
       if pd.api.types.is_bool_dtype(df[col]):
           df[col] = df[col].fillna(False)
       elif pd.api.types.is_numeric_dtype(df[col]):
           df[col] = df[col].fillna(0)
           if ((df[col] % 1 == 0) | (df[col].isnull())).all():
               df[col] = df[col].astype(int)
       elif pd.api.types.is_string_dtype(df[col]) or pd.api.types.is_object_dtype(df[col]):
           df[col] = df[col].where(df[col].notnull(), None)
   df = df.drop_duplicates(subset=['patient_id', 'phone', 'address_line'], keep='first')
   return df.reset_index(drop=True)


def convert_column_dtypes(df: pd.DataFrame, date_columns: list = None, bool_columns: list = None) -> pd.DataFrame:
   """
   Converts specified columns in the DataFrame to appropriate data types, such as datetime for date columns
   and boolean for boolean columns. Invalid values are coerced to NaT or NaN.
  
   Args:
       df (pd.DataFrame): The DataFrame whose columns' data types need to be converted.
       date_columns (list, optional): A list of column names to be converted to datetime. Defaults to None.
       bool_columns (list, optional): A list of column names to be converted to boolean. Defaults to None.


   Returns:
       pd.DataFrame: A DataFrame with the specified columns converted to the appropriate data types.
   """
   if date_columns:
       for col in date_columns:
           if col in df.columns:
               df[col] = pd.to_datetime(df[col], errors='coerce', utc=True)
               df[col] = df[col].dt.tz_localize(None)

   if bool_columns:
       for col in bool_columns:
           if col in df.columns:
               df[col] = df[col].map({
                   'True': True,
                   'False': False,
                   'NA': False
               }).fillna(False)
               df[col] = df[col].astype(bool)

   return df


def get_patient_schema() -> pa.DataFrameSchema:
   """
   Returns a Pandera schema used to validate patient data in a DataFrame.
  
   Returns:
       pa.DataFrameSchema: A schema defining the expected structure and data types for the patient data.
   """
   return pa.DataFrameSchema({
       "patient_id": pa.Column(str, coerce=True, nullable=False),
       "first_name": pa.Column(str, nullable=True),
       "last_name": pa.Column(str, nullable=True),
       "name_prefix": pa.Column(str, nullable=True),
       "name_suffix": pa.Column(str, nullable=True),
       "name_use": pa.Column(str, nullable=True),
       "phone": pa.Column(str, nullable=True),
       "phone_system": pa.Column(str, nullable=True),
       "phone_use": pa.Column(str, nullable=True),
       "gender": pa.Column(str, nullable=True),
       "birth_date": pa.Column(pa.DateTime, nullable=True),
       "deceased_date": pa.Column(pa.DateTime, nullable=True, coerce=True),
       "address_line": pa.Column(str, nullable=True),
       "city": pa.Column(str, nullable=True),
       "state": pa.Column(str, nullable=True),
       "postal_code": pa.Column(str, nullable=True),
       "country": pa.Column(str, nullable=True),
       "marital_status": pa.Column(str, nullable=True),
       "multiple_birth_bool": pa.Column(pa.Bool, nullable=True),
       "multiple_birth_number": pa.Column(int, nullable=True),
       "preferred_language": pa.Column(str, nullable=True),
       "language_code": pa.Column(str, nullable=True),
   })


def validate_patient_data(df: pd.DataFrame) -> None:
   """
   Validates patient data by checking the schema and ensuring data integrity for specific columns.
  
   Args:
       df (pd.DataFrame): The DataFrame containing patient data to validate.
  
   Raises:
       ValueError: If any validation checks fail, such as null or duplicate patient IDs or invalid data types.
  
   Returns:
       None
   """
   schema = get_patient_schema()
   schema.validate(df)


