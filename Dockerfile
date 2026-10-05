FROM python:3.12-slim

# Instalar ffmpeg con soporte de libass y fuentes del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libass-dev \
    fonts-dejavu-core \
    fonts-freefont-ttf \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . .

# Crear directorios necesarios
RUN mkdir -p assets/images outputs static

# Variables de entorno por defecto
ENV HOST=0.0.0.0
ENV PORT=8050
ENV PYTHONUNBUFFERED=1

EXPOSE 8050

# Comando de arranque del servidor
CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port ${PORT:-8050}"]
