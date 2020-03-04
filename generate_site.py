import os
import glob
from jinja2 import Template, Environment, FileSystemLoader
import xml.etree.ElementTree as ET 

def convert_name(name):
    return name.lower().replace(' ', '-').replace('---', '-').replace("'", '').replace('?', '').replace('(','').replace(')', '').replace('&-', '').replace(',', '').replace('/-', '')


# TODO: Support cross referencing somehow. 

# Find each xml file in faqxml
for file in glob.glob('faqxml/**/*.xml', recursive=True):
    tree = ET.parse(file)
    faq_node=tree.getroot()
    faq_name=faq_node.attrib['name']

    # Load Leaf Template
    template_file = open('templates/leaf.jinja2','r')
    template_text = template_file.read()
    template = Environment(loader=FileSystemLoader("templates/")).from_string(template_text)

    output_dir='docs'

    #for target_node in faq_node.findall('./target'):
        # if an xref entry
        # load that content from elsewhere
    #    print(template.render(target=target_node))

    parent_path = file.replace('faqxml/', '').replace('.xml', '')
    target_dir = os.path.join(output_dir, parent_path)
    # TODO: if os.path.isfile(target_dir)
    if( not os.path.isdir(target_dir) ):
        os.makedirs(target_dir)

    targets=[]

    for target_node in faq_node.findall('./target'):
        # Add the target details to generate an index page, and a search index
        targets.append(target_node.attrib['name'])

        # Generating page for the target
        safe_name=convert_name(target_node.attrib['name'])
        page=template.render(faq_name=faq_name, safe_name=safe_name, target=target_node)

        f = open(os.path.join(target_dir, safe_name + ".html"), "w")
        f.write(page)
        f.close()

    # Load Branch Template
    branch_template_file = open('templates/branch.jinja2','r')
    branch_template_text = branch_template_file.read()
    branch_template = Environment(loader=FileSystemLoader("templates/")).from_string(branch_template_text)

    page=branch_template.render(faq_name=faq_name, convert_name=convert_name, targets=targets)

    f = open(os.path.join(output_dir, parent_path, "index.html"), "w")
    f.write(page)
    f.close()
