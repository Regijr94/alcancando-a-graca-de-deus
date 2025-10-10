#!/bin/bash

# Script para executar a Galeria de Fotos com Música

echo "🎵 Galeria de Fotos com Música 🖼️"
echo "=================================="

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Por favor, instale o Docker primeiro."
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose não está disponível. Tentando instalar..."
    sudo apt install docker-compose-plugin
fi

# Verificar se o diretório pictures existe e tem fotos
if [ ! -d "pictures" ]; then
    echo "📁 Criando diretório 'pictures'..."
    mkdir -p pictures
fi

if [ ! -d "music" ]; then
    echo "📁 Criando diretório 'music'..."
    mkdir -p music
fi

# Contar arquivos
photo_count=$(find pictures -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.gif" -o -iname "*.bmp" -o -iname "*.webp" \) 2>/dev/null | wc -l)
music_count=$(find music -type f \( -iname "*.mp3" -o -iname "*.wav" -o -iname "*.ogg" -o -iname "*.m4a" \) 2>/dev/null | wc -l)

echo "📸 Fotos encontradas: $photo_count"
echo "🎵 Músicas encontradas: $music_count"

if [ $photo_count -eq 0 ]; then
    echo "⚠️  Nenhuma foto encontrada no diretório 'pictures'."
    echo "   Adicione algumas fotos antes de executar a aplicação."
    echo "   Formatos suportados: JPG, PNG, GIF, BMP, WebP"
fi

if [ $music_count -eq 0 ]; then
    echo "⚠️  Nenhuma música encontrada no diretório 'music'."
    echo "   Adicione algumas músicas para ter a experiência completa."
    echo "   Formatos suportados: MP3, WAV, OGG, M4A"
fi

echo ""
echo "🚀 Iniciando a aplicação..."
echo "   A aplicação estará disponível em: http://localhost:8501"
echo "   Pressione Ctrl+C para parar"
echo ""

# Executar com Docker Compose
docker compose up --build
