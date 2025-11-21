# Imagem base oficial do Python
FROM python:3.11-slim

# Atualiza o pip e instala o gerenciador uv
RUN pip install --upgrade pip && pip install uv

# Cria diretório de trabalho
WORKDIR /app

# Copia o projeto para o container
COPY . /app

# Instala as dependências usando uv
RUN uv pip install --system -r pyproject.toml

# Comando padrão do container
CMD ["univdoc", "--help"]