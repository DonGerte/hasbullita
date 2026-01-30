from aiogram import types
from app.storage.repository import get_db
from app.core.metrics import log_interaction
from app.core.config import config
from app.core.profiling import get_or_create_profile

async def message_handler(message: types.Message):
    """Handle general messages - the star function."""
    db = next(get_db())

    # Get user
    from app.storage.models import User
    user = db.query(User).filter(User.telegram_id == str(message.from_user.id)).first()
    if not user:
        # Should not happen, but fallback
        await message.reply("¡Hola! Usa /start primero para comenzar. 😊")
        return

    # Determine interaction type
    text_length = len(message.text or "")
    if message.text.startswith("/"):
        interaction_type = "command"
    elif text_length < 50:
        interaction_type = "short_text"
    else:
        interaction_type = "long_text"

    # Log interaction
    log_interaction(
        user_id=user.id,
        interaction_type=interaction_type,
        content_length=text_length,
        is_initiative=1,  # Assuming user messages are initiatives
        db=db
    )

    # Update profile if enabled
    if config.ENABLE_PROFILING:
        from app.core.profiling import update_profile
        update_profile(user.id, db)

    # Generate adaptive response
    profile_type = "explorador"
    if config.ENABLE_PROFILING:
        profile = get_or_create_profile(user.id, db)
        profile_type = profile.profile_type

    # Simple adaptive response
    if profile_type == "explorador":
        response = f"¡Interesante lo que dices, {message.from_user.first_name}! Como eres explorador, te sugiero probar más conversaciones. ¿Qué más te gusta? 🌟"
    elif profile_type == "ocasional":
        response = f"Genial, {message.from_user.first_name}. Tu estilo ocasional me gusta. ¿Quieres profundizar en eso? 😉"
    elif profile_type == "reactivo":
        response = f"Entendido, {message.from_user.first_name}. Directo al grano. ¿Qué sigue? 💪"
    else:  # intensivo
        response = f"¡Wow, {message.from_user.first_name}! Como conversas tanto, vamos a lo profundo: ¿Cómo te hace sentir eso realmente? 🧠"

    await message.reply(response)