""" Module to test data ingestion. """
from ingestion import load_fhir_data

def test_load_fhir_data_full():
   """
   Test for loading FHIR data from a directory containing valid JSON files.

   This test ensures that the `load_fhir_data()` function correctly loads
   patient data from a specified directory containing valid JSON files.

   It asserts that the returned list contains the correct data structure
   based on a sample valid JSON file.
   """
   test_dir_full = "tests/data/test_raw"
  
   patient_data = load_fhir_data(test_dir_full)

   expected_data = {
       "patient_id": "1",
       "name": [{"family": "Doe", "given": ["John"]}],
       "gender": "male",
       "birthDate": "1999-10-01"
   }
   assert patient_data[0] == expected_data


def test_load_fhir_data_empty():
   """
   Test case for loading FHIR data from an empty directory.


   This test ensures that the `load_fhir_data()` function returns an empty
   list when given a directory that does not contain any JSON files or is empty.

   It asserts that if the directory is empty or contains no valid JSON files,
   the returned list will be empty.

   This test is useful to check the behaviour of the function when there is no data to process.
   """
   test_dir_empty = "tests/data/test_raw_empty"
  
   patient_data = load_fhir_data(test_dir_empty)

   assert patient_data == []