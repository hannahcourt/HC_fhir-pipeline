""" Module to test data transfromformation and processing. """
import pandas as pd
from transformation import transform_resources, flatten_dict


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