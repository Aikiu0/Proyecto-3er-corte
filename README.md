# Mecanografía

Aplicación Flask para medir la velocidad de escritura en palabras por minuto.

## INSTALACIÓN
Ejecuta `database.sql` en tu servidor MySQL (por ejemplo desde MySQL Workbench o `mysql -u root -p < database.sql`). Esto crea la base de datos, las tablas y algunos textos de ejemplo.

> Si ya tenías la base de datos creada de antes, no vuelvas a correr `database.sql`: ejecuta `migracion_bloqueo.sql`, que solo agrega las columnas nuevas (`intentos_fallidos` y `bloqueada`) sin borrar tus datos.

Abre `config.py` y ajusta `host`, `user`, `password` y `port` según tu instalación de MySQL.

### Levanta la aplicación:

```
python app.py
```

### Entra a `http://localhost:5000`.

## ESTRUCTURA DE LA BASE DE DATOS

- **Usuario**: datos de la cuenta (nombre, edad, usuario, contraseña con hash).
- **Texto**: textos disponibles para practicar, separados por tipo (`codigo`, `plano`, `personalizado`).
- **Marcador**: resultados de las pruebas, cada fila liga un `usuario_id` con la velocidad obtenida.

## Flujo de la aplicación

1. Login / registro de usuario.
2. Menú con tres tipos de práctica: código Python, texto plano o un archivo propio (.txt / .py).
3. Prueba de escritura palabra por palabra durante 60 segundos, con conteo regresivo y barra de progreso.
4. Al terminar el tiempo (o el texto), se calculan las palabras por minuto y se guardan en `Marcador`.


# ACTIVIDAD

## Errores

- Cambiar el color del botón ‘Entrar’ en la página principal a un color de la paleta de la aplicación.

- Cambiar el texto que está mal escrito en la página en donde el usuario elige el tipo de texto que quiere escribir. El texto debe decir “**¿Con qué texto quieres practicar?**”.

## Modificaciones

- El texto que se desea escribir se debe mostrar oración por oración (una sola línea a la vez).

- El texto que muestra el tiempo (60s) debe mostrarse más grande

- Mover la base de datos local a un servidor en railway.

## Nuevas funciones

- Después de los 4 intentos fallidos de inicio sesion, se debe bloquear la cuenta. 

- Después de atinar 4 palabras seguidas añadir un símbolo o animación de racha.

- Al terminar el test, se debe de mostrar una imagen alusiva a la velocidad del usuario de acuerdo a la siguiente relación:
    - Caracol <30 p/m

    - Liebre>31 p/m

    - Chita >60 p/m

---

# CAMBIOS IMPLEMENTADOS

| Issue | Qué se hizo | Dónde |
|---|---|---|
| #1 Cambiar color del botón | Se quitó el `style="background: #3b82f6"` del botón *Entrar*; ahora usa `--acento` (#5eead4) de la paleta | `templates/login.html` |
| #2 Corregir el texto mal escrito | «¿Coexto quieres practr?» → «¿Con qué texto quieres practicar?» | `templates/menu.html` |
| #4 Mostrar el tiempo | El contador pasó de 14px a 38px y se pinta en rojo parpadeante en los últimos 10 segundos | `templates/test.html`, `static/css/style.css`, `static/js/test.js` |
| #6 Intentos erróneos de inicio de sesión | Se cuentan los fallos en la BD; al llegar a 4 la cuenta queda bloqueada. Un login correcto reinicia el contador y desde el panel de la BD se puede desbloquear | `app.py`, `database.sql`, `templates/admin_bd.html` |
| #7 Icono de racha | A partir de 4 palabras correctas seguidas aparece 🔥 con el número de racha, animado. Se reinicia al fallar una palabra | `templates/test.html`, `static/js/test.js`, `static/css/style.css` |
| #8 Imagen según la velocidad | Al terminar el test se muestra caracol (≤30 ppm), liebre (31–60 ppm) o chita (>60 ppm), con su nombre y una frase | `app.py`, `templates/test.html`, `static/js/test.js`, `static/img/*.svg` |

Las tres imágenes son SVG propios (`static/img/caracol.svg`, `liebre.svg`, `chita.svg`), así que no dependen de internet ni de librerías externas.
