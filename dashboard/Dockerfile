FROM python:3.11-alpine

WORKDIR /app

COPY index.html style.css app.js server.py ./

EXPOSE 8000

ENV PORT=8000

CMD ["python", "server.py"]
