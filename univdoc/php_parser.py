import re

def _parse_phpdoc_docstring(docstring):
    """
    Parseia docstring no estilo PHPDoc.
    Retorna dicionário com descrição, parâmetros e retorno.
    """
    if not docstring:
        return {"descricao": "", "parametros": {}, "retorno": ""}
    
    result = {"descricao": "", "parametros": {}, "retorno": ""}
    lines = docstring.split('\n')
    
    desc_lines = []
    
    for line in lines:
        line = line.strip()
        
        # Parse @param
        param_match = re.match(r'@param\s+(?:\S+\s+)?(\$?\w+)\s*([^@]+)?', line)
        if param_match:
            param_name = param_match.group(1).replace('$', '')
            param_desc = param_match.group(2) or ""
            result["parametros"][param_name] = param_desc.strip()
            continue
        
        # Parse @return
        return_match = re.match(r'@return\s+(.+)', line)
        if return_match:
            result["retorno"] = return_match.group(1).strip()
            continue
        
        # Ignora outras tags
        if line.startswith('@'):
            continue
        
        # Descrição
        desc_lines.append(line)
    
    result["descricao"] = '\n'.join(desc_lines).strip()
    
    return result

def parse_php_file(filepath, docstyle=None):
    """
    Extrai funções e classes, com comentários e parâmetros, de um arquivo PHP.
    Retorna uma lista de objetos para o renderer.
    Simplificado para PSR-5/PHPDoc.
    
    Args:
        filepath: Caminho do arquivo PHP
        docstyle: Estilo de docstring preferido. Para PHP, usa PHPDoc como padrão.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    # Se não especificado, assume PHPDoc como padrão para PHP
    if docstyle is None:
        docstyle = "phpdoc"
    
    # Encontrar docblocks e classes/funções
    objetos = []
    docblock_re = r"/\*\*(.*?)\*/\s*(?:public|protected|private|static|\s)*\s*(function|class)\s+(\w+)"
    for match in re.finditer(docblock_re, source, flags=re.DOTALL):
        raw_docstring = match.group(1).replace("*", "").strip()
        tipo = "função" if match.group(2) == "function" else "classe"
        nome = match.group(3)
        
        # Parse docstring se for PHPDoc
        if docstyle.lower() in ["phpdoc", "php"]:
            parsed_doc = _parse_phpdoc_docstring(raw_docstring)
        else:
            parsed_doc = {"descricao": raw_docstring, "parametros": {}, "retorno": ""}
        
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
                        param_desc = parsed_doc["parametros"].get(param_nome, "")
                        parametros.append({
                            "nome": param_nome,
                            "descricao": param_desc
                        })

        objetos.append({
            "tipo": tipo,
            "nome": nome,
            "docstring": parsed_doc["descricao"],
            "parametros": parametros,
            "retorno": parsed_doc["retorno"]
        })

    return objetos