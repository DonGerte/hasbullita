from aiogram import types
from aiogram.dispatcher import FSMContext
from app.storage.models import User
from app.storage.repository import get_db
from app.core.metrics import log_interaction
from app.core.config import config
from app.core.profiling import update_profile

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
            chat_type=message.chat.type
        )
        db.add(user)
        db.commit()

    # Log interaction
    log_interaction(
        user_id=user.id,
        interaction_type="command",
        content_length=0,
        is_initiative=1,
        db=db
    )

    # Update profile if enabled
    if config.ENABLE_PROFILING:
        update_profile(user.id, db)

    # Personalized welcome based on profile
    profile_type = "explorador"  # Default
    if config.ENABLE_PROFILING:
        from app.core.profiling import get_or_create_profile
        profile = get_or_create_profile(user.id, db)
        profile_type = profile.profile_type

    # Adapt response
    if profile_type == "explorador":
        response = f"¡Hola {message.from_user.first_name}! Soy Hasbullita, tu compañero de conversación inteligente. ¿Qué te trae por aquí? Cuéntame algo y te doy una respuesta adaptada. 🚀"
    elif profile_type == "ocasional":
        response = f"¡Ey {message.from_user.first_name}! Hasbullita aquí. Basado en tu estilo, te recomiendo probar una conversación corta. ¿Qué opinas del día? 😊"
    elif profile_type == "reactivo":
        response = f"Hola {message.from_user.first_name}. Soy Hasbullita. Veo que prefieres respuestas directas. ¿Qué necesitas? 💬"
    else:  # intensivo
        response = f"¡Hola de nuevo {message.from_user.first_name}! Hasbullita listo. Como conversas mucho, te sugiero algo profundo: ¿Cuál es tu mayor motivación hoy? 🤔"

    await message.reply(response)