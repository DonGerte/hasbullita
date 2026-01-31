from aiogram import types
from aiogram.fsm.context import FSMContext
from app.storage.models import User
from app.storage.repository import get_db
from app.core.metrics import log_interaction
from app.config import settings as config
from app.core.profiling import update_profile, get_or_create_profile
import logging
import json

logger = logging.getLogger(__name__)


async def help_handler(message: types.Message):
    """Handle /help command."""
    help_text = """
🤖 *Hasbullita - Tu compañero de conversación adaptativo*

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
    """
    await message.reply(help_text, parse_mode="Markdown")


async def info_handler(message: types.Message):
    """Handle /info command."""
    info_text = """
ℹ️ *Información sobre Hasbullita*

🤖 *¿Qué es Hasbullita?*
Hasbullita es un bot de Telegram inteligente diseñado para conversaciones adaptativas. Se inspira en bots como Akami, aprendiendo de tus interacciones para personalizar respuestas.

📊 *Características principales:*
- Análisis conductual en tiempo real
- Personalización de personalidad (mood)
- Sistema de gamificación con quizzes y logros
- Perfiles únicos basados en conversaciones
- Respuestas adaptativas según tu estilo

🔧 *Detalles técnicos:*
- Versión: MVP 1.0
- Lenguaje: Python 3.10
- Framework: aiogram 3.x
- Base de datos: SQLite
- Creado por: Hasbulla (@hasbulladox)

📈 *Estadísticas del bot:*
- Usuarios activos: Creciendo diariamente
- Conversaciones analizadas: Miles
- Perfiles únicos creados: Continuamente

🌟 *Objetivo:*
Crear una experiencia de conversación única y atractiva que mejore la retención de usuarios mediante personalización inteligente.

Para ver todos los comandos disponibles, usa /help

¡Gracias por usar Hasbullita! 🙏
    """
    await message.reply(info_text, parse_mode="Markdown")


async def callback_handler(callback: types.CallbackQuery):
    """Handle inline keyboard callbacks."""
    data = callback.data

    if data == "help":
        await help_handler(callback.message)
    elif data == "info":
        await info_handler(callback.message)
    elif data == "mood":
        await mood_handler(callback.message)
    elif data == "quiz":
        await quiz_handler(callback.message)
    elif data == "achievements":
        await achievements_handler(callback.message)
    elif data == "profile":
        await profile_handler(callback.message)
    elif data == "inspire":
        await inspire_handler(callback.message)
    elif data == "weather":
        await callback.message.reply("🌤️ Para consultar el clima, usa: /weather [ciudad]\n\nEjemplo: /weather Madrid")
    elif data == "moon":
        await moon_handler(callback.message)
    elif data == "news":
        await news_handler(callback.message)
    elif data == "horoscope":
        await callback.message.reply("🔮 Para ver tu horóscopo, usa: /horoscope [signo]\n\nEjemplo: /horoscope leo\n\nUsa /horoscope solo para ver la lista de signos.", parse_mode="Markdown")
    elif data == "meme":
        await meme_handler(callback.message)

    await callback.answer()


async def profile_handler(message: types.Message):
    """Handle /profile command."""
    db = next(get_db())
    user = db.query(User).filter(User.telegram_id == str(message.from_user.id)).first()
    if not user:
        await message.reply("Primero usa /start para registrarte. 😊")
        return

    profile = get_or_create_profile(user.id, db)
    profile_descriptions = {
        "explorador": "Eres curioso y exploras nuevas conversaciones. Te sugiero probar temas variados.",
        "ocasional": "Conversas de forma equilibrada. ¡Sigue así!",
        "reactivo": "Prefieres respuestas directas y rápidas. Vamos al grano.",
        "intensivo": "Te encanta profundizar en las charlas. ¡Hablemos de cosas profundas!"
    }

    response = f"📊 *Tu Perfil: {profile.profile_type.title()}*\n\n{profile_descriptions.get(profile.profile_type, 'Perfil en desarrollo...')}\n\nInteracciones: {profile.usage_frequency:.1f} por día"
    await message.reply(response, parse_mode="Markdown")


