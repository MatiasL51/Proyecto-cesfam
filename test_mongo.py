from gestion_oirs.mongo_conector import mongo_db

print("=== INICIO DE PRUEBAS TÉCNICAS MONGODB (LOGS OIRS) ===")

# 1. Prueba de inserción correcta con datos válidos
documento_prueba = {
    "establecimiento": "CESFAM Padre Las Casas",
    "tipo_evento": "REGISTRO_OIRS",
    "folio_referencia": "OIRS-2026-9988",
    "calificacion_global": 5,
    "observacion": "Excelente atención en mesón de informaciones."
}

id_generado = mongo_db.registrar_log_auditoria(documento_prueba)
print(f"[+] Documento insertado con éxito. ID MongoDB: {id_generado}")

# 2. Prueba de consulta normal (Encontrando el registro existente)
print("\n--- Ejecutando Búsqueda Existente ---")
resultado_valido = mongo_db.consultar_log_por_criterio({"folio_referencia": "OIRS-2026-9988"})
print("Resultado obtenido:", resultado_valido)

# 3. Prueba de escenario con datos nulos o filtros inexistentes (Manejo de vacíos)
print("\n--- Ejecutando Búsqueda con Filtros Nulos / Inexistentes ---")
resultado_nulo = mongo_db.consultar_log_por_criterio({
    "folio_referencia": "FOLIO-QUE-NO-EXISTE-999",
    "calificacion_global": None
})
print("Resultado obtenido ante datos nulos:", resultado_nulo)

# 4. Prueba de validación preventiva enviando un diccionario vacío (Datos nulos)
print("\n--- Ejecutando Inserción con Datos Nulos/Vacíos ---")
id_invalido = mongo_db.registrar_log_auditoria(None)
print("Respuesta ante inserción nula (esperado None):", id_invalido)

print("\n=== PRUEBAS FINALES COMPLETADAS CON ÉXITO ===")