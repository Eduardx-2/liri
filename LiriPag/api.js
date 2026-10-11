/**
 * Cliente API LIRI.
 * POST http://127.0.0.1:9081/api/consulta/number
 * Body: {"numero": "<valor del input>"}
 * La consulta real tarda entre 40 y 50 segundos.
 */
(function (global) {
  const API_URL = "http://127.0.0.1:9081/api/consulta/number";
  const TIMEOUT_MS = 120000;

  const RED_LABELS = {
    tiktok: "TikTok",
    instagram: "Instagram",
    facebook: "Facebook",
    wallet: "Wallet",
    falis: "Falis",
  };

  function soloDigitos(numero) {
    return String(numero ?? "").replace(/\D/g, "");
  }

  /**
   * El endpoint exige 8 dígitos. Se conserva el texto del input y solo se
   * quitan separadores o el prefijo 503 cuando el usuario lo escribió.
   */
  function numeroConsulta(numero) {
    const digits = soloDigitos(numero);
    if (digits.length === 11 && digits.startsWith("503")) return digits.slice(3);
    if (digits.length === 13 && digits.startsWith("00503")) return digits.slice(5);
    return digits || String(numero ?? "").trim();
  }

  function redRegistrada(info) {
    if (info && typeof info === "object") return info.estado === true;
    return String(info).toLowerCase() === "registered";
  }

  function nombreRed(clave, info) {
    if (info && typeof info === "object" && info.mensaje) return String(info.mensaje);
    return RED_LABELS[String(clave).toLowerCase()] || clave;
  }

  function redesRegistradas(dataNumRedes) {
    if (!dataNumRedes || typeof dataNumRedes !== "object") return [];
    return Object.entries(dataNumRedes)
      .filter(([, info]) => redRegistrada(info))
      .map(([clave, info]) => nombreRed(clave, info));
  }

  function nombreCompania(data) {
    if (!data || typeof data !== "object") return "";
    const nombre = data.compania ?? data.compañia;
    return nombre != null ? String(nombre).trim() : "";
  }

  function mapearDeudas(data) {
    if (!data || typeof data !== "object") return [];
    const monto = data.monto != null ? String(data.monto) : "";
    const fecha = data.fecha != null ? String(data.fecha) : "";
    const idFactura = data.docFactura != null ? String(data.docFactura) : "";
    if (!monto && !fecha && !idFactura) return [];
    return [{ monto, fecha, idFactura }];
  }

  function mensajeError(data, httpOk) {
    if (data && typeof data === "object") {
      const msg = data.errorNumero || data.error || data.errorLong || data.mensaje;
      if (msg) return String(msg);
    }
    return httpOk ? null : "Error de servidor";
  }

  function normalizar(data, httpOk = true) {
    const errorMsg = mensajeError(data, httpOk);
    const compania = nombreCompania(data);
    const deudas = mapearDeudas(data);
    const redes =
      data && data.dataNumRedes ? redesRegistradas(data.dataNumRedes) : [];

    if (errorMsg && !compania && !redes.length && !deudas.length) {
      return { ok: false, error: errorMsg, raw: data };
    }

    return {
      ok: true,
      error: errorMsg || undefined,
      telefono: data && data.numero,
      compania,
      deudas,
      redes,
      raw: data,
    };
  }

  async function consultarNumero(numero) {
    const valor = numeroConsulta(numero);
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({ numero: valor }),
        signal: controller.signal,
      });

      let data;
      try {
        data = await res.json();
      } catch {
        return { ok: false, error: "Respuesta inválida del servidor." };
      }

      return normalizar(data, res.ok);
    } catch (err) {
      if (err && err.name === "AbortError") {
        return {
          ok: false,
          error: "La consulta tardó demasiado. Intenta de nuevo.",
        };
      }
      throw err;
    } finally {
      clearTimeout(timer);
    }
  }

  global.LiriApi = {
    consultarNumero,
    numeroConsulta,
    API_URL,
    TIMEOUT_MS,
  };
})(typeof window !== "undefined" ? window : globalThis);
