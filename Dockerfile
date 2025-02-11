FROM python:3.9-slim-buster

# Instalar dependencias necesarias para psycopg2 y herramientas para Google Cloud SDK
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    libc6-dev \
    curl \
    gnupg

# Añadir el repositorio de Google Cloud SDK
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Actualizar el índice de los paquetes y luego instalar Google Cloud SDK
RUN apt-get update && apt-get install -y google-cloud-sdk

WORKDIR /app

# Copiar y luego instalar las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar pg8000 para trabajar con bases de datos
RUN pip install pg8000

# Instalar Uvicorn para el servidor ASGI
RUN pip install uvicorn

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto 8080 para App Engine
EXPOSE 8080

# Definir el comando de inicio para Gunicorn con UvicornWorker (ASGI)
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", ":8080", "main:app"]
