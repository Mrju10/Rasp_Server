from dotenv import load_dotenv
import os
import pymysql.cursors

load_dotenv() # Cargar variables de entorno desde el archivo .env

# Obtener los valores de las variables de entorno
host = os.getenv("HOST")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")

# Verificar que los valores no sean None o cadenas vacías
if host is None or host == "" or \
   username is None or username == "" or \
   password is None or password == "" or \
   database is None or database == "":
    raise ValueError("Las variables de entorno no están definidas correctamente.")

# Configurar la conexión a la base de datos con SSL
connection = pymysql.connect(
  host= host,
  user= username,
  password= password,
  database= database,
  ssl= {
    "ca": "/etc/ssl/cert.pem",
    "cert": "/etc/ssl/client-cert.pem",
    "key": "/etc/ssl/client-key.pem"
  }
)
