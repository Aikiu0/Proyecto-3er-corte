const oraciones = JSON.parse(document.getElementById("texto-datos").textContent);

const contenedorTexto = document.getElementById("texto-prueba");
const entrada = document.getElementById("entrada-usuario");
const marcadorTiempo = document.getElementById("tiempo-restante");
const barraProgreso = document.getElementById("barra-progreso");
const pantallaResultado = document.getElementById("pantalla-resultado");
const valorWpm = document.getElementById("valor-wpm");
const cajaTiempo = document.getElementById("tiempo");
const cajaRacha = document.getElementById("racha");
const numeroRacha = document.getElementById("racha-numero");
const imagenResultado = document.getElementById("imagen-resultado");
const nivelResultado = document.getElementById("nivel-resultado");
const fraseResultado = document.getElementById("frase-resultado");

// Niveles de velocidad (caracol / liebre / chita) que manda el servidor
const niveles = JSON.parse(document.getElementById("niveles-datos").textContent);

const DURACION_SEGUNDOS = 60;
const RACHA_MINIMA = 4;
const SEGUNDOS_CRITICOS = 10;

const palabrasPorOracion = oraciones.map((oracion) => oracion.split(/\s+/).filter(Boolean));
const totalPalabras = palabrasPorOracion.reduce((total, lista) => total + lista.length, 0);

let indiceOracion = 0;
let palabras = palabrasPorOracion[indiceOracion];
let indiceActual = 0;
let palabrasCorrectas = 0;
let palabrasCompletadasGlobal = 0;
let tiempoRestante = DURACION_SEGUNDOS;
let intervalo = null;
let pruebaIniciada = false;
let pruebaTerminada = false;
let racha = 0;

function dibujarTexto() {
    contenedorTexto.innerHTML = palabras
        .map((palabra, indice) => {
            const letras = palabra
                .split("")
                .map((letra) => `<span class="letra">${letra}</span>`)
                .join("");
            return `<span class="palabra" data-indice="${indice}">${letras}</span>`;
        })
        .join(" ");
    marcarPalabraActual();
}

function marcarPalabraActual() {
    document.querySelectorAll(".palabra").forEach((elemento) => elemento.classList.remove("actual"));
    const elementoActual = document.querySelector(`.palabra[data-indice="${indiceActual}"]`);
    if (elementoActual) {
        elementoActual.classList.add("actual");
        elementoActual.scrollIntoView({ block: "center", behavior: "smooth" });
    }
}

// Colorea letra por letra la palabra que se esta escribiendo en este momento
function actualizarLetrasPalabraActual() {
    const elementoActual = document.querySelector(`.palabra[data-indice="${indiceActual}"]`);
    if (!elementoActual) {
        return;
    }

    const palabraObjetivo = palabras[indiceActual];
    const letras = elementoActual.querySelectorAll(".letra");
    const escrito = entrada.value;

    letras.forEach((letraElemento, indice) => {
        letraElemento.classList.remove("correcta", "incorrecta", "cursor");
        if (indice < escrito.length) {
            letraElemento.classList.add(escrito[indice] === palabraObjetivo[indice] ? "correcta" : "incorrecta");
        } else if (indice === escrito.length) {
            letraElemento.classList.add("cursor");
        }
    });
}

// La racha solo se muestra a partir de 4 palabras correctas seguidas
function actualizarRacha(acerto) {
    racha = acerto ? racha + 1 : 0;

    if (racha < RACHA_MINIMA) {
        cajaRacha.classList.remove("visible");
        return;
    }

    numeroRacha.textContent = racha;
    cajaRacha.classList.add("visible");

    // Reinicia la animacion de destello en cada palabra nueva
    cajaRacha.classList.remove("pulso");
    void cajaRacha.offsetWidth;
    cajaRacha.classList.add("pulso");
}

function iniciarCuentaRegresiva() {
    intervalo = setInterval(() => {
        tiempoRestante -= 1;
        marcadorTiempo.textContent = tiempoRestante;
        cajaTiempo.classList.toggle("critico", tiempoRestante <= SEGUNDOS_CRITICOS);
        if (tiempoRestante <= 0) {
            finalizarPrueba();
        }
    }, 1000);
}

