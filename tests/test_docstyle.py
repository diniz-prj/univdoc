"""Testes para a funcionalidade de docstyle do UnivDoc."""

import os
import tempfile
import shutil
import pytest
from univdoc.python_parser import parse_python_file, _detect_docstring_style, _parse_google_style_docstring, _parse_numpy_style_docstring, _parse_sphinx_style_docstring
from univdoc.php_parser import parse_php_file, _parse_phpdoc_docstring
from univdoc.parser import parse_source_code


class TestPythonDocstringStyles:
    """Testes para diferentes estilos de docstring Python."""
    
    def test_detect_google_style(self):
        """Testa detecção de estilo Google."""
        docstring = """Função de exemplo.
        
        Args:
            param1: Descrição do parâmetro
        
        Returns:
            Resultado da função
        """
        assert _detect_docstring_style(docstring) == "google"
    
    def test_detect_numpy_style(self):
        """Testa detecção de estilo NumPy."""
        docstring = """Função de exemplo.
        
        Parameters
        ----------
        param1 : str
            Descrição do parâmetro
        
        Returns
        -------
        str
            Resultado da função
        """
        assert _detect_docstring_style(docstring) == "numpy"
    
    def test_detect_sphinx_style(self):
        """Testa detecção de estilo Sphinx."""
        docstring = """Função de exemplo.
        
        :param param1: Descrição do parâmetro
        :returns: Resultado da função
        """
        assert _detect_docstring_style(docstring) == "sphinx"
    
    def test_parse_google_style(self):
        """Testa parsing de docstring Google."""
        docstring = """Calcula a soma.
        
        Args:
            a (int): Primeiro número
            b (int): Segundo número
        
        Returns:
            int: A soma
        """
        parsed = _parse_google_style_docstring(docstring)
        assert "Calcula a soma" in parsed["descricao"]
        assert "a" in parsed["parametros"]
        assert "Primeiro número" in parsed["parametros"]["a"]
        assert "A soma" in parsed["retorno"]
    
    def test_parse_numpy_style(self):
        """Testa parsing de docstring NumPy."""
        docstring = """Calcula a soma.
        
        Parameters
        ----------
        a : int
            Primeiro número
        b : int
            Segundo número
        
        Returns
        -------
        int
            A soma
        """
        parsed = _parse_numpy_style_docstring(docstring)
        assert "Calcula a soma" in parsed["descricao"]
        assert "a" in parsed["parametros"]
        assert "A soma" in parsed["retorno"]
    
    def test_parse_sphinx_style(self):
        """Testa parsing de docstring Sphinx."""
        docstring = """Calcula a soma.
        
        :param a: Primeiro número
        :param b: Segundo número
        :returns: A soma
        """
        parsed = _parse_sphinx_style_docstring(docstring)
        assert "Calcula a soma" in parsed["descricao"]
        assert "a" in parsed["parametros"]
        assert "Primeiro número" in parsed["parametros"]["a"]
        assert "A soma" in parsed["retorno"]


class TestPHPDocstringStyles:
    """Testes para estilo PHPDoc."""
    
    def test_parse_phpdoc_style(self):
        """Testa parsing de docstring PHPDoc."""
        docstring = """Calcula a soma de dois números
        
        @param int $a Primeiro número
        @param int $b Segundo número
        @return int A soma
        """
        parsed = _parse_phpdoc_docstring(docstring)
        assert "Calcula a soma" in parsed["descricao"]
        assert "a" in parsed["parametros"]
        assert "Primeiro número" in parsed["parametros"]["a"]
        assert "A soma" in parsed["retorno"]


