# 🎲 Tinka & Kábala - Generador Inteligente de Combinaciones

Sistema desarrollado en Python para la generación, validación, análisis y almacenamiento de combinaciones numéricas para los juegos Tinka y Kábala.

La arquitectura actual está orientada a funcionamiento local mediante SQLite, permitiendo operar incluso sin conexión a Internet y sirviendo como base para una futura aplicación móvil.

---

# 📌 Características principales

* Generación inteligente de combinaciones numéricas
* Validación avanzada contra historial de sorteos
* Reglas estadísticas y filtros de calidad
* Detección de combinaciones históricas repetidas
* Sincronización de datos desde Railway
* Almacenamiento local en SQLite
* Operación offline
* Carga masiva desde archivos TXT
* Logging detallado
* Soporte para:

  * 🎯 Tinka
  * 🎯 Kábala

---

# 🏗️ Arquitectura

```text
TXT
 │
 ▼
Railway
 │
 ▼
SQLite
 │
 ▼
Generator
 │
 ▼
Validator
 │
 ▼
Output
```

La generación utiliza SQLite como fuente principal de datos.

Si SQLite no contiene información válida, el sistema puede recurrir a MySQL como mecanismo de respaldo.

---

# 📂 Estructura del proyecto

```text
src/
│
├── config/
│   ├── config_loader.py
│   └── game_config.py
│
├── database/
│   ├── connection.py
│   ├── sqlite_connection.py
│   └── create_sqlite_tables.py
│
├── migration/
│   ├── load_txt_dual_clean_log.py
│   └── migrate_railway_to_bkp_local.py
│
├── repository/
│   ├── game_repository.py
│   └── sqlite_game_repository.py
│
├── services/
│   ├── generator.py
│   └── validator.py
│
├── utils/
│   └── logger.py
│
├── run_tinka.py
├── run_kabala.py
└── check_duplicates.py
```

---

# ⚙️ Tecnologías utilizadas

* Python 3.x
* SQLite
* MySQL
* mysql-connector-python
* Logging estándar de Python

---

# 🗄️ Almacenamiento de datos

## Railway

Base de datos principal y fuente oficial de información.

## SQLite

Base local utilizada por el generador.

Ventajas:

* Mayor velocidad
* Menor dependencia de Internet
* Operación offline
* Compatible con futuras APK Android

## MySQL Local

Uso opcional como respaldo o entorno de desarrollo.

---

# 🔄 Flujo de sincronización

## 1. Carga de archivos TXT

```bash
python -m src.migration.load_txt_dual_clean_log
```

Procesa archivos históricos y los inserta en Railway.

---

## 2. Sincronización hacia SQLite

```bash
python -m src.migration.migrate_railway_to_bkp_local
```

Obtiene la información desde Railway y actualiza SQLite.

---

## 3. Generación de combinaciones

### Tinka

```bash
python -m src.run_tinka
```

### Kábala

```bash
python -m src.run_kabala
```

---

# 📂 Formato TXT

Ejemplo:

```text
22/04/2026  22 01 40 52 23 25
19/04/2026  31 36 50 17 32 28
```

Durante la importación:

* Conversión automática de fechas
* Ordenamiento de números
* Eliminación de ceros a la izquierda
* Validación de registros
* Detección de duplicados

---

# 🧠 Reglas del generador

El sistema evita combinaciones que:

* Repitan combinaciones históricas
* Sean demasiado similares a sorteos recientes
* Presenten patrones repetitivos
* Contengan exceso de números pares o impares
* Tengan distribuciones poco equilibradas
* Incumplan reglas estadísticas definidas para cada juego

---

# 🔍 Verificación de duplicados

```bash
python -m src.check_duplicates
```

Permite identificar combinaciones históricas repetidas dentro de SQLite.

---

# 📊 Logs

Los logs se almacenan en:

```text
logs/
```

Incluyendo:

* Sincronización
* Migraciones
* Generación
* Validaciones
* Errores

---

# 🔐 Configuración

Las credenciales deben configurarse en:

```text
config.ini
```

No incluir credenciales reales en repositorios públicos.

---

# 🚀 Objetivo del proyecto

La arquitectura actual está diseñada para evolucionar hacia una aplicación móvil Android donde SQLite actuará como almacenamiento local y Railway como fuente de sincronización de datos.

---

# ⚠️ Aviso

Este sistema realiza análisis estadístico y generación de combinaciones numéricas.

No predice resultados futuros ni garantiza premios.
