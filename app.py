import random
import re
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from config import get_connection

app = Flask(__name__)
app.secret_key = "cambia-esta-clave-por-una-propia-y-segura"

EXTENSIONES_PERMITIDAS = {"txt", "py"}

# Intentos de inicio de sesion antes de bloquear la cuenta
INTENTOS_MAXIMOS = 4

# Imagen que se muestra al terminar la prueba segun las palabras por minuto
NIVELES_VELOCIDAD = [
    {
        "maximo": 30,
        "nombre": "Caracol",
        "archivo": "img/caracol.svg",
        "frase": "Menos de 30 ppm. Vas con calma, sigue practicando.",
    },
    {
        "maximo": 60,
        "nombre": "Liebre",
        "archivo": "img/liebre.svg",
        "frase": "Entre 31 y 60 ppm. Buen ritmo, ya se nota la práctica.",
    },
    {
        "maximo": 9999,
        "nombre": "Chita",
        "archivo": "img/chita.svg",
        "frase": "Más de 60 ppm. Escribes a toda velocidad.",
    },
]


def archivo_permitido(nombre_archivo):
    return "." in nombre_archivo and nombre_archivo.rsplit(".", 1)[1].lower() in EXTENSIONES_PERMITIDAS


def dividir_en_oraciones(texto, tipo):
    if tipo == "codigo":
        lineas = [linea for linea in texto.split("\n") if linea.strip()]
        return lineas if lineas else [texto]

    oraciones = re.split(r"(?<=[.!?])\s+", texto.strip())
    oraciones = [o.strip() for o in oraciones if o.strip()]
    return oraciones if oraciones else [texto]


def login_requerido(vista):
    # Evita que se acceda a rutas internas sin haber iniciado sesion
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login"))
        return vista(*args, **kwargs)

    return envoltura


