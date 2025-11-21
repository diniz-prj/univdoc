import ast
import re

def _parse_google_style_docstring(docstring):
    """
    Parseia docstring no estilo Google.
    Retorna dicionário com descrição, parâmetros e retorno.
    """
    if not docstring:
        return {"descricao": "", "parametros": {}, "retorno": ""}
    
    result = {"descricao": "", "parametros": {}, "retorno": ""}
    lines = docstring.split('\n')
    
    current_section = "descricao"
    desc_lines = []
    param_lines = []
    return_lines = []
    
    for line in lines:
        line_stripped = line.strip()
        
        if line_stripped.startswith("Args:"):
            current_section = "args"
            continue
        elif line_stripped.startswith("Returns:"):
            current_section = "returns"
            continue
        elif line_stripped.startswith("Raises:") or line_stripped.startswith("Yields:") or line_stripped.startswith("Note:") or line_stripped.startswith("Example:"):
            current_section = "other"
            continue
        
        if current_section == "descricao":
            desc_lines.append(line)
        elif current_section == "args":
            param_lines.append(line)
        elif current_section == "returns":
            return_lines.append(line)
    
    result["descricao"] = '\n'.join(desc_lines).strip()
    
    # Parse parâmetros
    param_text = '\n'.join(param_lines)
    param_matches = re.findall(r'(\w+)\s*(?:\([\w\s,\[\]]+\))?\s*:\s*(.+)', param_text)
    for param_name, param_desc in param_matches:
        result["parametros"][param_name.strip()] = param_desc.strip()
    
    result["retorno"] = '\n'.join(return_lines).strip()
    
    return result

def _parse_numpy_style_docstring(docstring):
    """
    Parseia docstring no estilo NumPy.
    Retorna dicionário com descrição, parâmetros e retorno.
    """
    if not docstring:
        return {"descricao": "", "parametros": {}, "retorno": ""}
    
    result = {"descricao": "", "parametros": {}, "retorno": ""}
    lines = docstring.split('\n')
    
    current_section = "descricao"
    desc_lines = []
    param_lines = []
    return_lines = []
    
    for line in lines:
        line_stripped = line.strip()
        
        if line_stripped == "Parameters":
            current_section = "parameters"
            continue
        elif line_stripped in ["Returns", "Return"]:
            current_section = "returns"
            continue
        elif line_stripped.startswith("---"):
            continue
        elif line_stripped in ["Raises", "Yields", "Notes", "Examples"]:
            current_section = "other"
            continue
        
        if current_section == "descricao":
            desc_lines.append(line)
        elif current_section == "parameters":
            param_lines.append(line)
        elif current_section == "returns":
            return_lines.append(line)
    
    result["descricao"] = '\n'.join(desc_lines).strip()
    
    # Parse parâmetros
    param_text = '\n'.join(param_lines)
    param_matches = re.findall(r'(\w+)\s*:\s*(\w+(?:\s*,\s*\w+)*)\s*\n?\s*(.+?)(?=\n\w+\s*:|$)', param_text, re.DOTALL)
    for param_name, param_type, param_desc in param_matches:
        result["parametros"][param_name.strip()] = param_desc.strip()
    
    result["retorno"] = '\n'.join(return_lines).strip()
    
    return result

