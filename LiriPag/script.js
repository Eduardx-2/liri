const THEME_KEY = "liri-theme";
const FRASE_LINEAS = ["“Creer que algo", "es real hace que", "sea real”"];
const LERP_MS = 280;

const form = document.getElementById("form-busqueda");
const input = document.getElementById("telefono");
const errorEl = document.getElementById("error-telefono");
const estadoEl = document.getElementById("estado-busqueda");
const avisoEl = document.getElementById("resultado-aviso");
const vistaLanding = document.getElementById("vista-landing");
const vistaResultados = document.getElementById("vista-resultados");
const telefonoEl = document.getElementById("resultado-telefono");
const companiaEl = document.getElementById("resultado-compania");
const deudasEl = document.getElementById("lista-deudas");
const redesEl = document.getElementById("lista-redes");
const tituloResultados = document.getElementById("titulo-resultados");
const btnVolver = document.getElementById("btn-volver");
const btnTema = document.getElementById("btn-tema");
const canvas = document.getElementById("particulas");
const ctx = canvas.getContext("2d");
const fraseTexto = document.getElementById("frase-texto");
const fraseCursor = document.getElementById("frase-cursor");

const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

function temaActual() {
  return document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
}

function aplicarTema(tema, { lerp = true } = {}) {
  document.documentElement.setAttribute("data-theme", tema);
  localStorage.setItem(THEME_KEY, tema);
  const oscuro = tema === "dark";
  btnTema.setAttribute("aria-pressed", String(oscuro));
  btnTema.setAttribute("aria-label", oscuro ? "Activar modo claro" : "Activar modo oscuro");

  const destino = parseRgba(colorParticulaCss());
  if (lerp && !reduceMotion.matches) {
    iniciarLerpParticulas(destino);
  } else {
    colorActual = destino;
    lerpStart = 0;
    if (reduceMotion.matches) {
      dibujarParticulas();
    }
  }
}

function iniciarTema() {
  aplicarTema(temaActual(), { lerp: false });
}

btnTema.addEventListener("click", () => {
  aplicarTema(temaActual() === "dark" ? "light" : "dark");
});

function formatearTelefono(raw) {
  const trimmed = raw.trim();
  const digits = trimmed.replace(/\D/g, "");
  let local = null;

  if (digits.length === 8) {
    local = digits;
  } else if (digits.length === 11 && digits.startsWith("503")) {
    local = digits.slice(3);
  } else if (digits.length === 13 && digits.startsWith("00503")) {
    local = digits.slice(5);
  }

  if (local) {
    return `+503 ${local.slice(0, 4)}-${local.slice(4)}`;
  }

  return trimmed;
}

function pintarDeudas(deudas) {
  deudasEl.replaceChildren();

  if (!deudas.length) {
    const vacio = document.createElement("p");
    vacio.className = "sin-registros";
    vacio.textContent = "Sin registros";
    deudasEl.appendChild(vacio);
    return;
  }

  deudas.forEach((deuda) => {
    const fila = document.createElement("li");
    fila.className = "deuda-fila";

    if (deuda.monto) {
      const monto = document.createElement("span");
      monto.className = "deuda-monto";
      monto.textContent = deuda.monto;
      fila.appendChild(monto);
    }

    if (deuda.fecha) {
      const fecha = document.createElement("span");
      fecha.className = "deuda-fecha";
      fecha.textContent = `Fecha: ${deuda.fecha}`;
      fila.appendChild(fecha);
    }

    if (deuda.idFactura) {
      const id = document.createElement("span");
      id.className = "deuda-id";
      id.textContent = `ID: ${deuda.idFactura}`;
      fila.appendChild(id);
    }
    deudasEl.appendChild(fila);
  });
}

function pintarRedes(redes) {
  redesEl.replaceChildren();

  if (!redes.length) {
    const vacio = document.createElement("p");
    vacio.className = "sin-registros";
    vacio.textContent = "Sin registros";
    redesEl.appendChild(vacio);
    return;
  }

  redes.forEach((nombre) => {
    const chip = document.createElement("span");
    chip.className = "chip";

    const label = document.createElement("span");
    label.textContent = nombre;

    const check = document.createElement("span");
    check.className = "ok";
    check.setAttribute("aria-hidden", "true");
    check.textContent = "✓";

    chip.append(label, check);
    redesEl.appendChild(chip);
  });
}

