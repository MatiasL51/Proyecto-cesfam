from pymongo import MongoClient
from datetime import datetime, timezone

class MongoManager:
    """
    Gestor de conexión y operaciones para la base de datos no relacional MongoDB.
    Utiliza la base de datos 'salud_padrelascasas' y una colección dedicada 
    para la implementación de la Unidad 3.
    """
    def __init__(self, uri="mongodb://localhost:27017/", db_name="salud_padrelascasas"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def registrar_evento_implementacion(self, documento_datos):
        """
        Inserta un documento BSON en la nueva colección 'logs_auditoria_oirs'
        demostrando la persistencia NoSQL desde Django (Unidad 3).
        """
        coleccion = self.db['logs_auditoria_oirs']
        
        if 'fecha_registro' not in documento_datos:
            documento_datos['fecha_registro'] = datetime.now(timezone.utc).isoformat()
            
        resultado = coleccion.insert_one(documento_datos)
        return str(resultado.inserted_id)

# Instancia global
mongo_db = MongoManager()