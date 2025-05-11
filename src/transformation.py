""" Module to transfrom and process raw data."""
import pandas as pd
from config import PATIENT_RESOURCE_TYPE


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




