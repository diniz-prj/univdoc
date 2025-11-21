import os
from .python_parser import parse_python_file
from .php_parser import parse_php_file

# Extensões suportadas e funções de parser
PARSERS = {
    "python": {".py": parse_python_file},
    "php": {".php": parse_php_file},
}

def parse_source_code(source_dir, langs=None, docstyle=None):
    """
    Varre o diretório, detecta arquivos das linguagens escolhidas
    e retorna dados extraídos das docstrings/comentários.
    
    Args:
        source_dir: Diretório do código fonte
        langs: Lista de linguagens a processar (None = todas)
        docstyle: Estilo de docstring preferido (google, numpy, sphinx, rest, phpdoc)
    """
    if langs is None:
        # Se não informadas, detecta todas suportadas
        langs = list(PARSERS.keys())

    arquivos = []

    for root, dirs, files in os.walk(source_dir):
        for filename in files:
            ext = os.path.splitext(filename)[1]
            for lang in langs:
                if ext in PARSERS.get(lang, {}):
                    parser_fn = PARSERS[lang][ext]
                    full_path = os.path.join(root, filename)
                    objetos = parser_fn(full_path, docstyle=docstyle)
                    arquivos.append({
                        "nome": filename,
                        "caminho": full_path,
                        "objetos": objetos
                    })
    return {"arquivos": arquivos, "linguagens": langs}