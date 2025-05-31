from fastapi import HTTPException
from backend.conexion.dataBase import get_admin_supabase
from backend.models import ProcesoCreate, ProcesoUpdate
from backend.textProcessor import get_text_from_url
from urllib.parse import urlparse
import os
import re

supabase = get_admin_supabase()

# funciones auxiliares
def normalizar_nombre(nombre: str) -> str:
    return re.sub(r'\W+', '_', nombre.strip().lower())

def get_project_ref(supabase_url: str) -> str:
    parsed_url = urlparse(supabase_url)
    project_ref = parsed_url.netloc.split('.')[0]
    return project_ref

def generar_nombre_archivo(consulta: str) -> str:
    return f"{consulta[:20].replace(' ', '_')}.txt"

def eliminar_archivo_cache(nombre_archivo: str):
    ruta_local = os.path.join("cache_texts", nombre_archivo)
    print(f"Intentando eliminar: {ruta_local}")
    if os.path.exists(ruta_local):
        os.remove(ruta_local)
        print(f"Archivo eliminado: {ruta_local}")
    else:
        print(f"Archivo NO encontrado: {ruta_local}")

def subir_a_storage(carpeta: str, contenido: str, nombre_archivo: str) -> str:
    path = f"{carpeta}/{nombre_archivo}"
    try:
        res = supabase.storage.from_('procesos').upload(path, contenido.encode("utf-8"), {
            "content-type": "text/plain",
            "x-upsert": "true"
        })

        if not res:
            raise Exception("Error al subir archivo a Supabase Storage")

        tiempo = 60 * 60 * 24 * 365 * 200
        signed = supabase.storage.from_('procesos').create_signed_url(path, expires_in=tiempo)

        if not signed or "signedURL" not in signed:
            raise Exception("Error al generar signed URL")

        return signed["signedURL"]

    except Exception as e:
        print("Error al subir a Supabase Storage:", e)
        raise

def procesar_consultas_para_storage(consultas, proceso_id, carpeta_proceso):
    to_insert = []
    for c in consultas:
        nombre_archivo = generar_nombre_archivo(c.consulta)
        url_archivo = subir_a_storage(carpeta_proceso, c.informacion, nombre_archivo)
        get_text_from_url(url_archivo, nombre_archivo)
        to_insert.append({
            "proceso_id": proceso_id,
            "consulta": c.consulta,
            "informacion": url_archivo
        })
    return to_insert

# Funciones principales
def listar_procesos():
    procs = supabase.table("procesos").select("*").execute().data or []
    conocimientos = supabase.table("base_conocimiento").select("*").execute().data or []

    resultados = []
    for p in procs:
        consultas = []
        for c in conocimientos:
            if c["proceso_id"] == p["id_proceso"]:
                url = c["informacion"]
                filename = url.split("/")[-1].split("?")[0]
                contenido = get_text_from_url(url, filename)
                consultas.append({
                    "consulta": c["consulta"],
                    "informacion": contenido
                })
        resultados.append({
            "id_proceso": p["id_proceso"],
            "nombre": p["nombre"],
            "consultas": consultas
        })

    return resultados

def crear_proceso(payload: ProcesoCreate):
    res = supabase.table("procesos").insert({"nombre": payload.nombre}).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="Error al crear proceso")

    new_id = res.data[0]["id_proceso"]
    carpeta_proceso = normalizar_nombre(payload.nombre)

    to_insert = procesar_consultas_para_storage(payload.consultas, new_id, carpeta_proceso)
    ins = supabase.table("base_conocimiento").insert(to_insert).execute()

    if not ins.data:
        raise HTTPException(status_code=500, detail="Error al guardar consultas")

    return {
        "id_proceso": new_id,
        "nombre": payload.nombre,
        "consultas": payload.consultas
    }

def actualizar_proceso(id_proceso: str, payload: ProcesoUpdate):
    datos_actuales = supabase.table("base_conocimiento").select("consulta").eq("proceso_id", id_proceso).execute()
    if datos_actuales.data:
        for fila in datos_actuales.data:
            consulta = fila.get("consulta", "")
            if consulta:
                nombre_archivo = generar_nombre_archivo(consulta)
                eliminar_archivo_cache(nombre_archivo)

    upd = supabase.table("procesos").update({"nombre": payload.nombre}).eq("id_proceso", id_proceso).execute()
    if not upd.data:
        raise HTTPException(status_code=500, detail="Error al actualizar proceso")

    supabase.table("base_conocimiento").delete().eq("proceso_id", id_proceso).execute()

    carpeta_proceso = normalizar_nombre(payload.nombre)
    to_insert = procesar_consultas_para_storage(payload.consultas, id_proceso, carpeta_proceso)
    ins = supabase.table("base_conocimiento").insert(to_insert).execute()

    if not ins.data:
        raise HTTPException(status_code=500, detail="Error al actualizar consultas")
    return {
        "id_proceso": id_proceso,
        "nombre": payload.nombre,
        "consultas": payload.consultas
    }

def eliminar_proceso(id_proceso: str):
    res = supabase.table("procesos").delete().eq("id_proceso", id_proceso).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="Error al eliminar proceso")
    return {"message": "Proceso eliminado"}
