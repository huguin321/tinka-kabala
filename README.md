# 🎲 Tinka & Kábala - Generador y Analizador de Combinaciones

Sistema desarrollado en Python para la generación, validación, análisis y almacenamiento de combinaciones numéricas tipo lotería (Tinka y Kábala), con soporte de base de datos en la nube (Railway) y MySQL local.

---

## 📌 Características principales

- Generación inteligente de combinaciones aleatorias
- Validación avanzada contra historial de sorteos
- Reglas estadísticas (pares, impares, entropía, patrones, distancias)
- Detección de combinaciones repetidas o similares
- Persistencia en MySQL (local y Railway)
- Migración de datos entre entornos
- Carga masiva desde archivos `.txt`
- Logging detallado del sistema
- Soporte para dos juegos:
  - 🎯 Tinka (1 combinación por sorteo)
  - 🎯 Kábala (2 combinaciones por sorteo)

---

## 🏗️ Arquitectura del proyecto

src/
│
├── config/            # Configuración del sistema
├── database/          # Conexión a MySQL
├── migration/         # Migración y carga de datos
├── repository/        # Consultas a base de datos
├── services/          # Lógica de generación y validación
├── utils/             # Logger y utilidades
├── run_tinka.py       # Ejecución Tinka
├── run_kabala.py      # Ejecución Kábala

---

## ⚙️ Tecnologías utilizadas

- Python 3.x
- MySQL
- mysql-connector-python
- SciPy (distancias y análisis estadístico)
- Logging estándar de Python

---

## 📂 Formato de datos (TXT)

Los archivos deben tener el siguiente formato:

22/04/2026  22 01 40 52 23 25
19/04/2026  31 36 50 17 32 28

### Reglas de procesamiento:
- Orden cronológico automático
- Orden interno ascendente por combinación
- Eliminación de ceros a la izquierda
- Detección de duplicados

---

## 🚀 Ejecución del proyecto

### Tinka
python src/run_tinka.py

### Kabala
python src/run_kabala.py


### Migración de base de datos
python src/migration/migrate_local_to_railway.py

### Carga desde archivos TXT (Carga dual Local + Railway)
python src/migration/load_txt_dual_clean_log.py


## 🧠 Reglas del sistema

El generador evita combinaciones que:

Tengan demasiados números repetidos con históricos
Sean demasiado similares a sorteos anteriores
Tengan baja entropía
Presenten patrones repetitivos
Estén demasiado agrupadas
Tengan exceso de pares o impares
Sean estadísticamente similares a combinaciones recientes

## 🗄️ Base de datos

Tablas principales:

TblTinka
TblKabala

Campos:

fecha, NumUno, NumDos, NumTre, NumCua, NumCin, NumSei


## 🌐 Entornos soportados
🖥️ Local MySQL
☁️ Railway MySQL (producción)

## 📊 Logs

Los logs se generan en:

/logs/tinka.log
/logs/kabala.log

## 🔐 Seguridad
Las credenciales de base de datos deben configurarse en config.ini
No subir credenciales reales a GitHub
Usar variables separadas para producción

## 📌 Autor

Proyecto personal de Hugo Ramos M para análisis y generación de combinaciones numéricas.

## ⚠️ Nota

Este sistema es de análisis estadístico y generación aleatoria.
No garantiza predicción de resultados reales.
