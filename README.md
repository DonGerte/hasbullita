# Hasbullita MVP

Un bot de Telegram simple para validar retención de usuarios mediante interacciones adaptativas.

## ¿Qué hace Hasbullita?

Hasbullita es un bot de Telegram que responde de manera adaptativa basada en el perfil conductual del usuario. El objetivo es validar si los usuarios regresan después de una interacción inicial.

### Funciones del MVP
- **Onboarding perfecto**: /start registra usuario y explica valor en una frase.
- **Respuesta adaptativa**: Una función estrella que ajusta tono y longitud según perfil.
- **Perfil psicológico v0**: Clasificación ligera ("explorador", "ocasional", "reactivo", "intensivo") sin datos sensibles.
- **Personalización de personalidad**: Comando /mood para cambiar entre divertido, serio, filosófico, normal.
- **Gamificación básica**: /quiz para jugar y ganar puntos, /achievements para ver logros.
- **Funcionalidades útiles**: /inspire para frases motivadoras, /weather para clima, /moon para fases lunares.
- **Entretenimiento**: /news para noticias, /horoscope para horóscopo, /meme para memes.
- **Información completa**: /help y /info para ver todas las funcionalidades.
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
2. Copia `.env.example` a `.env` y configura:
   - `TELEGRAM_BOT_TOKEN` (requerido)
   - `OPENWEATHER_API_KEY` (opcional, para funcionalidad de clima)
   - `NEWSAPI_KEY` (opcional, para noticias)
   - Otras APIs opcionales para futuras funcionalidades
3. Ejecuta `run.bat` (Windows) o `python app/main.py` manualmente
4. Instala dependencias si no están: `pip install -r requirements.txt`

### Cómo obtener las APIs

