""" Module to test data transfromformation and processing. """
import pandas as pd
from transformation import transform_resources, flatten_dict, clean_null_values, rename_and_filter_columns
import numpy as np

def test_flatten_dict():
   """
   Test case for flatten_dict that handles realistic FHIR Patient data.
  
   This test ensures that the flatten_dict function:
   - Can flatten a realistic, nested FHIR patient record.
   - Correctly handles nested dictionaries and lists.
   - Outputs a flat dictionary with dot-separated keys.
   """


   input_data = {
       "resourceType": "Patient",
       "id": "12345",
       "name": [{"given": ["John"], "family": "Doe"}],
       "gender": "male",
       "birthDate": "1990-01-01",
       "address": [
           {
               "line": ["1234 Elm St"],
               "city": "Somewhere",
               "state": "CA",
               "postalCode": "90210"
           }
       ],
       "communication": [
           {
               "language": {"coding": [{"code": "en", "display": "English"}]},
               "preferred": True
           }
       ],
       "maritalStatus": {"coding": [{"code": "M", "display": "Married"}]},
       "contact": [
           {
               "relationship": [{"coding": [{"code": "C01", "display": "Emergency contact"}]}],
               "name": {"given": ["Jane"], "family": "Doe"},
               "telecom": [{"system": "phone", "value": "555-1234"}]
           }
       ]
   }


   expected = {
       'resourceType': 'Patient',
       'id': '12345',
       'name.0.given.0': 'John',
       'name.0.family': 'Doe',
       'gender': 'male',
       'birthDate': '1990-01-01',
       'address.0.line.0': '1234 Elm St',
       'address.0.city': 'Somewhere',
       'address.0.state': 'CA',
       'address.0.postalCode': '90210',
       'communication.0.language.coding.0.code': 'en',
       'communication.0.language.coding.0.display': 'English',
       'communication.0.preferred': True,
       'maritalStatus.coding.0.code': 'M',
       'maritalStatus.coding.0.display': 'Married',
       'contact.0.relationship.0.coding.0.code': 'C01',
       'contact.0.relationship.0.coding.0.display': 'Emergency contact',
       'contact.0.name.given.0': 'Jane',
       'contact.0.name.family': 'Doe',
       'contact.0.telecom.0.system': 'phone',
       'contact.0.telecom.0.value': '555-1234'
   }


   result = flatten_dict(input_data)
   assert result == expected


def test_transform_resources():
   """
   Test case for transform_resource_data that simulates transforming a list of FHIR patient data
   from a nested JSON structure into a flat tabular format using pandas DataFrame.


   The test ensures:
   - The function properly flattens patient data.
   - The correct columns are extracted and transformed.
   """


   input_data = [
       {
           "resourceType": "Bundle",
           "entry": [
               {
                   "resource": {
                       "resourceType": "Patient",
                       "id": "123",
                       "name": [{"given": ["John"], "family": "Doe"}],
                       "gender": "male",
                       "birthDate": "1990-01-01",
                   }
               }
           ]
       },
       {
           "resourceType": "Bundle",
           "entry": [
               {
                   "resource": {
                       "resourceType": "Patient",
                       "id": "456",
                       "name": [{"given": ["Jane"], "family": "Smith"}],
                       "gender": "female",
                       "birthDate": "1985-03-15",
                   }
               }
           ]
       }
   ]


   result_df = transform_resources(input_data)


   expected_df = pd.DataFrame([
       {
           'resourceType': 'Patient',
           'id': '123',
           'name.0.given.0': 'John',
           'name.0.family': 'Doe',
           'gender': 'male',
           'birthDate': '1990-01-01'
       },
       {
           'resourceType': 'Patient',
           'id': '456',
           'name.0.given.0': 'Jane',
           'name.0.family': 'Smith',
           'gender': 'female',
           'birthDate': '1985-03-15'
       }
   ])


   pd.testing.assert_frame_equal(result_df, expected_df)



def test_rename_and_filter_columns():
   """
   Test renaming and filtering of DataFrame columns using COLUMN_RENAME_MAP.


   Covers:
   - Standard case where all columns are present.
   - Case where some column_rename_map keys are missing from the input DataFrame.
   """
   column_rename_map = {
   'id': 'patient_id',
   'name.0.given.0': 'first_name',
   'name.0.family': 'last_name',
   'gender': 'gender',
   'birthDate': 'dob'
   }


   input_df_all = pd.DataFrame([
       {
           'id': '001',
           'name.0.given.0': 'Alice',
           'name.0.family': 'Wonderland',
           'gender': 'female',
           'birthDate': '2000-01-01',
           'unused_column': 'ignore_me'
       }
   ])


   expected_df_all = pd.DataFrame([
       {
           'patient_id': '001',
           'first_name': 'Alice',
           'last_name': 'Wonderland',
           'gender': 'female',
           'dob': '2000-01-01'
       }
   ])


   result_df_all = rename_and_filter_columns(input_df_all, column_rename_map)
   pd.testing.assert_frame_equal(result_df_all, expected_df_all)

   input_df_partial = pd.DataFrame([
       {'id': '123', 'gender': 'male'}
   ])
   expected_df_partial = pd.DataFrame([
       {'patient_id': '123', 'gender': 'male'}
   ])[['patient_id', 'gender']] 

   result_df_partial = rename_and_filter_columns(input_df_partial, column_rename_map)
   pd.testing.assert_frame_equal(result_df_partial, expected_df_partial)


def test_clean_null_values():
   """
   Test handling of null values in numeric and non-numeric columns,
   ensuring invalid patient_id (Null or 0) rows are dropped correctly,
   and duplicates are handled.
   """


   input_df = pd.DataFrame([{
       'patient_id': '001',
       'first_name': np.nan,
       'last_name': 'Doe',
       'gender': np.nan,
       'dob': '1980-01-01',
       'multiple_birth_number': np.nan, 
       'phone': np.nan, 
       'address_line': np.nan
   }, {
       'patient_id': '0', 
       'first_name': 'Jane',
       'last_name': 'Doe',
       'gender': 'female',
       'dob': '1985-01-01',
       'multiple_birth_number': 2.0,
       'phone': '123-456-7890',
       'address_line': '123 Elm St'
   }, {
       'patient_id': np.nan, 
       'first_name': 'John',
       'last_name': 'Doe',
       'gender': 'male',
       'dob': '1980-01-01',
       'multiple_birth_number': 0.0, 
       'phone': '987-654-3210',
       'address_line': '456 Oak St'
  }, {
       'patient_id': '001',
       'first_name': 'John',
       'last_name': 'Doe',
       'gender': 'male',
       'dob': '1980-01-01',
       'multiple_birth_number': 0.0,
       'phone': '123-456-7890',
       'address_line': '123 Elm St'
   }])

   expected_df = pd.DataFrame([{
       'patient_id': '001',
       'first_name': np.nan,
       'last_name': 'Doe',
       'gender': np.nan, 
       'dob': '1980-01-01',
       'multiple_birth_number': 0.0,
       'phone': np.nan,
       'address_line': np.nan 
   }, {
       'patient_id': '001',
       'first_name': 'John', 
       'last_name': 'Doe',
       'gender': 'male',
       'dob': '1980-01-01',
       'multiple_birth_number': 0.0, 
       'phone': '123-456-7890', 
       'address_line': '123 Elm St' 
   }])


   result_df = clean_null_values(input_df)
   result_df = result_df.where(pd.notnull(result_df), np.nan)
   expected_df = expected_df.where(pd.notnull(expected_df), np.nan)


   pd.testing.assert_frame_equal(result_df, expected_df, check_dtype=False)
