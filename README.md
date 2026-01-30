# Hasbullita MVP

Un bot de Telegram simple para validar retención de usuarios mediante interacciones adaptativas.

## ¿Qué hace Hasbullita?

Hasbullita es un bot de Telegram que responde de manera adaptativa basada en el perfil conductual del usuario. El objetivo es validar si los usuarios regresan después de una interacción inicial.

### Funciones del MVP
- **Onboarding perfecto**: /start registra usuario y explica valor en una frase.
- **Respuesta adaptativa**: Una función estrella que ajusta tono y longitud según perfil.
- **Perfil psicológico v0**: Clasificación ligera ("explorador", "ocasional", "reactivo", "intensivo") sin datos sensibles.
- **Métricas básicas**: Logging de usuarios, sesiones, retención día 1/7.
- **Feature flags**: Activar/desactivar perfil y logging extendido.

## ¿Qué NO hace?
- Panel web
- IA avanzada
- NLP complejo
- Gamificación
- Monetización
- Más de una función estrella

## Cómo correr

1. Clona el repo
2. Copia `.env.example` a `.env` y configura `TELEGRAM_BOT_TOKEN`
3. Ejecuta `run.bat` (Windows) o `python app/main.py` manualmente
4. Instala dependencias si no están: `pip install -r requirements.txt`

## Métricas que mide

- Usuarios únicos
- Sesiones totales
- Interacciones totales
- Retención día 1 y día 7
- Errores

## TODO para expansiones futuras

- Implementar cálculo real de retención
- Agregar más perfiles
- Integrar con dashboards simples
- Soporte multi-idioma
- Optimizaciones de performance

## Estructura del Proyecto

- `app/`: Código del backend FastAPI.
- `bots/`: Implementaciones de los bots de Telegram.
- `docker/`: Configuración de Docker y docker-compose.