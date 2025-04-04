CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabla Usuarios
CREATE TABLE Usuarios (
    ID_usuario UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    Rol VARCHAR(20) NOT NULL,
    Password VARCHAR(300) NOT NULL,
    Nombre VARCHAR(50) NOT NULL,
    Email VARCHAR(50) UNIQUE NOT NULL
);

-- Tabla Chat
CREATE TABLE Chat (
    ID_Chat UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    Usuario_id UUID NOT NULL,
    Fecha_inicio TIMESTAMP NOT NULL DEFAULT now(),
    FOREIGN KEY (Usuario_id) REFERENCES Usuarios(ID_usuario) ON DELETE CASCADE
);

-- Tabla Mensaje
CREATE TABLE Mensaje (
    ID_Mensaje UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    Chat_id UUID NOT NULL,
    Mensaje TEXT NOT NULL,
    Remitente VARCHAR(20) NOT NULL,
    Fecha_Envio DATE NOT NULL DEFAULT CURRENT_DATE,
    FOREIGN KEY (Chat_id) REFERENCES Chat(ID_Chat) ON DELETE CASCADE
);

-- Tabla Help_Request
CREATE TABLE Help_Request (
    ID_Help UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    Chat_id UUID NOT NULL,
    Estado VARCHAR(20) NOT NULL,
    Fecha TIMESTAMP NOT NULL DEFAULT now(),
    FOREIGN KEY (Chat_id) REFERENCES Chat(ID_Chat) ON DELETE CASCADE
);

-- Tabla Procesos
CREATE TABLE Procesos (
    ID_Proceso UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    Nombre VARCHAR(50) NOT NULL
);

-- Tabla Base_Conocimiento
CREATE TABLE Base_Conocimiento (
    ID_Conocimiento UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    Proceso_id UUID NOT NULL,
    Consulta TEXT NOT NULL,
    Informacion TEXT NOT NULL,
    embedding JSONB,
    FOREIGN KEY (Proceso_id) REFERENCES Procesos(ID_Proceso) ON DELETE CASCADE
);

-- Tabla Mensaje-Proceso 
CREATE TABLE Mensaje_Proceso (
    ID UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    Mensaje_id UUID NOT NULL,
    Proceso_id UUID NOT NULL,
    FOREIGN KEY (Mensaje_id) REFERENCES Mensaje(ID_Mensaje) ON DELETE CASCADE,
    FOREIGN KEY (Proceso_id) REFERENCES Procesos(ID_Proceso) ON DELETE CASCADE
);


-- Datos en tabla Procesos
INSERT INTO Procesos (ID_Proceso, Nombre) VALUES
('eaa84cae-9bc7-4d65-8e9d-13c768e90bdf', 'Credenciales');

-- Datos en tabla Base_Conocimiento
INSERT INTO Base_Conocimiento (ID_Conocimiento, Proceso_id, Consulta, Informacion, embedding) VALUES
('89c426a0-935c-492d-82a1-a0263ddc5001', 'eaa84cae-9bc7-4d65-8e9d-13c768e90bdf', 'Solicitud', 'https://nulsoiwjscvaxzxyjfgm.supabase.co/storage/v1/object/sign/credenciales/Solicitud.txt?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJjcmVkZW5jaWFsZXMvU29saWNpdHVkLnR4dCIsImlhdCI6MTc0MjUwMzczMiwiZXhwIjoxNzUxMTQzNzMyfQ.xCjHsNPjN4_zNihbo-OLW-ECzAyu_h2XWC6X8Ua8-lM', NULL),
('f39c2998-3cc3-4024-bcdf-39f68ab36e37', 'eaa84cae-9bc7-4d65-8e9d-13c768e90bdf', 'Pago', 'https://nulsoiwjscvaxzxyjfgm.supabase.co/storage/v1/object/sign/credenciales/Pago.txt?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJjcmVkZW5jaWFsZXMvUGFnby50eHQiLCJpYXQiOjE3NDI1MDM5NzIsImV4cCI6NDg5NjEwMzk3Mn0.M6QWpwpn6PG_0QLGN9VSup5yykYArMkk7QsAYoe3f00', NULL),
('c98c6601-29bc-4e19-a35f-fcbc4e955339', 'eaa84cae-9bc7-4d65-8e9d-13c768e90bdf', 'Funciones', 'https://nulsoiwjscvaxzxyjfgm.supabase.co/storage/v1/object/sign/credenciales/Funciones.txt?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJjcmVkZW5jaWFsZXMvRnVuY2lvbmVzLnR4dCIsImlhdCI6MTc0MjUwNDE2NiwiZXhwIjo0ODk2MTA0MTY2fQ.oo0XuUHJHXDjXnNzE8TEZKiJqyDvRVmuomp0HkUpOHI', NULL),
('7bf130e8-cfd5-44d7-a541-bf2e5be19414', 'eaa84cae-9bc7-4d65-8e9d-13c768e90bdf', 'Casos de Pago', 'https://nulsoiwjscvaxzxyjfgm.supabase.co/storage/v1/object/sign/credenciales/Cuando%20pagar.txt?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJjcmVkZW5jaWFsZXMvQ3VhbmRvIHBhZ2FyLnR4dCIsImlhdCI6MTc0MzM5MDMxOCwiZXhwIjo4MDUwNTkwMzE4fQ.6OlieN_cpF821fT_7H_cG4_z85p46rxU46vp-FUR-Xk', NULL),
('c39cd1b6-ce8e-4807-a83d-9ebba6a7d71d', 'eaa84cae-9bc7-4d65-8e9d-13c768e90bdf', 'Errores', 'https://nulsoiwjscvaxzxyjfgm.supabase.co/storage/v1/object/sign/credenciales/Errores.txt?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJjcmVkZW5jaWFsZXMvRXJyb3Jlcy50eHQiLCJpYXQiOjE3NDMzOTA0NDQsImV4cCI6ODA1MDU5MDQ0NH0.E36x1dfYxmCgU14tvr7rjiA-j1_fu94i7g_vBjAt0rk', NULL),
('85daea78-d06c-4be3-8f20-e06b16288120', 'eaa84cae-9bc7-4d65-8e9d-13c768e90bdf', 'Fotografía', 'https://nulsoiwjscvaxzxyjfgm.supabase.co/storage/v1/object/sign/credenciales/Foto.txt?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJjcmVkZW5jaWFsZXMvRm90by50eHQiLCJpYXQiOjE3NDMzOTA0ODUsImV4cCI6ODA1MDU5MDQ4NX0.HTBjRV-gePVLC2wJFsUoSs6Z2RU-FtCmgTyo2zh8PWY', NULL),
('8cea8b69-3089-49bc-83f4-adb8529e8d9c', 'eaa84cae-9bc7-4d65-8e9d-13c768e90bdf', 'Vencimiento de la credencial', 'https://nulsoiwjscvaxzxyjfgm.supabase.co/storage/v1/object/sign/credenciales/vencimiento.txt?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJjcmVkZW5jaWFsZXMvdmVuY2ltaWVudG8udHh0IiwiaWF0IjoxNzQzMzkwNjUxLCJleHAiOjgwNTA1OTA2NTF9.4SvOic6IBGkwSLMXK9Fg2OYuhyl3OSE899zVn6CYn9Q', NULL);