async def stats_handler(message: types.Message):
    """Handle /stats command."""
    db = next(get_db())
    user = db.query(User).filter(User.telegram_id == str(message.from_user.id)).first()
    if not user:
        await message.reply("Primero usa /start para registrarte. 😊")
        return

    from app.storage.models import Interaction
    from datetime import datetime, timedelta

    # Get user's interaction count
    interactions = db.query(Interaction).filter(Interaction.user_id == user.id).all()
    total_interactions = len(interactions)
    recent = [i for i in interactions if i.timestamp > datetime.utcnow() - timedelta(days=7)]
    weekly_interactions = len(recent)

    response = f"📈 *Tus Estadísticas*\n\nTotal interacciones: {total_interactions}\nEsta semana: {weekly_interactions}\n\n¡Sigue conversando para mejorar tus métricas!"
    await message.reply(response, parse_mode="Markdown")


async def suggest_handler(message: types.Message):
    """Handle /suggest command - innovative suggestion based on profile."""
    db = next(get_db())
    user = db.query(User).filter(User.telegram_id == str(message.from_user.id)).first()
    if not user:
        await message.reply("Primero usa /start para registrarte. 😊")
        return

    profile = get_or_create_profile(user.id, db)
    suggestions = {
        "explorador": "🌟 Prueba preguntarme sobre temas que no conozcas. ¿Qué te gustaría explorar hoy?",
        "ocasional": "💬 ¿Qué tal una conversación ligera sobre tu día? ¡Cuéntame!",
        "reactivo": "⚡ Vamos directo: ¿Cuál es tu opinión sobre algo actual?",
        "intensivo": "🧠 Profundicemos: ¿Qué filosofía o idea te ha impactado últimamente?"
    }

    response = f"💡 *Sugerencia Personalizada*\n\n{suggestions.get(profile.profile_type, '¡Escribe algo y veamos qué pasa!')}"
    await message.reply(response, parse_mode="Markdown")


async def mood_handler(message: types.Message):
    """Handle /mood command - change bot personality."""
    db = next(get_db())
    user = db.query(User).filter(User.telegram_id == str(message.from_user.id)).first()
    if not user:
        await message.reply("Primero usa /start para registrarte. 😊")
        return

    # Parse mood from command
    parts = message.text.split()
    if len(parts) < 2:
        await message.reply("Uso: /mood [divertido|serio|filosofico|normal]\n\nEjemplo: /mood divertido")
        return

    new_mood = parts[1].lower()
    valid_moods = ["divertido", "serio", "filosofico", "normal"]
    if new_mood not in valid_moods:
        await message.reply(f"Mood inválido. Opciones: {', '.join(valid_moods)}")
        return

    profile = get_or_create_profile(user.id, db)
    profile.mood = new_mood
    db.commit()

    mood_responses = {
        "divertido": "¡Genial! Ahora soy más divertido. 😄 ¿Listo para reírnos?",
        "serio": "Entendido. Modo serio activado. 💼 ¿Qué tema serio quieres discutir?",
        "filosofico": "Excelente. Vamos a lo profundo. 🧘 ¿Qué preguntas existenciales te rondan?",
        "normal": "Volviendo a lo normal. 🤖 ¿Qué te cuentas?"
    }

    await message.reply(mood_responses[new_mood])


