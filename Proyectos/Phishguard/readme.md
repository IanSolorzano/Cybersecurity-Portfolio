# PhishGuard – URL Phishing Detection Tool

PhishGuard es una herramienta desarrollada en Python para la detección de posibles ataques de phishing mediante el análisis de URLs.

---

## Funcionamiento

1. **Ingreso y validación de URLs**  
   El usuario ingresa una o varias URLs, las cuales se validan contra el estándar [RFC 3986](https://datatracker.ietf.org/doc/html/rfc3986) para garantizar que tengan un formato correcto.

2. **Normalización**  
   Cada URL es normalizada para facilitar un análisis consistente, limpiando parámetros y ajustando a un formato estándar.

3. **Análisis local**  
   - Se extrae el dominio y sus subdominios para identificar características sospechosas.  
   - Se detectan caracteres especiales inusuales.  
   - Se verifica si se usa una dirección IP en lugar de un nombre de dominio.  
   - Se buscan patrones típicos de phishing, como términos relacionados con acceso o verificación (por ejemplo, "login", "verify").  
   - Se comprueba si el sitio utiliza HTTPS con certificado SSL válido.

4. **Análisis externo (opcional)**  
   Si se configuran las claves API en un archivo `.env`, PhishGuard puede consultar servicios externos para enriquecer el análisis. Actualmente se integran:

   | Servicio           | Funcionalidad                                  |
   |--------------------|-----------------------------------------------|
   | VirusTotal         | Escaneo de URL con múltiples motores antivirus|
   | Google Safe Browsing| Verificación contra listas de URLs maliciosas |
   | Shodan (opcional)  | Información de servicios y puertos expuestos  |

5. **Reporte final**  
   Los resultados combinan el análisis local y la información externa, generando un puntaje de riesgo categorizado en: **bajo**, **medio** o **alto**.  
   El reporte puede visualizarse en la terminal o exportarse en formatos JSON o CSV para análisis posteriores.

---

## Tecnologías principales

- Python 3.x  
- `requests` (comunicación con APIs externas)  
- `urllib` y expresiones regulares (procesamiento y validación de URLs)  
- `python-dotenv` (gestión segura de claves API)  

---

## Consideraciones de seguridad

- Las claves API se almacenan localmente en un archivo `.env`, que está incluido en `.gitignore` para evitar exposición accidental.  
- Las consultas a servicios externos solo se realizan si el usuario lo habilita explícitamente.

---

## Próximas mejoras

- Incorporar técnicas de machine learning para mejorar la clasificación.  
- Añadir soporte para más fuentes de reputación.  
- Soportar análisis masivo a partir de archivos de entrada.