def _parse_sphinx_style_docstring(docstring):
    """
    Parseia docstring no estilo Sphinx/reST.
    Retorna dicionário com descrição, parâmetros e retorno.
    """
    if not docstring:
        return {"descricao": "", "parametros": {}, "retorno": ""}
    
    result = {"descricao": "", "parametros": {}, "retorno": ""}
    lines = docstring.split('\n')
    
    desc_lines = []
    in_desc = True
    
    for line in lines:
        # Parse :param name: description
        param_match = re.match(r'\s*:param\s+(\w+)\s*:\s*(.+)', line)
        if param_match:
            in_desc = False
            result["parametros"][param_match.group(1)] = param_match.group(2).strip()
            continue
        
        # Parse :type name: type
        type_match = re.match(r'\s*:type\s+\w+\s*:', line)
        if type_match:
            in_desc = False
            continue
        
        # Parse :return: or :returns:
        return_match = re.match(r'\s*:returns?\s*:\s*(.+)', line)
        if return_match:
            in_desc = False
            result["retorno"] = return_match.group(1).strip()
            continue
        
        # Parse :rtype:
        rtype_match = re.match(r'\s*:rtype\s*:', line)
        if rtype_match:
            in_desc = False
            continue
        
        if in_desc:
            desc_lines.append(line)
    
    result["descricao"] = '\n'.join(desc_lines).strip()
    
    return result

def _detect_docstring_style(docstring):
    """
    Detecta automaticamente o estilo da docstring.
    Retorna 'google', 'numpy', 'sphinx' ou 'plain'.
    """
    if not docstring:
        return "plain"
    
    # Verifica estilo Sphinx/reST
    if re.search(r':param\s+\w+:', docstring) or re.search(r':returns?:', docstring):
        return "sphinx"
    
    # Verifica estilo Google
    if re.search(r'\bArgs:\s*\n', docstring) or re.search(r'\bReturns:\s*\n', docstring):
        return "google"
    
    # Verifica estilo NumPy
    if re.search(r'\bParameters\s*\n\s*-+', docstring) or re.search(r'\bReturns?\s*\n\s*-+', docstring):
        return "numpy"
    
    return "plain"

def _parse_docstring_by_style(docstring, docstyle=None):
    """
    Parseia docstring de acordo com o estilo especificado ou detectado.
    """
    if docstyle is None:
        docstyle = _detect_docstring_style(docstring)
    else:
        docstyle = docstyle.lower()
    
    if docstyle == "google":
        return _parse_google_style_docstring(docstring)
    elif docstyle == "numpy":
        return _parse_numpy_style_docstring(docstring)
    elif docstyle in ["sphinx", "rest"]:
        return _parse_sphinx_style_docstring(docstring)
    else:
        # Estilo plain ou desconhecido - retorna docstring como está
        return {"descricao": docstring, "parametros": {}, "retorno": ""}

def parse_python_file(filepath, docstyle=None):
    """
    Extrai funções e classes, com docstrings e parâmetros, de um arquivo Python.
    Retorna uma lista de objetos para o renderer.
    
    Args:
        filepath: Caminho do arquivo Python
        docstyle: Estilo de docstring preferido (google, numpy, sphinx, rest).
                  Se None, detecta automaticamente ou usa padrão Google.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)
    objetos = []
    
    # Se não especificado, assume Google como padrão para Python
    if docstyle is None:
        docstyle = "google"

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            raw_docstring = ast.get_docstring(node) or ""
            parsed_doc = _parse_docstring_by_style(raw_docstring, docstyle)
            
            obj = {
                "tipo": "função",
                "nome": node.name,
                "docstring": parsed_doc["descricao"],
                "parametros": [],
                "retorno": parsed_doc["retorno"]
            }
            # Parâmetros da função
            for arg in node.args.args:
                param_name = arg.arg
                param_desc = parsed_doc["parametros"].get(param_name, "")
                param = {
                    "nome": param_name,
                    "descricao": param_desc
                }
                obj["parametros"].append(param)
            # Retorno (pode ser tipo anotado)
            if getattr(node, "returns", None) and not obj["retorno"]:
                obj["retorno"] = ast.unparse(node.returns).strip()
            objetos.append(obj)
        elif isinstance(node, ast.ClassDef):
            raw_docstring = ast.get_docstring(node) or ""
            parsed_doc = _parse_docstring_by_style(raw_docstring, docstyle)
            
            obj = {
                "tipo": "classe",
                "nome": node.name,
                "docstring": parsed_doc["descricao"],
                "parametros": [],
                "retorno": ""
            }
            objetos.append(obj)
    return objetos