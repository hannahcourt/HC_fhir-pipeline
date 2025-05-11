""" Module to ingest data into the pipeline from the source."""
import os
import json


def load_fhir_data(data_dir: str):
   """
   Loads FHIR patient data from JSON files in a specified directory.

   Args:
       data_dir (str): The path to the directory containing the JSON files.

   Returns:
       list: A list of dictionaries representing the FHIR patient data.
   """
   data = []
   for filename in os.listdir(data_dir):
       if filename.endswith(".json"):
           filepath = os.path.join(data_dir, filename)
           with open(filepath) as f:
               file_data = json.load(f)
               data.append(file_data)
  
   return data




