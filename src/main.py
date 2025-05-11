""" Module to import and run the full production pipeline. """
from config import RAW_DATA_DIR, PROCESSED_DATA_DIR, COLUMN_RENAME_MAP, DATE_COLUMNS, BOOL_COLUMNS, DATABASE_URL, TABLE_NAME
from ingestion import load_fhir_data
from transformation import transform_resources, rename_and_filter_columns, clean_null_values, convert_column_dtypes, validate_patient_data
from storage import save_to_parquet, save_to_postgres
from loguru import logger

def main():
   logger.info("Starting FHIR Patient data processing...")


   logger.info("Loading raw data...")
   fhir_data = load_fhir_data(RAW_DATA_DIR)

   if not fhir_data:
       logger.warning("No files found in the raw data directory.")
       return
   logger.info(f"Loaded {len(fhir_data)} FHIR bundles.")

   logger.info("Extracting Patient resources...")
   df_raw = transform_resources(fhir_data)

   if df_raw.empty:
       logger.warning("No Patient resources found.")
       return
  
   logger.info(f"Extracted {len(df_raw)} Patient records.")

   logger.info("Renaming and filtering relevant columns...")
   df_clean = rename_and_filter_columns(df_raw, column_rename_map=COLUMN_RENAME_MAP)

   logger.info("Converting column types...")
   df_clean = convert_column_dtypes(
       df_clean,
       date_columns=DATE_COLUMNS,
       bool_columns=BOOL_COLUMNS
   )

   logger.info("Replacing null values...")
   df_clean = clean_null_values(df_clean)

   if df_clean.empty:
       logger.warning("No Patient records left after cleaning.")
       return

   try:
       logger.info("Validating patient data...")
       validate_patient_data(df_clean)
       logger.info("Patient data passed validation.")
   except Exception as e:
       logger.error(f"Validation failed: {e}")
       return

   logger.info(f"Storing validated data.")
   save_to_parquet(df_clean, PROCESSED_DATA_DIR)
   logger.info(f"Data saved to {PROCESSED_DATA_DIR}")

   save_to_postgres(df_clean, table_name=TABLE_NAME, db_name=DATABASE_URL)
   logger.info(f"Data saved to {TABLE_NAME}")

   logger.info("FHIR Patient data processed successfully.")

if __name__ == '__main__':
   main()