async def quiz_handler(message: types.Message):
    """Handle /quiz command - quick quiz for engagement."""
    db = next(get_db())
    user = db.query(User).filter(User.telegram_id == str(message.from_user.id)).first()
    if not user:
        await message.reply("Primero usa /start para registrarte. 😊")
        return

    profile = get_or_create_profile(user.id, db)

    # Simple quiz questions
    questions = [
        {"q": "¿Cuál es la capital de Francia?", "a": "paris", "options": ["Londres", "París", "Madrid", "Roma"]},
        {"q": "¿Cuántos planetas hay en el sistema solar?", "a": "8", "options": ["7", "8", "9", "10"]},
        {"q": "¿Qué lenguaje se usa para este bot?", "a": "python", "options": ["Java", "Python", "C++", "JavaScript"]},
    ]

    import random
    question = random.choice(questions)

    # Store current quiz in profile (simple way)
    profile.quiz_current = f"{question['q']}|{question['a']}"
    db.commit()

    options_text = "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(question["options"]))
    await message.reply(f"🧠 *Pregunta Rápida*\n\n{question['q']}\n\n{options_text}\n\nResponde con el número de la opción correcta.")


async def achievements_handler(message: types.Message):
    """Handle /achievements command - show unlocked achievements."""
    db = next(get_db())
    user = db.query(User).filter(User.telegram_id == str(message.from_user.id)).first()
    if not user:
        await message.reply("Primero usa /start para registrarte. 😊")
        return

    profile = get_or_create_profile(user.id, db)
    achievements = json.loads(profile.achievements) if profile.achievements else []

    achievement_descriptions = {
        "first_message": "🎉 Primer mensaje enviado",
        "quiz_master": "🧠 5 respuestas correctas en quiz",
        "conversationalist": "💬 10 interacciones",
        "mood_changer": "🎭 Cambió el mood del bot",
    }

    if not achievements:
        response = "🏆 *Logros*\n\nAún no has desbloqueado logros. ¡Sigue conversando y jugando para ganar algunos!"
    else:
        list_ach = "\n".join(f"✅ {achievement_descriptions.get(a, a)}" for a in achievements)
        response = f"🏆 *Tus Logros*\n\n{list_ach}\n\n¡Sigue así para más!"

    await message.reply(response, parse_mode="Markdown")


async def inspire_handler(message: types.Message):
    """Handle /inspire command - Send inspirational quotes."""
    import random

    inspirational_quotes = [
        "🌟 La única forma de hacer un gran trabajo es amar lo que haces. - Steve Jobs",
        "💪 El éxito no es final, el fracaso no es fatal: es el coraje para continuar lo que cuenta. - Winston Churchill",
        "🚀 Tu tiempo es limitado, así que no lo desperdicies viviendo la vida de alguien más. - Steve Jobs",
        "🌈 La vida es lo que sucede mientras estás ocupado haciendo otros planes. - John Lennon",
        "🔥 No cuentes los días, haz que los días cuenten. - Muhammad Ali",
        "💡 La creatividad es la inteligencia divirtiéndose. - Albert Einstein",
        "🌱 Lo que no te mata, te hace más fuerte. - Friedrich Nietzsche",
        "🎯 El futuro pertenece a quienes creen en la belleza de sus sueños. - Eleanor Roosevelt",
        "⚡ La diferencia entre lo ordinario y lo extraordinario es ese pequeño extra. - Jimmy Johnson",
        "🌞 Mantén tu rostro siempre hacia el sol y las sombras caerán detrás de ti. - Walt Whitman",
        "💎 No se trata de ser el mejor, se trata de ser mejor que ayer. - Anónimo",
        "🎨 La vida comienza al final de tu zona de confort. - Neale Donald Walsch",
        "🔮 El único límite para nuestros logros de mañana serán nuestras dudas de hoy. - Franklin D. Roosevelt",
        "🌟 Sé el cambio que quieres ver en el mundo. - Mahatma Gandhi",
        "💫 La felicidad no es algo hecho. Viene de tus propias acciones. - Dalai Lama"
    ]

    quote = random.choice(inspirational_quotes)
    await message.reply(f"💭 *Frase Inspiradora*\n\n{quote}", parse_mode="Markdown")


