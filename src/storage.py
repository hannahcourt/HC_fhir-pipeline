""" Module to store transformed data."""
import os
from config import DATABASE_URL, TABLE_NAME
from sqlalchemy import create_engine

def save_to_parquet(df, file_path):
   """
   Save the DataFrame to a Parquet file.

   Args:
   ----------
       df (pd.DataFrame): The DataFrame to save.
       file_path (str): The path to the output Parquet file.
  
   Returns:
   -------
   None
       This function does not return any value. It saves the data to the a parquet file.
   """
   os.makedirs(os.path.dirname(file_path), exist_ok=True)
   df.to_parquet(file_path, index=False)


def save_to_postgres(df, table_name=TABLE_NAME, db_name=DATABASE_URL):
   """
   Saves a DataFrame to a PostgreSQL database table.


   This function takes a pandas DataFrame and writes it to a specified table
   in a PostgreSQL database. If the table already exists, it will be replaced
   with the new data. The database connection is established using SQLAlchemy's
   `create_engine`.


   Parameters:
   ----------
   df : pandas.DataFrame
       The DataFrame to be saved to the database.
      
   table_name : str, optional
       The name of the table in the database where the DataFrame will be saved. .


   db_name : str, optional
       The database connection URL. It should include the username, password, host,
       port, and database name.


   Returns:
   -------
   None
       This function does not return any value. It saves the data to the specified database table.
   """
   engine = create_engine(db_name)
   df.to_sql(table_name, engine, if_exists='replace', index=False)
