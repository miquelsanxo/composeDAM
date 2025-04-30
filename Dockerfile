# Usa una imagen base de Python
FROM python:3.9.6

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación
COPY ./app/ .

RUN rm -rf /app/instance
RUN rm -rf /app/.env*
RUN rm -rf /app/.gitignore
RUN rm -rf /app/Dockerfile
RUN rm -rf /app/docker-compose.yml
RUN rm -rf /app/README.md

# Expone el puerto en el que corre Flask
EXPOSE 8000
ENV PORT 8000

# Comando para ejecutar la aplicación con Gunicorn
CMD ["python", "index.py"]