async def weather_handler(message: types.Message):
    """Handle /weather command - Get weather information."""
    parts = message.text.split()
    if len(parts) < 2:
        await message.reply("Uso: /weather [ciudad]\n\nEjemplo: /weather Madrid")
        return

    city = " ".join(parts[1:])
    api_key = config.openweather_api_key

    try:
        import requests
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=es"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            weather_response = f"🌤️ *Clima en {city.title()}*\n\n" \
                             f"🌡️ Temperatura: {temp}°C\n" \
                             f"☁️ Condición: {description.title()}\n" \
                             f"💧 Humedad: {humidity}%\n" \
                             f"💨 Viento: {wind_speed} m/s"
        else:
            weather_response = f"❌ No pude encontrar información del clima para '{city}'. Verifica el nombre de la ciudad."

    except Exception as e:
        logger.error(f"Error getting weather: {e}")
        weather_response = "❌ Error al obtener información del clima. Inténtalo más tarde."

    await message.reply(weather_response, parse_mode="Markdown")


async def moon_handler(message: types.Message):
    """Handle /moon command - Get current moon phase."""
    from datetime import datetime
    import math

    def get_moon_phase(date):
        """Calculate moon phase (0-7, where 0=new, 4=full)"""
        # Simplified calculation
        year = date.year
        month = date.month
        day = date.day

        if month < 3:
            year -= 1
            month += 12

        a = year // 100
        b = a // 4
        c = 2 - a + b
        e = 365.25 * (year + 4716)
        f = 30.6001 * (month + 1)
        jd = c + day + e + f - 1524.5

        # Moon phase calculation
        moon_age = (jd - 2451550.1) / 29.530588853
        moon_age = moon_age - int(moon_age)
        if moon_age < 0:
            moon_age += 1

        phase = moon_age * 8
        phase = math.floor(phase + 0.5) % 8

        return phase

    today = datetime.now()
    phase = get_moon_phase(today)

    moon_phases = {
        0: ("🌑 Luna Nueva", "Un nuevo comienzo, tiempo de plantar semillas y establecer intenciones."),
        1: ("🌒 Luna Creciente", "Tiempo de crecimiento, acción y manifestación de deseos."),
        2: ("🌓 Cuarto Creciente", "Equilibrio entre luz y oscuridad, tiempo de decisiones importantes."),
        3: ("🌔 Gibosa Creciente", "Energía creciente, buena para proyectos creativos y sociales."),
        4: ("🌕 Luna Llena", "Culminación, plenitud, tiempo de celebración y liberación."),
        5: ("🌖 Gibosa Menguante", "Liberación gradual, tiempo de agradecer y soltar lo que ya no sirve."),
        6: ("🌗 Cuarto Menguante", "Reflexión y evaluación, tiempo de descanso y planificación."),
        7: ("🌘 Luna Menguante", "Renovación interna, tiempo de limpieza y preparación para lo nuevo.")
    }

    phase_name, description = moon_phases.get(phase, ("🌙 Fase Lunar", "Información no disponible"))

    moon_response = f"{phase_name}\n\n{description}\n\n*Fecha: {today.strftime('%d/%m/%Y')}*"

    await message.reply(moon_response, parse_mode="Markdown")


async def news_handler(message: types.Message):
    """Handle /news command - Get latest news headlines."""
    try:
        import requests
        import random

        # Using NewsAPI - free tier allows 100 requests/day
        api_key = config.newsapi_key or "demo"  # Fallback for demo
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}&pageSize=5"

        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code == 200 and data.get('articles'):
            articles = data['articles'][:3]  # Show top 3
            news_text = "📰 *Últimas Noticias*\n\n"

            for i, article in enumerate(articles, 1):
                title = article.get('title', 'Sin título')
                source = article.get('source', {}).get('name', 'Desconocido')
                news_text += f"{i}. *{title}*\n   📺 {source}\n\n"

            news_text += "_Usa /news [tema] para buscar noticias específicas_"
        else:
            news_text = "❌ No pude obtener noticias en este momento. Inténtalo más tarde."

    except Exception as e:
        logger.error(f"Error getting news: {e}")
        news_text = "❌ Error al obtener noticias. Verifica la configuración de la API."

    await message.reply(news_text, parse_mode="Markdown")