class TestParsersWithDocstyle:
    """Testa os parsers com parâmetro docstyle."""
    
    def test_python_parser_with_google_style(self, tmp_path):
        """Testa parser Python com estilo Google."""
        test_file = tmp_path / "test_google.py"
        test_file.write_text('''
def soma(a, b):
    """Soma dois números.
    
    Args:
        a (int): Primeiro número
        b (int): Segundo número
    
    Returns:
        int: A soma
    """
    return a + b
''')
        
        objetos = parse_python_file(str(test_file), docstyle="google")
        assert len(objetos) == 1
        assert objetos[0]["nome"] == "soma"
        assert "Soma dois números" in objetos[0]["docstring"]
        assert len(objetos[0]["parametros"]) == 2
        assert objetos[0]["parametros"][0]["nome"] == "a"
        assert "Primeiro número" in objetos[0]["parametros"][0]["descricao"]
    
    def test_python_parser_with_numpy_style(self, tmp_path):
        """Testa parser Python com estilo NumPy."""
        test_file = tmp_path / "test_numpy.py"
        test_file.write_text('''
def soma(a, b):
    """Soma dois números.
    
    Parameters
    ----------
    a : int
        Primeiro número
    b : int
        Segundo número
    
    Returns
    -------
    int
        A soma
    """
    return a + b
''')
        
        objetos = parse_python_file(str(test_file), docstyle="numpy")
        assert len(objetos) == 1
        assert objetos[0]["nome"] == "soma"
        assert "Soma dois números" in objetos[0]["docstring"]
        assert len(objetos[0]["parametros"]) == 2
    
    def test_python_parser_with_sphinx_style(self, tmp_path):
        """Testa parser Python com estilo Sphinx."""
        test_file = tmp_path / "test_sphinx.py"
        test_file.write_text('''
def soma(a, b):
    """Soma dois números.
    
    :param a: Primeiro número
    :param b: Segundo número
    :returns: A soma
    """
    return a + b
''')
        
        objetos = parse_python_file(str(test_file), docstyle="sphinx")
        assert len(objetos) == 1
        assert objetos[0]["nome"] == "soma"
        assert "Soma dois números" in objetos[0]["docstring"]
        assert len(objetos[0]["parametros"]) == 2
        assert objetos[0]["parametros"][0]["nome"] == "a"
        assert "Primeiro número" in objetos[0]["parametros"][0]["descricao"]
    
    def test_php_parser_with_phpdoc_style(self, tmp_path):
        """Testa parser PHP com estilo PHPDoc."""
        test_file = tmp_path / "test_phpdoc.php"
        test_file.write_text('''<?php
/**
 * Soma dois números
 *
 * @param int $a Primeiro número
 * @param int $b Segundo número
 * @return int A soma
 */
function soma($a, $b) {
    return $a + $b;
}
?>
''')
        
        objetos = parse_php_file(str(test_file), docstyle="phpdoc")
        assert len(objetos) == 1
        assert objetos[0]["nome"] == "soma"
        assert "Soma dois números" in objetos[0]["docstring"]
        assert len(objetos[0]["parametros"]) == 2
        assert objetos[0]["parametros"][0]["nome"] == "a"
        assert "Primeiro número" in objetos[0]["parametros"][0]["descricao"]


class TestParseSourceCodeWithDocstyle:
    """Testa função parse_source_code com parâmetro docstyle."""
    
    def test_parse_source_code_passes_docstyle(self, tmp_path):
        """Verifica que parse_source_code passa docstyle para os parsers."""
        test_dir = tmp_path / "test_code"
        test_dir.mkdir()
        
        test_file = test_dir / "test.py"
        test_file.write_text('''
def exemplo(param):
    """Função de exemplo.
    
    Args:
        param (str): Um parâmetro
    
    Returns:
        str: O resultado
    """
    return param
''')
        
        result = parse_source_code(str(test_dir), langs=["python"], docstyle="google")
        assert "arquivos" in result
        assert len(result["arquivos"]) == 1
        assert len(result["arquivos"][0]["objetos"]) == 1
        assert result["arquivos"][0]["objetos"][0]["nome"] == "exemplo"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
