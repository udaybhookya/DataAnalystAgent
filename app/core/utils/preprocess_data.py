import pandas as pd
from typing import Dict, NamedTuple

class Table(NamedTuple):
    df: pd.DataFrame
    schema: pd.DataFrame

def preprocess_tables(
    tables: Dict[str, Table]
) -> Dict[str, Table]:
    """
    Cast each DataFrame’s columns according to its schema’s data_type.

    Args:
        tables: mapping from table name → Table(df, schema), 
                where schema is a DataFrame with at least
                ['column_name', 'data_type'].

    Returns:
        new_tables: same as `tables`, but with df’s columns
                    converted (or coerced) to the types declared
                    in schema.
    """
    print("\n===========================")
    print("Preprocessing data...")
    print("===========================")
    
    new_tables: Dict[str, Table] = {}

    for tbl_name, tbl in tables.items():
        df = tbl.df.copy()
        schema_df = tbl.schema

        for _, row in schema_df.iterrows():
            col = row['column_name']
            dtype = str(row['data_type']).strip().lower()

            if col not in df.columns:
                # skip if the column isn’t present
                continue

            if 'datetime' in dtype:
                df[col] = pd.to_datetime(df[col], errors='coerce')
            elif dtype in {'float', 'double', 'decimal'}:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            elif dtype in {'integer', 'int', 'long'}:
                df[col] = pd.to_numeric(df[col], errors='coerce', downcast='integer')
            elif dtype in {'boolean', 'bool'}:
                # pandas BooleanDtype retains NA
                df[col] = df[col].astype('boolean')
            else:
                # everything else → string
                df[col] = df[col].astype(str)

        new_tables[tbl_name] = Table(df=df, schema=tbl.schema)

    return new_tables
