from jinja2 import Environment, FileSystemLoader, select_autoescape

def render_markdown(doc_data, template_path, output_file):
    """
    Renderiza a documentação usando um template Jinja2 e salva como Markdown.
    """
    env = Environment(
        loader=FileSystemLoader(searchpath=os.path.dirname(template_path)),
        autoescape=select_autoescape(["md", "jinja"]),
        trim_blocks=True,
        lstrip_blocks=True
    )
    template_name = os.path.basename(template_path)
    template = env.get_template(template_name)

    rendered = template.render(**doc_data)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rendered)