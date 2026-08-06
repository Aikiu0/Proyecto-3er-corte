-- Ejecutar SOLO si ya tenias la base de datos creada y no quieres perder los datos.
-- Si vas a correr database.sql desde cero, no hace falta este archivo.

USE mecanografia_db;

ALTER TABLE Usuario
    ADD COLUMN intentos_fallidos INT NOT NULL DEFAULT 0,
    ADD COLUMN bloqueada TINYINT(1) NOT NULL DEFAULT 0;

-- Para desbloquear una cuenta a mano:
-- UPDATE Usuario SET intentos_fallidos = 0, bloqueada = 0 WHERE usuario = 'nombre_del_usuario';