function mostrarResultados(numeroIngresado, data) {
  telefonoEl.textContent = formatearTelefono(
    data.telefono != null ? String(data.telefono) : numeroIngresado
  );
  companiaEl.textContent = data.compania || "Sin registros";
  if (data.error) {
    avisoEl.hidden = false;
    avisoEl.textContent = data.error;
  } else {
    avisoEl.hidden = true;
    avisoEl.textContent = "";
  }
  pintarDeudas(data.deudas || []);
  pintarRedes(data.redes || []);

  vistaLanding.hidden = true;
  vistaLanding.inert = true;
  vistaResultados.hidden = false;
  vistaResultados.inert = false;
  window.scrollTo(0, 0);
  tituloResultados.focus();
}

function setEstado(texto) {
  estadoEl.textContent = texto;
  estadoEl.hidden = !texto;
}

function mostrarLanding() {
  errorEl.textContent = "";
  setEstado("");
  input.removeAttribute("aria-invalid");
  vistaResultados.hidden = true;
  vistaResultados.inert = true;
  vistaLanding.hidden = false;
  vistaLanding.inert = false;
  window.scrollTo(0, 0);
  escribirFrase();
  input.focus();
}

input.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    form.requestSubmit();
  }
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const valor = input.value.trim();
  const btnBuscar = form.querySelector(".btn-buscar");

  if (!valor) {
    errorEl.textContent = "Ingresa un numero de telefono.";
    input.setAttribute("aria-invalid", "true");
    input.focus();
    return;
  }

  errorEl.textContent = "";
  input.removeAttribute("aria-invalid");

  const textoBoton = btnBuscar ? btnBuscar.textContent : "";
  if (btnBuscar) {
    btnBuscar.disabled = true;
    btnBuscar.textContent = "Consultando…";
    btnBuscar.setAttribute("aria-busy", "true");
  }
  input.disabled = true;
  setEstado("Consultando… puede tardar cerca de un minuto.");
  let fallo = false;

  try {
    const data = await LiriApi.consultarNumero(valor);

    if (!data.ok) {
      errorEl.textContent = data.error || "No se pudo consultar el número.";
      input.setAttribute("aria-invalid", "true");
      fallo = true;
      return;
    }

    mostrarResultados(valor, data);
  } catch (err) {
    errorEl.textContent = "No se pudo conectar con el servidor.";
    input.setAttribute("aria-invalid", "true");
    fallo = true;
  } finally {
    input.disabled = false;
    setEstado("");
    if (btnBuscar) {
      btnBuscar.disabled = false;
      btnBuscar.textContent = textoBoton;
      btnBuscar.removeAttribute("aria-busy");
    }
    if (fallo) input.focus();
  }
});

btnVolver.addEventListener("click", mostrarLanding);

let particles = [];
let rafId = 0;
let colorActual = { r: 26, g: 26, b: 26, a: 0.62 };
let colorDesde = colorActual;
let colorHasta = colorActual;
let lerpStart = 0;
let typeTimer = 0;

function colorParticulaCss() {
  return getComputedStyle(document.documentElement).getPropertyValue("--particle").trim();
}

function parseRgba(str) {
  const m = str.match(
    /rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)(?:\s*,\s*([\d.]+))?\s*\)/i
  );
  if (!m) {
    return { r: 26, g: 26, b: 26, a: 0.62 };
  }
  return {
    r: Number(m[1]),
    g: Number(m[2]),
    b: Number(m[3]),
    a: m[4] === undefined ? 1 : Number(m[4]),
  };
}

function rgbaString(c) {
  return `rgba(${Math.round(c.r)}, ${Math.round(c.g)}, ${Math.round(c.b)}, ${c.a})`;
}

function lerp(a, b, t) {
  return a + (b - a) * t;
}

function lerpColor(from, to, t) {
  const clamped = Math.min(1, Math.max(0, t));
  return {
    r: lerp(from.r, to.r, clamped),
    g: lerp(from.g, to.g, clamped),
    b: lerp(from.b, to.b, clamped),
    a: lerp(from.a, to.a, clamped),
  };
}

function iniciarLerpParticulas(destino) {
  colorDesde = { ...colorActual };
  colorHasta = destino;
  lerpStart = performance.now();
}

function colorDibujo() {
  if (!lerpStart) {
    return colorActual;
  }
  const t = (performance.now() - lerpStart) / LERP_MS;
  if (t >= 1) {
    colorActual = colorHasta;
    lerpStart = 0;
    return colorActual;
  }
  colorActual = lerpColor(colorDesde, colorHasta, t);
  return colorActual;
}

