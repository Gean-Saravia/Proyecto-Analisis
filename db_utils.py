import os
import pyodbc
import urllib.parse
from dotenv import load_dotenv
from sqlalchemy import create_engine

#Conexión con pyodbc (control fino, para Silver/Gold) 
def db_conectar(autocommit: bool = False) -> pyodbc.Connection:
    """Conecta a SQL Server usando pyodbc (útil para Silver/Gold)."""
    load_dotenv()
    server   = os.getenv("MSSQL_SERVER")
    database = os.getenv("MSSQL_DATABASE")
    usuario  = os.getenv("MSSQL_USUARIO")
    password = os.getenv("MSSQL_PASSWORD")
    driver   = os.getenv("MSSQL_DRIVER", "ODBC Driver 17 for SQL Server")

    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={usuario};"
        f"PWD={password}"
    )
    return pyodbc.connect(connection_string, autocommit=autocommit)


# Conexión con SQLAlchemy (rápida, solo para bronce)
def crear_engine_mssql():
    """Crea un engine de SQLAlchemy (con fast_executemany) para cargas masivas."""
    load_dotenv()
    server   = os.getenv("MSSQL_SERVER")
    database = os.getenv("MSSQL_DATABASE")
    usuario  = os.getenv("MSSQL_USUARIO")
    password = os.getenv("MSSQL_PASSWORD")
    driver   = os.getenv("MSSQL_DRIVER", "ODBC Driver 17 for SQL Server")

    # Armamos el ODBC connection string y lo encodeamos para SQLAlchemy
    odbc_str = (
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={usuario};"
        f"PWD={password};"
        "Encrypt=yes;TrustServerCertificate=no"
    )
    params = urllib.parse.quote_plus(odbc_str)

    engine = create_engine(
        f"mssql+pyodbc:///?odbc_connect={params}",
        fast_executemany=True
    )
    return engine