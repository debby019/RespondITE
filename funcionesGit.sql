--Trigger
-- Función que se ejecutará antes de insertar en Help_Request
CREATE OR REPLACE FUNCTION verificar_peticiones_activas()
RETURNS TRIGGER AS $$
BEGIN
  -- Verificamos si ya hay una solicitud activa del mismo usuario 
  IF EXISTS (
    SELECT 1 FROM Help_Request 
    WHERE Chat_id = NEW.Chat_id AND Estado = 'activa'
  ) THEN
    RAISE EXCEPTION 'Ya existe una solicitud activa para este usuario.';
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--Creamos el trigger que ejecuta esta función al hacer un INSERT en Help_Request:
CREATE TRIGGER trigger_verificar_peticiones_activas
BEFORE INSERT ON Help_Request
FOR EACH ROW
EXECUTE FUNCTION verificar_peticiones_activas();

-- Función para obtener número de consultas por proceso
CREATE OR REPLACE FUNCTION obtener_consultas_por_proceso()
RETURNS TABLE (
    Proceso VARCHAR,
    Total_Consultas INTEGER
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    p.Nombre AS Proceso,
    COUNT(bc.ID_Conocimiento) AS Total_Consultas
  FROM Procesos p
  JOIN Base_Conocimiento bc ON bc.Proceso_id = p.ID_Proceso
  GROUP BY p.Nombre
  ORDER BY Total_Consultas DESC;
END;
$$ LANGUAGE plpgsql;

--consulta
SELECT * FROM obtener_consultas_por_proceso();