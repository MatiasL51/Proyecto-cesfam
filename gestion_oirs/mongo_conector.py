from pymongo import MongoClient
from datetime import datetime, timezone

class MongoManager:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="salud_padrelascasas"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def registrar_evento_implementacion(self, documento_datos):
        coleccion = self.db['logs_auditoria_oirs']
        
        if 'fecha_registro' not in documento_datos:
            documento_datos['fecha_registro'] = datetime.now(timezone.utc).isoformat()
            
        resultado = coleccion.insert_one(documento_datos)
        return str(resultado.inserted_id)

# Instancia global
mongo_db = MongoManager()