function finalizarPrueba() {
    if (pruebaTerminada) {
        return;
    }
    pruebaTerminada = true;

    clearInterval(intervalo);
    entrada.disabled = true;

    const segundosUsados = DURACION_SEGUNDOS - tiempoRestante;
    const minutos = segundosUsados > 0 ? segundosUsados / 60 : 1 / 60;
    const palabrasPorMinuto = Math.round(palabrasCorrectas / minutos);

    cajaRacha.classList.remove("visible");
    cajaTiempo.classList.remove("critico");

    valorWpm.textContent = palabrasPorMinuto;
    mostrarImagenVelocidad(palabrasPorMinuto);
    pantallaResultado.classList.add("visible");

    fetch("/guardar_resultado", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ velocidad: palabrasPorMinuto }),
    });
}

// Elige caracol, liebre o chita segun las palabras por minuto logradas
function mostrarImagenVelocidad(palabrasPorMinuto) {
    const nivel = niveles.find((opcion) => palabrasPorMinuto <= opcion.maximo) || niveles[niveles.length - 1];

    imagenResultado.src = nivel.imagen;
    imagenResultado.alt = nivel.nombre;
    nivelResultado.textContent = nivel.nombre;
    fraseResultado.textContent = nivel.frase;
}

// Avanza a la siguiente oracion, o termina la prueba si ya no hay mas
function pasarSiguienteOracion() {
    indiceOracion += 1;

    if (indiceOracion >= palabrasPorOracion.length) {
        finalizarPrueba();
        return;
    }

    palabras = palabrasPorOracion[indiceOracion];
    indiceActual = 0;
    dibujarTexto();
}

// Se ejecuta cuando el usuario confirma una palabra con espacio o enter
function procesarPalabra() {
    const escrita = entrada.value.trim();
    const elementoActual = document.querySelector(`.palabra[data-indice="${indiceActual}"]`);
    const palabraObjetivo = palabras[indiceActual];

    if (elementoActual) {
        const letras = elementoActual.querySelectorAll(".letra");
        letras.forEach((letraElemento, indice) => {
            letraElemento.classList.remove("cursor");
            const correcta = indice < escrita.length && escrita[indice] === palabraObjetivo[indice];
            letraElemento.classList.toggle("correcta", correcta);
            letraElemento.classList.toggle("incorrecta", !correcta);
        });

        const esCorrecta = escrita === palabraObjetivo;
        elementoActual.classList.toggle("correcta", esCorrecta);
        elementoActual.classList.toggle("incorrecta", !esCorrecta);

        if (esCorrecta && !elementoActual.dataset.contada) {
            palabrasCorrectas += 1;
            elementoActual.dataset.contada = "1";
        }

        actualizarRacha(esCorrecta);
    }

    indiceActual += 1;
    palabrasCompletadasGlobal += 1;
    entrada.value = "";
    barraProgreso.style.width = `${(palabrasCompletadasGlobal / totalPalabras) * 100}%`;

    if (indiceActual >= palabras.length) {
        pasarSiguienteOracion();
        return;
    }

    marcarPalabraActual();
}

// Permite volver a la palabra anterior si quedo marcada como incorrecta
function retrocederPalabra() {
    const palabraAnterior = document.querySelector(`.palabra[data-indice="${indiceActual - 1}"]`);
    if (!palabraAnterior || !palabraAnterior.classList.contains("incorrecta")) {
        return;
    }

    indiceActual -= 1;
    palabrasCompletadasGlobal -= 1;
    racha = 0;
    cajaRacha.classList.remove("visible");
    palabraAnterior.classList.remove("correcta", "incorrecta");
    palabraAnterior.querySelectorAll(".letra").forEach((letra) => {
        letra.classList.remove("correcta", "incorrecta", "cursor");
    });

    barraProgreso.style.width = `${(palabrasCompletadasGlobal / totalPalabras) * 100}%`;
    marcarPalabraActual();
}

entrada.addEventListener("input", (evento) => {
    if (pruebaTerminada) {
        return;
    }

    if (!pruebaIniciada) {
        pruebaIniciada = true;
        iniciarCuentaRegresiva();
    }

    if (evento.target.value.endsWith(" ")) {
        procesarPalabra();
        return;
    }

    actualizarLetrasPalabraActual();
});

entrada.addEventListener("keydown", (evento) => {
    if (pruebaTerminada) {
        return;
    }

    if (evento.key === "Enter") {
        evento.preventDefault();
        if (entrada.value.trim().length > 0) {
            entrada.value += " ";
            entrada.dispatchEvent(new Event("input"));
        }
        return;
    }

    if (evento.key === "Backspace" && entrada.value.length === 0 && indiceActual > 0) {
        evento.preventDefault();
        retrocederPalabra();
    }
});

dibujarTexto();
entrada.focus();