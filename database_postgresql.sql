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