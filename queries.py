"""
Consultas de negocio sobre la base de datos relacional de la tienda.

Cada consulta responde una pregunta concreta que un analista podría recibir
del área comercial. Ejecuta build_db.py antes de correr este script.

Uso:
    python queries.py
"""
import sqlite3
from pathlib import Path

DB_PATH = Path("tienda.db")


def run_query(conn, title, question, sql, params=()):
    """Ejecuta una consulta e imprime la pregunta de negocio y su resultado."""
    print("\n" + "=" * 70)
    print(title)
    print("Pregunta: " + question)
    print("-" * 70)
    cur = conn.cursor()
    cur.execute(sql, params)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    print(" | ".join(cols))
    for row in rows:
        print(" | ".join(str(v) for v in row))
    if not rows:
        print("(sin resultados)")


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    # 1. Actividad de un cliente específico
    run_query(
        conn,
        "CONSULTA 1 — Pedidos por cliente",
        "¿Cuántos pedidos ha realizado un cliente determinado?",
        """
        SELECT c.nombre, c.email, COUNT(p.id) AS total_pedidos
        FROM clientes c
        LEFT JOIN pedidos p ON p.id_cliente = c.id
        WHERE c.email = ?
        GROUP BY c.id
        """,
        ("jessicaflores@example.com",),
    )

    # 2. Detalle de un pedido
    run_query(
        conn,
        "CONSULTA 2 — Detalle de un pedido",
        "¿Qué productos, en qué cantidad y a qué precio incluye un pedido?",
        """
        SELECT pr.id, pr.nombre, pr.precio, pp.cantidad,
               pr.precio * pp.cantidad AS subtotal
        FROM productos_pedidos pp
        JOIN productos pr ON pr.id = pp.id_producto
        WHERE pp.id_pedido = ?
        ORDER BY pr.id ASC
        """,
        (2,),
    )

    # 3. Cruce producto + rango de fechas
    run_query(
        conn,
        "CONSULTA 3 — Pedidos de un producto en un rango de fechas",
        "¿Qué pedidos que contienen 'Tablet' se hicieron entre el 05 y el 07 de enero?",
        """
        SELECT DISTINCT p.id, p.direccion, p.detalle, p.fecha
        FROM pedidos p
        JOIN productos_pedidos pp ON pp.id_pedido = p.id
        JOIN productos pr ON pr.id = pp.id_producto
        WHERE pr.nombre = 'Tablet'
          AND p.fecha BETWEEN '2024-01-05' AND '2024-01-07'
        ORDER BY p.fecha DESC
        """,
    )

    # 4. Ranking de productos más vendidos (valor de negocio agregado)
    run_query(
        conn,
        "CONSULTA 4 — Productos más vendidos por unidades",
        "¿Cuáles son los productos con mayor cantidad total vendida?",
        """
        SELECT pr.nombre,
               SUM(pp.cantidad) AS unidades_vendidas,
               SUM(pp.cantidad * pr.precio) AS ingresos
        FROM productos_pedidos pp
        JOIN productos pr ON pr.id = pp.id_producto
        GROUP BY pr.id
        ORDER BY unidades_vendidas DESC, ingresos DESC
        """,
    )

    # 5. Ingresos por cliente
    run_query(
        conn,
        "CONSULTA 5 — Ingresos generados por cada cliente",
        "¿Cuánto ha gastado cada cliente en total? (ranking de clientes)",
        """
        SELECT c.nombre,
               SUM(pp.cantidad * pr.precio) AS gasto_total
        FROM clientes c
        JOIN pedidos p ON p.id_cliente = c.id
        JOIN productos_pedidos pp ON pp.id_pedido = p.id
        JOIN productos pr ON pr.id = pp.id_producto
        GROUP BY c.id
        ORDER BY gasto_total DESC
        """,
    )

    conn.close()
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
