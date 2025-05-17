from fastapi import HTTPException
from backend.conexion.dataBase import get_admin_supabase
from backend.models import ProcesoCreate, ProcesoUpdate
from backend.textProcessor import get_text_from_url
from urllib.parse import urlparse
import os
import re

supabase = get_admin_supabase()
def normalizar_nombre(nombre: str) -> str:
    return re.sub(r'\W+', '_', nombre.strip().lower())

def get_project_ref(supabase_url: str) -> str:
    parsed_url = urlparse(supabase_url)
    project_ref = parsed_url.netloc.split('.')[0]
    return project_ref

SUPABASE_URL = os.environ.get("SUPABASE_URL")

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

    to_insert = []
    for c in payload.consultas:
        nombre_archivo = f"{c.consulta[:20].replace(' ', '_')}.txt"
        url_archivo = subir_a_storage(carpeta_proceso, c.informacion, nombre_archivo)
        to_insert.append({
            "proceso_id": new_id,
            "consulta": c.consulta,
            "informacion": url_archivo
        })

    ins = supabase.table("base_conocimiento").insert(to_insert).execute()
    if not ins.data:
        raise HTTPException(status_code=500, detail="Error al guardar consultas")

    return {
        "id_proceso": new_id,
        "nombre": payload.nombre,
        "consultas": payload.consultas
    }

def actualizar_proceso(id_proceso: str, payload: ProcesoUpdate):
    upd = supabase.table("procesos").update({"nombre": payload.nombre}).eq("id_proceso", id_proceso).execute()
    if not upd.data:
        raise HTTPException(status_code=500, detail="Error al actualizar proceso")

    supabase.table("base_conocimiento").delete().eq("proceso_id", id_proceso).execute()

    carpeta_proceso = normalizar_nombre(payload.nombre)

    to_insert = []
    for c in payload.consultas:
        nombre_archivo = f"{c.consulta[:20].replace(' ', '_')}.txt"
        url_archivo = subir_a_storage(carpeta_proceso, c.informacion, nombre_archivo)
        to_insert.append({
            "proceso_id": id_proceso,
            "consulta": c.consulta,
            "informacion": url_archivo
        })

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
