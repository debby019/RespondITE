from fastapi import APIRouter, Depends
from backend.models import ProcesoCreate, ProcesoUpdate, ProcesoOut
from backend.logic.auth import verificar_token
from backend.logic.admin import *
from typing import List

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/procesos", response_model=List[ProcesoOut])
def get_procesos(user=Depends(verificar_token)):
    return listar_procesos()

@router.post("/procesos", response_model=ProcesoOut)
def post_proceso(payload: ProcesoCreate, user=Depends(verificar_token)):
    return crear_proceso(payload)

@router.put("/procesos/{id_proceso}", response_model=ProcesoOut)
def put_proceso(id_proceso: str, payload: ProcesoUpdate, user=Depends(verificar_token)):
    return actualizar_proceso(id_proceso, payload)

@router.delete("/procesos/{id_proceso}")
def del_proceso(id_proceso: str, user=Depends(verificar_token)):
    return eliminar_proceso(id_proceso)