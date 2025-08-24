from db_utils import db_conectar

def crear_esquemas():
    """
    Crea Bronce, Silver, Gold si no existen (idempotente).
    Ejecutalo SOLO cuando quieras crear/verificar esquemas.
    """
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
    print("✅ Esquemas verificados/creados (si faltaban).")