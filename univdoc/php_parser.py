import re

def parse_php_file(filepath):
    """
    Extrai funções e classes, com comentários e parâmetros, de um arquivo PHP.
    Retorna uma lista de objetos para o renderer.
    Simplificado para PSR-5/PHPDoc.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    # Encontrar docblocks e classes/funções
    objetos = []
    docblock_re = r"/\*\*(.*?)\*/\s*(?:public|protected|private|static|\s)*\s*(function|class)\s+(\w+)"
    for match in re.finditer(docblock_re, source, flags=re.DOTALL):
        docstring = match.group(1).replace("*", "").strip()
        tipo = "função" if match.group(2) == "function" else "classe"
        nome = match.group(3)
        parametros = []

        if tipo == "função":
            # Captura parâmetros (simples - pode melhorar)
            func_re = r"function\s+" + re.escape(nome) + r"\s*\(([^)]*)\)"
            params_match = re.search(func_re, source)
            if params_match:
                params = params_match.group(1).split(",")
                for param in params:
                    param = param.strip()
                    if param:
                        param_nome = param.split()[-1].replace("$", "")
                        parametros.append({
                            "nome": param_nome,
                            "descricao": ""
                        })

        objetos.append({
            "tipo": tipo,
            "nome": nome,
            "docstring": docstring,
            "parametros": parametros,
            "retorno": ""
        })

    return objetos