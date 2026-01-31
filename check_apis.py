#!/usr/bin/env python3
"""
Script para verificar la configuración de APIs de Hasbullita
Ejecuta: python check_apis.py
"""

from app.config import settings

def check_api_status():
    """Verifica qué APIs están configuradas"""
    print("🔍 Verificación de APIs de Hasbullita")
    print("=" * 40)

    apis = {
        "OpenWeather (Clima)": settings.openweather_api_key,
        "NewsAPI (Noticias)": settings.newsapi_key,
        "Spotify Client ID": settings.spotify_client_id,
        "Spotify Client Secret": settings.spotify_client_secret,
        "YouTube API": settings.youtube_api_key,
        "Google Calendar": settings.google_calendar_api_key,
    }

    configured = 0
    total = len(apis)

    for name, value in apis.items():
        status = "✅ Configurada" if value else "❌ No configurada"
        print(f"{name}: {status}")
        if value:
            configured += 1

    print("=" * 40)
    print(f"📊 APIs configuradas: {configured}/{total}")

    if configured == 0:
        print("⚠️  Ninguna API configurada. Solo funcionarán comandos básicos.")
    elif configured < total:
        print("ℹ️  Algunas APIs están configuradas. Funcionalidades limitadas.")
    else:
        print("🎉 Todas las APIs configuradas. Funcionalidades completas!")

    print("\n💡 Para configurar APIs, edita el archivo .env en la raíz del proyecto")

if __name__ == "__main__":
    check_api_status()