function cantidadParticulas() {
  const area = window.innerWidth * window.innerHeight;
  if (window.innerWidth < 640) {
    return Math.max(18, Math.min(36, Math.floor(area / 18000)));
  }
  return Math.max(40, Math.min(90, Math.floor(area / 14000)));
}

function extraRadio() {
  const light = 0.35;
  const dark = 0;
  if (!lerpStart) {
    return temaActual() === "light" ? light : dark;
  }
  const t = Math.min(1, (performance.now() - lerpStart) / LERP_MS);
  const from = colorDesde.r < 80 ? light : dark;
  const to = colorHasta.r < 80 ? light : dark;
  return lerp(from, to, t);
}

function crearParticulas() {
  const n = cantidadParticulas();
  particles = Array.from({ length: n }, () => ({
    x: Math.random() * window.innerWidth,
    y: Math.random() * window.innerHeight,
    vx: (Math.random() - 0.5) * 0.35,
    vy: (Math.random() - 0.5) * 0.35,
    r: Math.random() * 1.4 + 0.6,
  }));
}

function ajustarCanvas() {
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  const w = window.innerWidth;
  const h = window.innerHeight;
  canvas.width = Math.floor(w * dpr);
  canvas.height = Math.floor(h * dpr);
  canvas.style.width = `${w}px`;
  canvas.style.height = `${h}px`;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  crearParticulas();
}

function dibujarParticulas() {
  const w = window.innerWidth;
  const h = window.innerHeight;
  const color = rgbaString(colorDibujo());
  const estatico = reduceMotion.matches;
  const radioExtra = extraRadio();

  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = color;
  ctx.strokeStyle = color;

  for (const p of particles) {
    if (!estatico) {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0 || p.x > w) p.vx *= -1;
      if (p.y < 0 || p.y > h) p.vy *= -1;
    }

    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r + radioExtra, 0, Math.PI * 2);
    ctx.fill();
  }

  if (!estatico) {
    const maxDist = w < 640 ? 90 : 130;
    for (let i = 0; i < particles.length; i += 1) {
      for (let j = i + 1; j < particles.length; j += 1) {
        const a = particles[i];
        const b = particles[j];
        const dx = a.x - b.x;
        const dy = a.y - b.y;
        const dist = Math.hypot(dx, dy);
        if (dist < maxDist) {
          ctx.globalAlpha = (1 - dist / maxDist) * 0.45;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
          ctx.globalAlpha = 1;
        }
      }
    }

    rafId = requestAnimationFrame(dibujarParticulas);
  }
}

function iniciarParticulas() {
  cancelAnimationFrame(rafId);
  ajustarCanvas();
  colorActual = parseRgba(colorParticulaCss());
  lerpStart = 0;
  dibujarParticulas();
}

function pintarFrase(lineas) {
  fraseTexto.replaceChildren();
  lineas.forEach((texto, index) => {
    if (index > 0) {
      fraseTexto.appendChild(document.createElement("br"));
    }
    fraseTexto.appendChild(document.createTextNode(texto));
  });
}

function fraseCompleta() {
  pintarFrase(FRASE_LINEAS);
  fraseCursor.hidden = true;
}

function escribirFrase() {
  window.clearTimeout(typeTimer);

  if (reduceMotion.matches) {
    fraseCompleta();
    return;
  }

  const lineas = [""];
  pintarFrase(lineas);
  fraseCursor.hidden = false;

  let linea = 0;
  let char = 0;

  function tick() {
    if (linea >= FRASE_LINEAS.length) {
      typeTimer = window.setTimeout(() => {
        fraseCursor.hidden = true;
      }, 900);
      return;
    }

    const actual = FRASE_LINEAS[linea];
    if (char < actual.length) {
      lineas[linea] += actual[char];
      char += 1;
      pintarFrase(lineas);
      typeTimer = window.setTimeout(tick, 38);
      return;
    }

    linea += 1;
    char = 0;
    if (linea < FRASE_LINEAS.length) {
      lineas.push("");
    }
    typeTimer = window.setTimeout(tick, 180);
  }

  tick();
}

window.addEventListener("resize", () => {
  iniciarParticulas();
});

reduceMotion.addEventListener("change", () => {
  iniciarParticulas();
  if (reduceMotion.matches) {
    fraseCompleta();
  }
});

iniciarTema();
iniciarParticulas();
escribirFrase();