**APIs Gratuitas (recomendadas para empezar):**
- **OpenWeather**: Regístrate en [openweathermap.org](https://openweathermap.org/api) - 1000 llamadas/día gratis
- **NewsAPI**: Regístrate en [newsapi.org](https://newsapi.org) - 100 llamadas/día gratis

**APIs Opcionales para futuras funcionalidades:**
- **Spotify**: Para música - [developer.spotify.com](https://developer.spotify.com/)
- **YouTube**: Para videos - [console.developers.google.com](https://console.developers.google.com/)
- **Google Calendar**: Para recordatorios - [console.developers.google.com](https://console.developers.google.com/)

**Nota**: Las funcionalidades de horóscopo y memes funcionan sin APIs adicionales.

### Verificar configuración de APIs

Ejecuta `python check_apis.py` para ver qué APIs tienes configuradas y cuáles faltan.

## Ejemplo de Conversación

### Usuario Nuevo (Explorador)
/start
Bot: ¡Hola Juan! 👋 Soy Hasbullita, tu compañero de conversación inteligente. Me adapto a tu estilo para hacer charlas más divertidas. ¿Qué te trae por aquí? Cuéntame algo nuevo y veamos qué pasa. 🚀

Usa /help para ver todos los comandos disponibles.

/help
Bot: 🤖 *Hasbullita - Tu compañero de conversación adaptativo*

*Comandos disponibles:*

📋 *Información y Ayuda:*
/start - Inicia tu experiencia personalizada con el bot
/help - Muestra esta guía completa de comandos
/info - Información general sobre Hasbullita

👤 *Perfil y Estadísticas:*
/profile - Ve tu perfil conductual basado en conversaciones
/stats - Tus estadísticas de conversación (mensajes, temas, etc.)
/suggest - Recibe una sugerencia personalizada basada en tu perfil

🎭 *Personalización:*
/mood - Cambia mi personalidad entre: divertido, serio, filosófico, normal

🎮 *Gamificación:*
/quiz - Juega un quiz interactivo para ganar puntos y mejorar tu perfil
/achievements - Ve tus logros desbloqueados y progreso

🌟 *Funcionalidades Útiles:*
/inspire - Recibe una frase inspiradora para motivarte
/weather [ciudad] - Consulta el clima actual de una ciudad
/moon - Descubre la fase lunar actual y su significado

📰 *Entretenimiento y Actualidad:*
/news - Últimas noticias destacadas
/horoscope [signo] - Tu horóscopo diario
/meme - Un meme aleatorio para reírte

*Cómo funciona Hasbullita:*
- 🤖 Respondo adaptándome a tu estilo de conversación
- 📊 Analizo tus mensajes para crear un perfil conductual único
- 🎯 Cuanto más charlemos, mejor te conoceré y personalizaré respuestas
- 🏆 Gana puntos con quizzes y desbloquea logros
- 🌟 Prueba diferentes tipos de mensajes para ver cómo evoluciona mi personalidad

*Consejos:*
- Usa /mood para cambiar mi actitud según tu estado de ánimo
- Los quizzes te ayudan a ganar puntos y mejorar tu perfil
- Revisa tus /achievements para ver tu progreso

¿Listo para conversar? Solo escribe algo natural. 🚀
- Cuanto más charlemos, mejor te conoceré
- ¡Prueba diferentes tipos de mensajes!

¿Listo para conversar? Solo escribe algo. 🚀

/info
Bot: ℹ️ *Información sobre Hasbullita*

🤖 *¿Qué es Hasbullita?*
Hasbullita es un bot de Telegram inteligente diseñado para conversaciones adaptativas. Se inspira en bots como Akami, aprendiendo de tus interacciones para personalizar respuestas.

📊 *Características principales:*
- Análisis conductual en tiempo real
- Personalización de personalidad (mood)
- Sistema de gamificación con quizzes y logros
- Funcionalidades útiles: frases inspiradoras, clima, fases lunares
- Entretenimiento: noticias, horóscopo, memes aleatorios
- Perfiles únicos basados en conversaciones
- Respuestas adaptativas según tu estilo

🔧 *Detalles técnicos:*
- Versión: MVP 1.0
- Lenguaje: Python 3.10
- Framework: aiogram 3.x
- Base de datos: SQLite
- Creado por: Comunidad de desarrolladores

📈 *Estadísticas del bot:*
- Usuarios activos: Creciendo diariamente
- Conversaciones analizadas: Miles
- Perfiles únicos creados: Continuamente

🌟 *Objetivo:*
Crear una experiencia de conversación única y atractiva que mejore la retención de usuarios mediante personalización inteligente.

Para ver todos los comandos disponibles, usa /help

¡Gracias por usar Hasbullita! 🙏

/profile
Bot: 📊 *Tu Perfil: Explorador*

Eres curioso y exploras nuevas conversaciones. Te sugiero probar temas variados.

Interacciones: 0.5 por día

/stats
Bot: 📈 *Tus Estadísticas*

Total interacciones: 5
Esta semana: 3

¡Sigue conversando para mejorar tus métricas!

/suggest
Bot: 💡 *Sugerencia Personalizada*

🌟 Prueba preguntarme sobre temas que no conozcas. ¿Qué te gustaría explorar hoy?

/mood divertido
Bot: ¡Genial! Ahora soy más divertido. 😄 ¿Listo para reírnos?

/quiz
Bot: 🧠 *Pregunta Rápida*

¿Cuál es la capital de Francia?
1. Londres
2. París
3. Madrid
4. Roma

Responde con el número de la opción correcta.

3
Bot: ¡Correcto! 🎉 Tu puntuación total: 1

/achievements
Bot: 🏆 *Tus Logros*

✅ Primer mensaje enviado
✅ 10 interacciones

¡Sigue así para más!

## Ver Métricas

Las métricas se almacenan en `hasbullita.db`. Para verlas:

```sql
SELECT * FROM metrics;
SELECT profile_type, COUNT(*) FROM user_profiles GROUP BY profile_type;
SELECT COUNT(*) as total_users FROM users;
```

O usa un explorador de SQLite como DB Browser.

## Monitoreo

- Logs en consola durante ejecución.
- Usuarios recurrentes se loggean en start_handler.
- Errores se capturan en middleware.

## Pruebas

Ejecuta `pytest` para validar funcionalidades. Cobertura actual: 71%.

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