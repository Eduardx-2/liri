
### ¿Que es Liri?

Liri es una herramienta Open-source que tiene como finalidad proporcionar información de un número de Télefono. (503)
<a href="https://github.com/Eduardx-2/liri/blob/main/LiriPag/Liri.png"><img alt="https://github.com/Eduardx-2/liri/blob/main/LiriPag/Liri.png" src="https://github.com/Eduardx-2/liri/blob/main/LiriPag/Liri.png"></a>

### ¿Cómo funciona Liri?

- Liri funciona através de realizar busquedas Abiertas(Osint), consulta información de un número téfonico en fuentes:
	- Operadores Télefonicos
	- Redes Sociales
- Liri cuenta actualmente con el soporte de consultas en 3 operadoras:
	- Tigo
	- Claro
	- Movistar
- Redes Sociales:
	- Instagram
	- Facebook
	- Más redes(Próximo)
 
# Requisitos del sistema

- Python 3
- Firefox instalado (lo usa Selenium para el scraping)
- `geckodriver`: no hace falta instalarlo a mano, Selenium Manager lo descarga solo la primera vez.

## Entorno virtual (recomendado)

```bash
cd ~/Documentos/Liri
python3 -m venv .venv
source .venv/bin/activate
```
## Instalar dependencias

```bash
pip install -r liri-back/requirements.txt
pip install -r LiriPag/requirements.txt
```

- `liri-back/requirements.txt`: `flask`, `requests`, `selenium`, `regex`
- `LiriPag/requirements.txt`: `flask`

# Ejecutar

La primera vez, dale permiso de ejecución al script:

```bash
chmod +x start.sh
```
> [!Scraping]
> Tenga en cuenta en realizar uso de una vpn, ya que los servicios de instagram puede tomarlo a usted como un bot.

> # Información:
	- Datos de deudas.
	- Número activo en Redes.(Facebook,Instagram)

Sí quiere saber más sobre como funciona Liri, puede consultar Liri BACKEND.md.
