-- Base de datos para la aplicacion de mecanografia
-- Ejecutar este script completo en MySQL para dejar todo listo

CREATE DATABASE IF NOT EXISTS mecanografia_db
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE mecanografia_db;

CREATE TABLE Usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    intentos_fallidos INT NOT NULL DEFAULT 0,
    bloqueado_hasta DATETIME NULL
);

CREATE TABLE Texto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(20) NOT NULL,
    contenido TEXT NOT NULL
);

CREATE TABLE Marcador (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    velocidad INT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id) ON DELETE CASCADE
);

-- Textos de ejemplo tipo codigo (python)

INSERT INTO Texto (tipo, contenido) VALUES
('codigo', 'class CuentaBancaria:
    def __init__(self, titular, saldo=0):
        self.titular = titular
        self.saldo = saldo
        self.movimientos = []

    def depositar(self, monto):
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        self.saldo += monto
        self.movimientos.append(("deposito", monto))

    def retirar(self, monto):
        if monto > self.saldo:
            raise ValueError("Fondos insuficientes")
        self.saldo -= monto
        self.movimientos.append(("retiro", monto))

    def historial(self):
        for tipo, monto in self.movimientos:
            print(f"{tipo}: {monto}")

cuenta = CuentaBancaria("Laura", 500)
cuenta.depositar(150)
cuenta.retirar(200)
cuenta.historial()
print(f"Saldo final: {cuenta.saldo}")'),

('codigo', 'def quicksort(lista):
    if len(lista) <= 1:
        return lista
    pivote = lista[len(lista) // 2]
    menores = [x for x in lista if x < pivote]
    iguales = [x for x in lista if x == pivote]
    mayores = [x for x in lista if x > pivote]
    return quicksort(menores) + iguales + quicksort(mayores)

def busqueda_binaria(lista, objetivo):
    inicio, fin = 0, len(lista) - 1
    while inicio <= fin:
        medio = (inicio + fin) // 2
        if lista[medio] == objetivo:
            return medio
        elif lista[medio] < objetivo:
            inicio = medio + 1
        else:
            fin = medio - 1
    return -1

numeros = [9, 3, 7, 1, 8, 2, 5, 4, 6]
ordenados = quicksort(numeros)
print(ordenados)
print(busqueda_binaria(ordenados, 7))'),

('codigo', 'import csv
from dataclasses import dataclass

@dataclass
class Producto:
    nombre: str
    precio: float
    cantidad: int

    def total(self):
        return self.precio * self.cantidad

def leer_inventario(ruta):
    productos = []
    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector)
        for fila in lector:
            nombre, precio, cantidad = fila
            productos.append(Producto(nombre, float(precio), int(cantidad)))
    return productos

def valor_total(productos):
    return sum(producto.total() for producto in productos)

productos = leer_inventario("inventario.csv")
for producto in productos:
    print(f"{producto.nombre}: {producto.total():.2f}")

print(f"Valor total del inventario: {valor_total(productos):.2f}")'),

('codigo', 'def generador_fibonacci(limite):
    a, b = 0, 1
    while a < limite:
        yield a
        a, b = b, a + b

def es_primo(numero):
    if numero < 2:
        return False
    for divisor in range(2, int(numero ** 0.5) + 1):
        if numero % divisor == 0:
            return False
    return True

def primos_hasta(limite):
    return [n for n in range(2, limite) if es_primo(n)]

def registrar_tiempo(funcion):
    def envoltura(*args, **kwargs):
        import time
        inicio = time.time()
        resultado = funcion(*args, **kwargs)
        duracion = time.time() - inicio
        print(f"{funcion.__name__} tardo {duracion:.4f} segundos")
        return resultado
    return envoltura

@registrar_tiempo
def calcular_todo():
    fibonacci = list(generador_fibonacci(100))
    primos = primos_hasta(100)
    return fibonacci, primos

fibonacci, primos = calcular_todo()
print(fibonacci)
print(primos)'),

('codigo', 'from collections import defaultdict

class GestorTareas:
    def __init__(self):
        self.tareas = defaultdict(list)

    def agregar(self, categoria, descripcion, prioridad="media"):
        self.tareas[categoria].append({
            "descripcion": descripcion,
            "prioridad": prioridad,
            "completada": False,
        })

    def completar(self, categoria, indice):
        try:
            self.tareas[categoria][indice]["completada"] = True
        except IndexError:
            print("Esa tarea no existe")

    def pendientes(self, categoria):
        return [t for t in self.tareas[categoria] if not t["completada"]]

    def resumen(self):
        for categoria, lista in self.tareas.items():
            completadas = sum(1 for t in lista if t["completada"])
            print(f"{categoria}: {completadas}/{len(lista)} completadas")

gestor = GestorTareas()
gestor.agregar("trabajo", "Enviar reporte semanal", "alta")
gestor.agregar("trabajo", "Revisar correos", "baja")
gestor.agregar("personal", "Comprar viveres")
gestor.completar("trabajo", 0)
gestor.resumen()');

-- Textos de ejemplo tipo plano

INSERT INTO Texto (tipo, contenido) VALUES
('plano', 'La velocidad al escribir en un teclado se mide normalmente en palabras por minuto y es una habilidad que mejora con la practica constante. No se trata solamente de mover los dedos rapido, sino de reconocer patrones en las palabras y anticipar el siguiente movimiento sin mirar las teclas. Muchas personas que trabajan frente a una computadora todos los dias notan que despues de unas semanas de practica cometen menos errores y logran mantener un ritmo mas parejo durante sesiones largas. La clave esta en la constancia mas que en sesiones intensas y esporadicas, ya que el cuerpo aprende mejor con repeticiones cortas pero frecuentes a lo largo del tiempo.'),

('plano', 'El aprendizaje de cualquier habilidad requiere practica constante, paciencia y la disposicion de equivocarse muchas veces antes de mejorar. No existe una formula magica para dominar algo de la noche a la manana, el progreso llega poco a poco con cada intento, cada error corregido y cada pequena victoria que muchas veces pasa desapercibida. Quienes logran resultados notables casi siempre comparten una misma caracteristica, y es que no dejaron de intentarlo cuando las cosas se pusieron dificiles. Ya sea aprender un idioma nuevo, tocar un instrumento o escribir mas rapido en un teclado, el camino siempre pasa por acumular horas de practica deliberada y estar dispuesto a revisar lo que no esta funcionando.'),

('plano', 'Los primeros teclados mecanicos fueron diseñados para maquinas de escribir mucho antes de que existieran las computadoras personales. Su distribucion de letras, conocida como QWERTY, se creo pensando en evitar que los martillos metalicos de las letras mas usadas se trabaran entre si al escribir rapido. Aunque hoy la tecnologia es completamente distinta, esa misma distribucion de teclas sigue siendo la base de casi todos los teclados modernos que usamos en oficinas, escuelas y hogares alrededor del mundo. Con el paso de los anos han surgido distribuciones alternativas que prometen mayor eficiencia, pero ninguna ha logrado reemplazar la costumbre que millones de personas ya tienen con el diseño original.'),

('plano', 'Mantener una buena postura frente al computador reduce el cansancio y previene molestias en las manos, el cuello y la espalda durante jornadas largas de trabajo o estudio. Es recomendable ajustar la altura de la silla para que los pies queden completamente apoyados en el piso, mantener la pantalla a la altura de los ojos y evitar encorvar los hombros hacia adelante mientras se escribe. Hacer pausas cortas cada cierto tiempo tambien ayuda a que los musculos se relajen y la concentracion se mantenga durante mas tiempo. Pequenos cambios en la forma de sentarse pueden marcar una diferencia importante en la comodidad general al final del dia.'),

('plano', 'Leer con frecuencia amplia el vocabulario de una persona y mejora notablemente la forma en que se expresa tanto al hablar como al escribir. Combinar la lectura con la practica constante de escritura es una manera muy efectiva de fortalecer ambas habilidades al mismo tiempo, ya que una alimenta a la otra de forma natural. Quienes leen distintos tipos de textos, desde noticias hasta cuentos, suelen encontrar mas facil construir oraciones claras y variar el ritmo de lo que escriben. Ademas, la lectura frecuente entrena la mente para reconocer patrones en el lenguaje, lo cual tambien resulta util a la hora de escribir mas rapido y con menos errores.'),

('plano', 'La tecnologia ha cambiado por completo la manera en que las personas se comunican, trabajan y aprenden en su vida diaria. Hace apenas unas decadas, escribir una carta implicaba papel, tinta y varios dias de espera para recibir una respuesta, mientras que hoy un mensaje puede llegar a cualquier parte del mundo en cuestion de segundos. Esta rapidez trae grandes ventajas, pero tambien exige nuevas habilidades, como la capacidad de escribir con claridad y velocidad frente a un teclado. Las escuelas y empresas cada vez valoran mas estas competencias digitales, porque una comunicacion efectiva por escrito se ha vuelto una herramienta fundamental en casi cualquier tipo de trabajo.');