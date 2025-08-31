from db_utils import db_conectar
#Creacion de esquemas
def crear_esquemas():
    esquemas = ["Bronce", "Silver", "Gold"]
    with db_conectar(autocommit=True) as conn:
        cur = conn.cursor()
        for esquema in esquemas:
            cur.execute(f"""
                IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = '{esquema}')
                BEGIN
                    EXEC('CREATE SCHEMA {esquema}')
                END
            """)