async def horoscope_handler(message: types.Message):
    """Handle /horoscope command - Get daily horoscope."""
    parts = message.text.split()
    if len(parts) < 2:
        signs_text = "🔮 *Horóscopo Diario*\n\nElige tu signo zodiacal:\n\n"
        signs_text += "♈ Aries ♉ Tauro ♊ Géminis ♋ Cáncer\n"
        signs_text += "♌ Leo ♍ Virgo ♎ Libra ♏ Escorpio\n"
        signs_text += "♐ Sagitario ♑ Capricornio ♒ Acuario ♓ Piscis\n\n"
        signs_text += "Uso: /horoscope [signo]\nEjemplo: /horoscope leo"
        await message.reply(signs_text, parse_mode="Markdown")
        return

    sign = parts[1].lower()
    zodiac_mapping = {
        'aries': 'aries', 'tauro': 'taurus', 'geminis': 'gemini', 'cancer': 'cancer',
        'leo': 'leo', 'virgo': 'virgo', 'libra': 'libra', 'escorpio': 'scorpio',
        'sagitario': 'sagittarius', 'capricornio': 'capricorn', 'acuario': 'aquarius', 'piscis': 'pisces'
    }

    if sign not in zodiac_mapping:
        await message.reply("❌ Signo no válido. Usa /horoscope para ver la lista de signos.", parse_mode="Markdown")
        return

    try:
        import requests
        # Using Aztro API for horoscopes (free)
        url = f"https://aztro.sameerkumar.website/?sign={zodiac_mapping[sign]}&day=today"
        response = requests.post(url, timeout=10)
        data = response.json()

        if response.status_code == 200:
            horoscope_text = f"🔮 *Horóscopo de {sign.title()}*\n\n"
            horoscope_text += f"📅 *Fecha:* {data.get('current_date', 'Hoy')}\n"
            horoscope_text += f"🎭 *Compatibilidad:* {data.get('compatibility', 'N/A')}\n"
            horoscope_text += f"💕 *Amor:* {data.get('description', 'Sin descripción')}\n\n"
            horoscope_text += f"💡 *Consejo:* {data.get('lucky_time', 'Sigue tu intuición')}\n"
            horoscope_text += f"🎲 *Número de la suerte:* {data.get('lucky_number', '?')}"
        else:
            horoscope_text = "❌ No pude obtener el horóscopo en este momento."

    except Exception as e:
        logger.error(f"Error getting horoscope: {e}")
        horoscope_text = "❌ Error al obtener el horóscopo. Inténtalo más tarde."

    await message.reply(horoscope_text, parse_mode="Markdown")


async def meme_handler(message: types.Message):
    """Handle /meme command - Get a random meme."""
    try:
        import requests
        import random

        # Using Reddit API for memes (no auth required for basic access)
        subreddits = ['memes', 'dankmemes', 'ProgrammerHumor', 'wholesomememes']
        subreddit = random.choice(subreddits)

        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
        headers = {'User-Agent': 'HasbullitaBot/1.0'}

        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        if response.status_code == 200 and data.get('data', {}).get('children'):
            posts = [post['data'] for post in data['data']['children']
                    if not post['data'].get('stickied', False) and
                    post['data'].get('url', '').endswith(('.jpg', '.png', '.gif', '.jpeg'))]

            if posts:
                post = random.choice(posts)
                title = post.get('title', 'Meme sin título')
                image_url = post.get('url', '')
                subreddit_name = post.get('subreddit', subreddit)

                meme_text = f"😂 *Meme de r/{subreddit_name}*\n\n*{title}*\n\n{image_url}"
            else:
                meme_text = "😅 No encontré memes con imágenes en este momento. ¡Inténtalo de nuevo!"
        else:
            meme_text = "❌ No pude obtener memes en este momento."

    except Exception as e:
        logger.error(f"Error getting meme: {e}")
        meme_text = "❌ Error al obtener meme. Verifica la conexión a internet."

    await message.reply(meme_text, parse_mode="Markdown")