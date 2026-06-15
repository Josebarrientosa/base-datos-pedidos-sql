"""
Construcción de la base de datos relacional a partir de archivos CSV.

Crea un esquema de 4 tablas (clientes, productos, pedidos, productos_pedidos)
con sus llaves foráneas y carga los datos desde la carpeta data/.

Uso:
    python build_db.py

Genera el archivo tienda.db (SQLite), listo para consultar.
"""
import csv
import sqlite3
from pathlib import Path

DATA_DIR = Path("data")
DB_PATH = Path("tienda.db")

SCHEMA = """
DROP TABLE IF EXISTS productos_pedidos;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS clientes;

CREATE TABLE clientes (
    id     INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    email  TEXT NOT NULL
);

CREATE TABLE productos (
    id          INTEGER PRIMARY KEY,
    nombre      TEXT NOT NULL,
    descripcion TEXT,
    precio      INTEGER NOT NULL
);

CREATE TABLE pedidos (
    id         INTEGER PRIMARY KEY,
    fecha      DATE NOT NULL,
    direccion  TEXT NOT NULL,
    id_cliente INTEGER NOT NULL,
    detalle    TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
);

CREATE TABLE productos_pedidos (
    id_producto INTEGER NOT NULL,
    id_pedido   INTEGER NOT NULL,
    cantidad    INTEGER NOT NULL,
    PRIMARY KEY (id_producto, id_pedido),
    FOREIGN KEY (id_producto) REFERENCES productos(id),
    FOREIGN KEY (id_pedido)   REFERENCES pedidos(id)
);
"""

# Definición de cada carga: archivo, tabla, columnas y conversores de tipo.
LOADS = [
    ("clientes.csv", "clientes",
     ["id", "nombre", "email"],
     [int, str, str]),
    ("productos.csv", "productos",
     ["id", "nombre", "descripcion", "precio"],
     [int, str, str, int]),
    ("pedidos.csv", "pedidos",
     ["id", "fecha", "direccion", "id_cliente", "detalle"],
     [int, str, str, int, str]),
    ("productos_pedidos.csv", "productos_pedidos",
     ["id_producto", "id_pedido", "cantidad"],
     [int, int, int]),
]


def read_csv(path, converters):
    """Lee un CSV con encabezado y devuelve las filas convertidas a su tipo."""
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # saltar encabezado
        for row in reader:
            rows.append(tuple(conv(val) for conv, val in zip(converters, row)))
    return rows


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cur = conn.cursor()

    cur.executescript(SCHEMA)

    for filename, table, columns, converters in LOADS:
        rows = read_csv(DATA_DIR / filename, converters)
        placeholders = ", ".join(["?"] * len(columns))
        cols = ", ".join(columns)
        cur.executemany(
            f"INSERT INTO {table} ({cols}) VALUES ({placeholders})", rows
        )
        print(f"  {table}: {len(rows)} filas cargadas")

    conn.commit()
    conn.close()
    print(f"\nBase de datos creada en {DB_PATH}")


if __name__ == "__main__":
    main()