@app.route("/")
def login():
    if "usuario_id" in session:
        return redirect(url_for("menu"))
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def procesar_login():
    usuario = request.form.get("usuario", "").strip()
    contrasena = request.form.get("contrasena", "")

    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM Usuario WHERE usuario = %s", (usuario,))
            fila = cursor.fetchone()

            # Usuario inexistente: no se avisa cual de los dos datos fallo
            if not fila:
                flash("Usuario o contraseña incorrectos")
                return redirect(url_for("login"))

            if fila["bloqueada"]:
                flash("Esta cuenta está bloqueada por superar los 4 intentos fallidos.")
                return redirect(url_for("login"))

            # Acceso correcto: se reinicia el contador de intentos
            if check_password_hash(fila["contrasena"], contrasena):
                cursor.execute("UPDATE Usuario SET intentos_fallidos = 0 WHERE id = %s", (fila["id"],))
                conexion.commit()
                session["usuario_id"] = fila["id"]
                session["usuario"] = fila["usuario"]
                return redirect(url_for("menu"))

            # Contraseña incorrecta: se suma el intento y se bloquea al llegar al limite
            intentos = fila["intentos_fallidos"] + 1
            bloquear = intentos >= INTENTOS_MAXIMOS
            cursor.execute(
                "UPDATE Usuario SET intentos_fallidos = %s, bloqueada = %s WHERE id = %s",
                (intentos, 1 if bloquear else 0, fila["id"]),
            )
        conexion.commit()
    finally:
        conexion.close()

    if bloquear:
        flash("Cuenta bloqueada: llegaste a 4 intentos fallidos de inicio de sesión.")
    else:
        restantes = INTENTOS_MAXIMOS - intentos
        flash(f"Usuario o contraseña incorrectos. Te quedan {restantes} intento(s) antes del bloqueo.")

    return redirect(url_for("login"))


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "GET":
        return render_template("registro.html")

    nombre = request.form.get("nombre", "").strip()
    edad = request.form.get("edad", "").strip()
    usuario = request.form.get("usuario", "").strip()
    contrasena = request.form.get("contrasena", "")

    if not nombre or not edad or not usuario or not contrasena:
        flash("Completa todos los campos")
        return redirect(url_for("registro"))

    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id FROM Usuario WHERE usuario = %s", (usuario,))
            if cursor.fetchone():
                flash("Ese nombre de usuario ya existe")
                return redirect(url_for("registro"))

            cursor.execute(
                "INSERT INTO Usuario (nombre, edad, usuario, contrasena) VALUES (%s, %s, %s, %s)",
                (nombre, edad, usuario, generate_password_hash(contrasena)),
            )
        conexion.commit()
    finally:
        conexion.close()

    flash("Cuenta creada, ahora inicia sesión")
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/menu")
@login_requerido
def menu():
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                SELECT u.usuario AS usuario, MAX(m.velocidad) AS mejor_velocidad
                FROM Marcador m
                JOIN Usuario u ON u.id = m.usuario_id
                GROUP BY u.id, u.usuario
                ORDER BY mejor_velocidad DESC
                LIMIT 3
                """
            )
            top_usuarios = cursor.fetchall()
    finally:
        conexion.close()

    return render_template("menu.html", usuario=session["usuario"], top_usuarios=top_usuarios)


@app.route("/personalizado", methods=["GET", "POST"])
@login_requerido
def personalizado():
    if request.method == "GET":
        return render_template("personalizado.html")

    archivo = request.files.get("archivo")
    if not archivo or archivo.filename == "" or not archivo_permitido(archivo.filename):
        flash("Sube un archivo .txt o .py válido")
        return redirect(url_for("personalizado"))

    contenido = archivo.read().decode("utf-8", errors="ignore").strip()
    if not contenido:
        flash("El archivo está vacío")
        return redirect(url_for("personalizado"))

    nombre_archivo = secure_filename(archivo.filename)

    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Texto (tipo, contenido) VALUES (%s, %s)",
                ("personalizado", contenido),
            )
            texto_id = cursor.lastrowid
        conexion.commit()
    finally:
        conexion.close()

    return redirect(url_for("test", tipo="personalizado", texto_id=texto_id, nombre=nombre_archivo))


@app.route("/test/<tipo>")
@login_requerido
def test(tipo):
    if tipo not in ("codigo", "plano", "personalizado"):
        return redirect(url_for("menu"))

    texto_id = request.args.get("texto_id")
    nombre_archivo = request.args.get("nombre", "")

    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            if texto_id:
                cursor.execute("SELECT * FROM Texto WHERE id = %s", (texto_id,))
                texto = cursor.fetchone()
            else:
                cursor.execute("SELECT * FROM Texto WHERE tipo = %s", (tipo,))
                textos = cursor.fetchall()
                texto = random.choice(textos) if textos else None
    finally:
        conexion.close()

    if not texto:
        flash("No hay textos disponibles para esta opción")
        return redirect(url_for("menu"))

    titulos = {
        "codigo": "practica.py",
        "plano": "documento.txt",
        "personalizado": nombre_archivo or "personalizado.txt",
    }

    oraciones = dividir_en_oraciones(texto["contenido"], tipo)

    niveles = [
        {
            "maximo": nivel["maximo"],
            "nombre": nivel["nombre"],
            "frase": nivel["frase"],
            "imagen": url_for("static", filename=nivel["archivo"]),
        }
        for nivel in NIVELES_VELOCIDAD
    ]

    return render_template("test.html", oraciones=oraciones, titulo=titulos[tipo], niveles=niveles)


@app.route("/guardar_resultado", methods=["POST"])
@login_requerido
def guardar_resultado():
    datos = request.get_json(silent=True) or {}
    velocidad = int(datos.get("velocidad", 0))

    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Marcador (usuario_id, velocidad, fecha) VALUES (%s, %s, %s)",
                (session["usuario_id"], velocidad, datetime.now()),
            )
        conexion.commit()
    finally:
        conexion.close()

    return jsonify({"ok": True})


@app.route("/admin/bd")
@login_requerido
def admin_bd():
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, nombre, edad, usuario, fecha_registro, intentos_fallidos, bloqueada
                FROM Usuario ORDER BY id
                """
            )
            usuarios = cursor.fetchall()

            cursor.execute(
                """
                SELECT m.id, u.usuario, m.velocidad, m.fecha
                FROM Marcador m
                JOIN Usuario u ON u.id = m.usuario_id
                ORDER BY m.fecha DESC
                """
            )
            marcadores = cursor.fetchall()

            cursor.execute("SELECT id, tipo, LEFT(contenido, 60) AS contenido FROM Texto ORDER BY id")
            textos = cursor.fetchall()
    finally:
        conexion.close()

    return render_template("admin_bd.html", usuarios=usuarios, marcadores=marcadores, textos=textos)


@app.route("/admin/desbloquear/<int:usuario_id>", methods=["POST"])
@login_requerido
def desbloquear_usuario(usuario_id):
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE Usuario SET intentos_fallidos = 0, bloqueada = 0 WHERE id = %s",
                (usuario_id,),
            )
        conexion.commit()
    finally:
        conexion.close()

    flash("Cuenta desbloqueada")
    return redirect(url_for("admin_bd"))


if __name__ == "__main__":
    app.run(debug=True)