from pymongo import MongoClient
from datetime import datetime

class MongoManager:
    """
    Gestor de conexión y operaciones para la base de datos no relacional MongoDB.
    Utiliza la base de datos 'salud_padrelascasas' para el sistema OIRS del CESFAM.
    """
    def __init__(self, uri="mongodb://localhost:27017/", db_name="salud_padrelascasas"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def guardar_encuesta(self, datos_encuesta):
        """
        Inserta un documento BSON con la encuesta de satisfacción anónima o log de auditoría.
        """
        coleccion = self.db['encuestas_satisfaccion']
        
        if 'fecha_registro' not in datos_encuesta:
            datos_encuesta['fecha_registro'] = datetime.utcnow().isoformat()
            
        resultado = coleccion.insert_one(datos_encuesta)
        return str(resultado.inserted_id)

# Instancia global para llamadas rápidas
mongo_db = MongoManager()