import os
from jinja2 import Template, Environment, FileSystemLoader

# Global
TOP_OUTPUT_DIR ='docs'

# Generic function to apply a Jinja2 template
def generate_html(infilename, tofilename):
    template_file = open(infilename,'r')
    template_text = template_file.read()
    template = Environment(loader=FileSystemLoader("templates/")).from_string(template_text)

    page=template.render(filename=tofilename)

    f = open(os.path.join(TOP_OUTPUT_DIR, tofilename), "w")
    f.write(page)
    f.close()

generate_html('templates/about.jinja2', 'about.html')
generate_html('templates/contribute.jinja2', 'contribute.html')
generate_html('templates/feedback.jinja2', 'feedback.html')
generate_html('templates/sources.jinja2', 'sources.html')
generate_html('templates/heads.jinja2', 'heads.html')
generate_html('templates/app-bugs.jinja2', 'app-bugs.html')
generate_html('templates/autocon.jinja2', 'autocon.html')
