from pymongo import MongoClient
from datetime import datetime

class MongoManager:
    """
    Gestor de conexión y operaciones para la base de datos no relacional MongoDB.
    Complementa el almacenamiento híbrido del sistema OIRS del CESFAM.
    """
    def __init__(self, uri="mongodb://localhost:27017/", db_name="cesfam_oirs_no_relacional"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def guardar_encuesta(self, datos_encuesta):
        """
        Inserta un documento BSON con la encuesta de satisfacción anónima o log de auditoría.
        """
        coleccion = self.db['encuestas_satisfaccion']
        
        # Añadir marca de tiempo si no viene incluida
        if 'fecha_registro' not in datos_encuesta:
            datos_encuesta['fecha_registro'] = datetime.utcnow().isoformat()
            
        resultado = coleccion.insert_one(datos_encuesta)
        return str(resultado.inserted_id)

    def obtener_todas_las_encuestas(self):
        """
        Recupera todos los documentos almacenados en la colección no relacional.
        """
        coleccion = self.db['encuestas_satisfaccion']
        return list(coleccion.find({}, {'_id': False})) # Excluye el _id de ObjectId para facilitar lectura si es necesario

# Instancia global para llamadas rápidas desde las vistas de Django
mongo_db = MongoManager()