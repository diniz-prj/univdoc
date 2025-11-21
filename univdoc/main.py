import os
import sys
import click
from .parser import parse_source_code
from .renderer import render_markdown

DEFAULT_TEMPLATES = {
    "simple": os.path.join(os.path.dirname(__file__), "templates", "simple.md.jinja"),
    "elegant": os.path.join(os.path.dirname(__file__), "templates", "elegant.md.jinja"),
}


@click.command()
@click.option('--source', '-s', required=True, type=click.Path(exists=True, file_okay=False, readable=True), help="Diretório do código fonte a ser documentado.")
@click.option('--lang', '-l', default=None, help="Linguagens para documentar, separadas por vírgula. Exemplo: python,php")
@click.option('--output', '-o', default="./docs", type=click.Path(), help="Diretório de saída para a documentação gerada.")
@click.option('--template', '-t', default="simple", help="Template Jinja2 para geração da documentação (simple, elegant ou caminho para arquivo).")
def cli(source, lang, output, template):
    """
    UnivDoc -- Gerador universal de documentação por docstrings.
    """
    click.echo("🔎 Extraindo informações do código-fonte...")

    # Linguagens escolhidas
    langs = None
    if lang:
        langs = [l.strip().lower() for l in lang.split(",") if l]

    # Template: default ou customizado
    if template in DEFAULT_TEMPLATES:
        template_path = DEFAULT_TEMPLATES[template]
    elif os.path.isfile(template):
        template_path = template
    else:
        click.echo(f"❌ Template '{template}' não encontrado. Dica: escolha 'simple', 'elegant' ou informe o caminho completo para um arquivo jinja2.")
        sys.exit(1)

    # Cria diretório de saída se não existe
    if not os.path.exists(output):
        os.makedirs(output)

    # Parse arquivos e gera estrutura de documentação
    doc_data = parse_source_code(source, langs)

    # Gera Markdown
    output_file = os.path.join(output, "documentacao.md")
    render_markdown(doc_data, template_path, output_file)

    click.echo(f"✅ Documentação gerada com sucesso em {output_file}!")

if __name__ == "__main__":
    cli()