from datetime import datetime, timezone
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from decouple import config

# Configuración de conexión segura a MongoDB mediante variables de entorno (.env)
MONGO_URI = config('MONGO_URI', default='mongodb://localhost:27017/')
DB_NAME = config('MONGO_DB_NAME', default='salud_padrelascasas')

class MongoConector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoConector, cls).__new__(cls)
            cls._instance.client = MongoClient(MONGO_URI)
            cls._instance.db = cls._instance.client[DB_NAME]
        return cls._instance

    @classmethod
    def registrar_log_auditoria(cls, documento_datos):
        try:
            db = cls().db
            coleccion = db['logs_auditoria_oirs']
            
            # Validación preventiva de campos nulos o vacíos críticos
            if not documento_datos or not isinstance(documento_datos, dict):
                raise ValueError("El documento de auditoría contiene datos nulos o formato inválido.")
            
            # Incorporar marca de tiempo UTC si no viene especificada
            if 'fecha_registro' not in documento_datos:
                documento_datos['fecha_registro'] = datetime.now(timezone.utc).isoformat()
            
            resultado = coleccion.insert_one(documento_datos)
            return str(resultado.inserted_id)
            
        except PyMongoError as e:
            print(f"Error de conexión o escritura en MongoDB: {e}")
            return None
        except ValueError as ve:
            print(f"Advertencia de validación: {ve}")
            return None

    @classmethod
    def consultar_log_por_criterio(cls, filtro):
        try:
            db = cls().db
            coleccion = db['logs_auditoria_oirs']
            
            # Ejecución de consulta con manejo de cursores vacíos
            resultado = coleccion.find_one(filtro)
            if resultado is None:
                return {"estado": "vacio", "mensaje": "No se encontraron registros coincidentes o los parámetros son nulos."}
            return resultado
        except PyMongoError as e:
            return {"estado": "error", "mensaje": str(e)}

# Instancia global compatible con el sistema
mongo_db = MongoConector()