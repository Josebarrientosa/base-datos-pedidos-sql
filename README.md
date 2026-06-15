# Base de datos relacional de pedidos — modelado y consultas SQL

Diseño de un esquema relacional para una tienda, carga de datos desde archivos CSV y consultas SQL orientadas a responder preguntas de negocio (actividad de clientes, detalle de pedidos, productos más vendidos e ingresos por cliente).

Proyecto desarrollado a partir de un trabajo del Diplomado en Ciencia de Datos para la Gestión (PUC), reescrito como proyecto propio y portado a SQLite para que sea reproducible sin necesidad de instalar un servidor de base de datos.

## Problema

Una tienda registra clientes, productos y pedidos en archivos sueltos (CSV). En ese formato no se pueden responder preguntas que cruzan información, como cuánto gasta cada cliente o qué productos se venden más. El objetivo es estructurar esos datos en una base relacional y escribir consultas SQL que entreguen respuestas accionables para el área comercial.

## Modelo de datos

Cuatro tablas relacionadas mediante llaves foráneas:

- **clientes** — id, nombre, email.
- **productos** — id, nombre, descripción, precio.
- **pedidos** — id, fecha, dirección, detalle, y el cliente que lo realizó (`id_cliente` → clientes).
- **productos_pedidos** — tabla puente que resuelve la relación muchos-a-muchos entre pedidos y productos, con la cantidad de cada producto en cada pedido. Su clave primaria es compuesta (`id_producto`, `id_pedido`).

```
clientes ──< pedidos ──< productos_pedidos >── productos
```

## Consultas incluidas

1. **Pedidos por cliente** — cuántos pedidos hizo un cliente determinado (JOIN + COUNT + GROUP BY).
2. **Detalle de un pedido** — productos, cantidades, precios y subtotal de un pedido (JOIN).
3. **Pedidos de un producto en un rango de fechas** — cruce de tres tablas con filtro de fechas y DISTINCT.
4. **Productos más vendidos** — ranking por unidades vendidas e ingresos (JOIN + SUM + GROUP BY + ORDER BY).
5. **Ingresos por cliente** — cuánto ha gastado cada cliente, ordenado de mayor a menor (JOIN de cuatro tablas + agregación).

Las consultas 1 a 3 corresponden al trabajo original; las consultas 4 y 5 se agregaron para mostrar análisis agregado orientado a decisiones comerciales.

## Tecnologías

- Python (sqlite3, csv) — sin dependencias externas.
- SQL (SQLite).

## Estructura del repositorio

```
.
├── build_db.py          # Crea el esquema y carga los CSV en SQLite
├── queries.py           # Ejecuta las consultas de negocio
├── data/                # Datos de origen en CSV
│   ├── clientes.csv
│   ├── productos.csv
│   ├── pedidos.csv
│   └── productos_pedidos.csv
└── README.md
```

## Cómo ejecutar

```bash
# 1. Construir la base de datos (genera tienda.db)
python build_db.py

# 2. Ejecutar las consultas de negocio
python queries.py
```

No requiere instalar nada adicional: usa solo la librería estándar de Python.

## Nota sobre los datos

Los archivos CSV de esta versión son datos de ejemplo, generados para que el proyecto sea reproducible de forma pública. El foco del proyecto está en el diseño del modelo relacional y en las consultas SQL, no en los datos en sí.
