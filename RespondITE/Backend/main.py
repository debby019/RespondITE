# Prueba de Endpoints (Se eliminara)
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from db.dataBase import supabase

app = FastAPI()


# Endpoint raíz
@app.get("/")
async def root():
    return {
        "message": "API de RespondITE funcionando",
        "rutas_disponibles": {
            "probar_bd": "/test-db",
            "documentacion": "/docs"
        }
    }


# Endpoint de ejemplo (Devuelve un dato de la tabla base_conocimiento en la ruta  http://127.0.0.1:8000/test-db)
@app.get("/test-db")
async def test_db():
    try:
        response = supabase.table("base_conocimiento").select("*").limit(1).execute()

        if not response.data:
            return JSONResponse(
                status_code=404,
                content={"status": "success", "message": "La tabla está vacía"}
            )

        return JSONResponse({
            "status": "success",
            "data": response.data[0]
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Error en Supabase: {str(e)}",
                "details": "Tabla usada: 'base_conocimiento'"
            }
        )
