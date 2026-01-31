from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.storage.models import User
from app.storage.repository import get_db
from app.core.metrics import log_interaction
from app.config import settings as config
from app.core.profiling import update_profile
import logging

logger = logging.getLogger(__name__)


async def start_handler(message: types.Message, state: FSMContext):
    """Handle /start command."""
    db = next(get_db())

    # Register user
    user = db.query(User).filter(User.telegram_id == str(message.from_user.id)).first()
    if not user:
        user = User(
            telegram_id=str(message.from_user.id),
            username=message.from_user.username,
            language_code=message.from_user.language_code,
            chat_type=message.chat.type,
        )
        db.add(user)
        db.commit()
        logger.info(f"New user registered: {user.id}")
    else:
        logger.info(f"Returning user: {user.id}, profile: {user.profile.profile_type if user.profile else 'none'}")

    # Log interaction
    log_interaction(user_id=user.id, interaction_type="command", content_length=0, is_initiative=1, db=db)

    # Update profile if enabled
    if config.enable_profiling:
        update_profile(user.id, db)

    # Personalized welcome based on profile
    profile_type = "explorador"  # Default
    if config.enable_profiling:
        from app.core.profiling import get_or_create_profile

        profile = get_or_create_profile(user.id, db)
        profile_type = profile.profile_type

    # Adapt response
    if profile_type == "explorador":
        response = f"¡Hola {message.from_user.first_name}! 👋 Soy Hasbullita, tu compañero de conversación inteligente. Me adapto a tu estilo para hacer charlas más divertidas. ¿Qué te trae por aquí? Cuéntame algo nuevo y veamos qué pasa. 🚀"
    elif profile_type == "ocasional":
        response = f"¡Ey {message.from_user.first_name}! 😊 Hasbullita aquí. Basado en tu estilo, te recomiendo conversaciones equilibradas. ¿Qué tal si me cuentas sobre tu día?"
    elif profile_type == "reactivo":
        response = f"Hola {message.from_user.first_name}. 💬 Soy Hasbullita. Veo que prefieres respuestas directas. ¿Qué necesitas? Vamos al grano."
    else:  # intensivo
        response = f"¡Hola de nuevo {message.from_user.first_name}! 🤔 Hasbullita listo. Como conversas mucho, vamos a profundizar: ¿Cuál es tu mayor motivación hoy?"

    # Create inline keyboard with main functions
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎭 Cambiar Mood", callback_data="mood"),
            InlineKeyboardButton(text="🧠 Hacer Quiz", callback_data="quiz")
        ],
        [
            InlineKeyboardButton(text="🏆 Ver Logros", callback_data="achievements"),
            InlineKeyboardButton(text="📊 Mi Perfil", callback_data="profile")
        ],
        [
            InlineKeyboardButton(text="💭 Inspiración", callback_data="inspire"),
            InlineKeyboardButton(text="🌤️ Clima", callback_data="weather")
        ],
        [
            InlineKeyboardButton(text="🌙 Fase Lunar", callback_data="moon"),
            InlineKeyboardButton(text="📰 Noticias", callback_data="news")
        ],
        [
            InlineKeyboardButton(text="🔮 Horóscopo", callback_data="horoscope"),
            InlineKeyboardButton(text="😂 Meme", callback_data="meme")
        ],
        [
            InlineKeyboardButton(text="ℹ️ Info del Bot", callback_data="info"),
            InlineKeyboardButton(text="❓ Ayuda", callback_data="help")
        ]
    ])

    await message.reply(response, reply_markup=keyboard)
