FROM python:3.11-slim

WORKDIR /app

# Copia requirements ANTES do código (aproveita cache Docker se código mudar)
COPY requirements.txt .

# Instala dependências sem cache local (reduz tamanho da imagem)
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da API
COPY api.py .

# Copia o modelo treinado
COPY modelo/ modelo/

# Expõe a porta 8000 (informativo - não ativa a porta)
EXPOSE 8000

# Comando para iniciar o servidor
# --host 0.0.0.0 é obrigatório: dentro de um container, localhost só seria acessível de dentro
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
