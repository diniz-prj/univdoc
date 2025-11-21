# UnivDoc

Ferramenta universal para geração automática de documentação baseada em docstrings de código-fonte.

## Principais funcionalidades

- Suporte inicial para linguagens Python e PHP.
- CLI fácil de usar.
- Geração de documentação em Markdown usando templates Jinja2.
- Estrutura modular e extensível para múltiplas linguagens.


## Estrutura do Projeto

```text
univdoc/
├── univdoc/
│   ├── __init__.py
│   ├── main.py             # Ponto de entrada do CLI
│   ├── parser.py           # Lógica de parsing (chama cada linguagem)
│   ├── python_parser.py    # Parsing específico para Python
│   ├── php_parser.py       # Parsing específico para PHP
│   ├── renderer.py         # Gera Markdown a partir de dados
│   ├── utils.py            # Funções auxiliares (p.ex, busca arquivos)
│   └── templates/
│       └── default.md.jinja
├── tests/
│   └── test_basic.py
├── Dockerfile
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

main.py: Faz o parsing dos argumentos do usuário (--source, --lang, --output) e orquestra a chamada das funções.
parser.py: Função central que chama o parser correto conforme linguagem detectada ou fornecida.
python_parser.py / php_parser.py: Funções para extrair docstrings/comentários dessas linguagens.
renderer.py: Recebe os dados extraídos e renderiza via Jinja2.
templates/default.md.jinja: Template Markdown base configurável.
tests/: Testes automatizados.
Dockerfile: Containerização.
README.md: Documentação clara de uso, instalação e contribuição.

## Instalação rápida

Você precisa ter o [uv](https://github.com/astral-sh/uv) instalado.  
Para instalar as dependências do projeto com uv, execute:

```bash
uv pip install -r pyproject.toml
```

## Uso

```bash
uv pip install -r pyproject.toml  # Instala dependências localmente

# Gera documentação para todas as linguagens suportadas automaticamente, saída padrão
univdoc --source ./meu_codigo

# Gera documentação apenas para as linguagens informadas e salva no diretório especificado
univdoc --source ./meu_codigo --lang python,php --output ./docs

# Gerando documentação com template simples padrão
univdoc --source ./meu_codigo --template simple

# Gerando documentação com template elegante padrão
univdoc --source ./meu_codigo --template elegant

# Gerando documentação com um template jinja personalizado
univdoc --source ./meu_codigo --template ./caminho/meu_template.md.jinja

```

A documentação será gerada para os arquivos Python e/ou PHP no diretório de código especificado e salva no diretório de saída informado.

## Uso com Docker

Você pode executar o UnivDoc facilmente via Docker sem precisar instalar dependências em sua máquina local.

### Passos

1. **Construa a imagem Docker:**

    ```bash
    docker build -t univdoc .
    ```

2. **Execute o UnivDoc via Docker:**

    ```bash
    docker run --rm -v $(pwd)/meu_codigo:/app/meu_codigo -v $(pwd)/docs:/app/docs univdoc --source /app/meu_codigo --lang python,php --output /app/docs
    ```

    - O parâmetro `-v` mapeia o diretório do seu projeto local (`meu_codigo`) e o diretório desejado para saída (`docs`) para o container Docker.
    - Ajuste os caminhos conforme necessário para seu ambiente ou projeto.

3. **O UnivDoc irá gerar a documentação no diretório de saída definido.**

## Como contribuir

Contribuições são muito bem-vindas! Para colaborar, siga os passos abaixo:

1. **Fork o projeto** no GitHub e clone para sua máquina local.
2. **Crie uma branch** para sua feature ou correção de bug:

    ```bash
    git checkout -b minha-feature
    ```

3. **Instale as dependências utilizando o uv:**

    ```bash
    uv pip install -r pyproject.toml
    ```

4. **Faça suas alterações e testes.**
5. **Envie um pull request** detalhando sua proposta.

Se quiser sugerir melhorias, abrir issues ou discutir novas ideias, fique à vontade para utilizar o campo de Issues do GitHub!


## Licença

MIT License (veja o arquivo LICENSE)