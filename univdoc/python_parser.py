import ast

def parse_python_file(filepath):
    """
    Extrai funções e classes, com docstrings e parâmetros, de um arquivo Python.
    Retorna uma lista de objetos para o renderer.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)
    objetos = []

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            obj = {
                "tipo": "função",
                "nome": node.name,
                "docstring": ast.get_docstring(node) or "",
                "parametros": [],
                "retorno": ""
            }
            # Parâmetros da função
            for arg in node.args.args:
                param = {
                    "nome": arg.arg,
                    "descricao": ""
                }
                obj["parametros"].append(param)
            # Retorno (pode ser tipo anotado)
            if getattr(node, "returns", None):
                obj["retorno"] = ast.unparse(node.returns).strip()
            objetos.append(obj)
        elif isinstance(node, ast.ClassDef):
            obj = {
                "tipo": "classe",
                "nome": node.name,
                "docstring": ast.get_docstring(node) or "",
                "parametros": [],
                "retorno": ""
            }
            objetos.append(obj)
    return objetos