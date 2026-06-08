# 🎲 Tinka & Kábala — Generador Inteligente de Combinaciones

Sistema desarrollado en Python para la generación, validación, análisis estadístico y almacenamiento de combinaciones numéricas para los juegos **Tinka** y **Kábala**.

La arquitectura actual está diseñada para operar principalmente sobre **SQLite**, permitiendo generación local, funcionamiento offline y sincronización periódica con Railway. Este diseño servirá como base para una futura aplicación Android.

---

# 📌 Características principales

* Generación inteligente de combinaciones numéricas
* Validación avanzada contra historial completo de sorteos
* Reglas estadísticas y filtros de calidad
* Detección de combinaciones históricas repetidas
* Operación offline mediante SQLite
* Sincronización de datos desde Railway
* Fallback automático a MySQL cuando sea necesario
* Carga masiva desde archivos TXT
* Logging centralizado
* Soporte para:

  * 🎯 Tinka
  * 🎯 Kábala

---

# 🏗️ Arquitectura General

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

### Flujo de generación

```text
run_tinka.py / run_kabala.py
            │
            ▼
      generator.py
            │
            ▼
 sqlite_game_repository.py
            │
            ▼
         SQLite
```

SQLite es la fuente primaria de datos.

El generador no depende de Internet para funcionar.

---

# 📂 Estructura del Proyecto

```text
TnkIntellij/
│
├── src/
│   │
│   ├── config/
│   │   ├── config_loader.py
│   │   └── game_config.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── sqlite_connection.py
│   │   └── create_sqlite_tables.py
│   │
│   ├── migration/
│   │   ├── load_txt_dual_clean_log.py
│   │   └── migrate_railway_to_bkp_local.py
│   │
│   ├── repository/
│   │   ├── game_repository.py
│   │   └── sqlite_game_repository.py
│   │
│   ├── services/
│   │   ├── generator.py
│   │   └── validator.py
│   │
│   ├── utils/
│   │   └── logger.py
│   │
│   ├── run_tinka.py
│   ├── run_kabala.py
│   └── check_duplicates.py
│
├── data/
├── database/
├── logs/
├── output/
│
├── config.ini
└── exportar_codigo.py
```

---

# ⚙️ Tecnologías Utilizadas

| Tecnología             | Uso                           |
| ---------------------- | ----------------------------- |
| Python 3.x             | Lenguaje principal            |
| SQLite                 | Caché local y fuente primaria |
| MySQL                  | Sincronización y respaldo     |
| Railway                | Base de datos principal       |
| mysql-connector-python | Acceso a MySQL                |
| logging                | Registro de eventos           |

---

# 🗄️ Almacenamiento de Datos

## ☁️ Railway

Fuente oficial de información histórica.

Contiene la totalidad de sorteos disponibles.

---

## 💾 SQLite

Base local utilizada por el generador.

Ventajas:

* Operación offline
* Menor latencia
* Menor dependencia de Internet
* Ideal para futuras aplicaciones móviles

---

## 🖥️ MySQL Local

Uso opcional como respaldo o entorno de desarrollo.

No es obligatorio para la operación del generador.

---

# 🔄 Flujo de Sincronización

## 1. Carga de archivos TXT

```bash
python -m src.migration.load_txt_dual_clean_log
```

Procesa archivos históricos y los inserta en Railway.

Si MySQL local está disponible también puede actualizarlo.

---

## 2. Actualización de SQLite

```bash
python -m src.migration.migrate_railway_to_bkp_local
```

Obtiene la información desde Railway y reconstruye SQLite.

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

# 📂 Formato de Archivos TXT

Ejemplo:

```text
22/04/2026 22 01 40 52 23 25
19/04/2026 31 36 50 17 32 28
```

Durante la importación el sistema realiza:

* Conversión automática de fechas
* Ordenamiento de números
* Eliminación de ceros a la izquierda
* Validación de rangos
* Detección de registros inválidos
* Control de duplicados

---

# 🧠 Reglas de Validación

El generador rechaza combinaciones que:

* Ya existieron históricamente
* Son demasiado similares a sorteos recientes
* Presentan exceso de pares o impares
* Contienen demasiados consecutivos
* Tienen rango insuficiente
* Repiten patrones históricos
* Poseen similitud elevada mediante índice de Jaccard
* Presentan distancia euclidiana demasiado cercana a sorteos anteriores

Las reglas son configurables por juego.

---

# 🔍 Verificación de Duplicados

```bash
python -m src.check_duplicates
```

Permite detectar combinaciones históricas repetidas.

Actualmente se identificaron:

| Juego  | Combinaciones repetidas |
| ------ | ----------------------: |
| Tinka  |                       2 |
| Kábala |                       7 |

Estas combinaciones son consideradas una única combinación histórica por el generador.

---

# 📊 Logs

Los logs se almacenan en:

```text
logs/
```

Incluyendo eventos de:

* Generación
* Validación
* Migraciones
* Sincronización
* Carga de archivos TXT
* Errores y advertencias

---

# 💾 Operación Offline

Una vez sincronizada SQLite, el sistema puede:

* Generar combinaciones
* Consultar historial
* Aplicar validaciones
* Detectar duplicados

sin necesidad de conexión a Internet.

La nube se utiliza únicamente para actualización de datos.

---

# 🔐 Configuración

Las credenciales deben almacenarse en:

```text
config.ini
```

Recomendaciones:

* No subir credenciales a GitHub
* Mantener configuraciones separadas para desarrollo y producción
* Incluir `config.ini` en `.gitignore`

---

# 🚀 Objetivo del Proyecto

La arquitectura actual está orientada a evolucionar hacia una aplicación Android donde:

```text
Railway/API
      │
      ▼
   SQLite
      │
      ▼
 Generator
```

manteniendo operación offline y sincronización periódica de datos.

---

# 📌 Autor

Proyecto personal de Hugo Ramos M para análisis estadístico y generación de combinaciones numéricas.

---

# ⚠️ Disclaimer

Este sistema realiza análisis estadístico y generación aleatoria de combinaciones numéricas.

No predice resultados futuros ni garantiza premios o resultados reales.
