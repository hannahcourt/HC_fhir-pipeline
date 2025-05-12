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


from sqlalchemy import create_engine

def save_to_postgres(df, table_name='patients', db_name='postgresql://testuser:testpass@db:5432/testdb'):
    """
    Saves a DataFrame to a PostgreSQL database table.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to be saved to the database.
    
    table_name : str, optional
        The name of the table in the database where the DataFrame will be saved. Default is 'patients'.
    
    db_name : str, optional
        The database connection URL. Default is 'postgresql://testuser:testpass@db:5432/testdb'.
    
    Returns
    -------
    None
    """
    try:
        # Create the SQLAlchemy engine for connecting to the database
        engine = create_engine(db_name)

        # Save the DataFrame to PostgreSQL, replace the table if it already exists
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data saved to {table_name} table.")
    except Exception as e:
        print(f"An error occurred while saving data to PostgreSQL: {e}")

