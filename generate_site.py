import os
import glob
from jinja2 import Template, Environment, FileSystemLoader
import xml.etree.ElementTree as ET 
import json

def convert_name(name):
    return name.lower().replace(' ', '-').replace('---', '-').replace("'", '').replace('?', '').replace('(','').replace(')', '').replace('&-', '').replace(',', '').replace('/-', '')

def clean_markup(text):
    return text.replace('[[', '').replace(']]', '')

# Heavyweight way to get the data for a xref tag
# TODO: Consider caching each file as it loads. Especially for the current file. 
def get_xref(xref, parent_path):
    # split on #
    xref_data = xref.split('#')
    if(xref.startswith('#')):
        file = parent_path + ".xml"
        id = xref_data[1]
    else:
        file = xref_data[0] + ".xml"
        id = xref_data[1]
    # Open file xml file
    tree = ET.parse(os.path.join('faqxml', file))
    root = tree.getroot()
    # Search for <entry id="<id>">
    xpath = "[@id='" + id + "']"
    node = root.find(".//entry[@id='" + id + "']")
    target_node = root.find(".//entry[@id='" + id + "']...")
    # Return node to that entry along with the source data
    source_info = get_source_info(root, target_node)
    return [node, source_info]

def get_source_info(faq_node, target_node):
    link = faq_node.attrib['source_url']
    if('source' in faq_node.attrib):
        name = faq_node.attrib['source']
    else:
        name = faq_node.attrib['name']
    if('source_url' in target_node.attrib):
        link = target_node.attrib['source_url']
        if('source' in target_node.attrib):
            name = target_node.attrib['source']
        else:
            name = target_node.attrib['name']

    if("FAQ" in name):
        color = 'gold'
    elif("Roundup" in name):
        color = 'red'
    else:
        color = 'blue'

    return { 'color' : color, 'link' : link, 'name' : name }

# TODO: Support cross referencing somehow. 
# xreffing is done via an entry with xref="". This points to another entry with an id.
# ids are optional, but must exist on a target. ids must also be unique. 
# Generally ids are only expected to exist when an entry needs to be xrefable. 

# Solution:
#   xrefs should be hierarchical; i.e. they should indicate the file they are found in.
#   thus if an xref is prefixed with a #, then it is in the same file. If it is an alphanum, then a diff file.
#   In the latter case, another file will need to be loaded for a quick scan for the content. 
#   Format is:   xref="#foo"  (same file)   and xref="dir/file#foo"   foo in the dir/file file

output_dir='docs'

target_index = {}

# Find each xml file in faqxml
for file in glob.glob('faqxml/**/*.xml', recursive=True):
    print("Parsing " + file)
    tree = ET.parse(file)
    faq_node=tree.getroot()
    faq_name=faq_node.attrib['name']

    # Load Leaf Template
    template_file = open('templates/leaf.jinja2','r')
    template_text = template_file.read()
    template = Environment(loader=FileSystemLoader("templates/")).from_string(template_text)

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
        name = target_node.attrib['name']
        # Add the target details to generate an index page
        targets.append(name)

        # Generating page for the target
        safe_name = convert_name(name)
        default_source_info = get_source_info(faq_node, target_node)
        page = template.render(faq_name=faq_name, get_xref=get_xref, safe_name=safe_name, target=target_node, parent_path=parent_path, default_source_info=default_source_info, clean_markup=clean_markup)

        f = open(os.path.join(target_dir, safe_name + ".html"), "w")
        f.write(page)
        f.close()

        # This is a URL snippet, so hardcode the /
        target_index[name] = parent_path + "/" + safe_name + ".html"

    # Load Branch Template
    branch_template_file = open('templates/branch.jinja2','r')
    branch_template_text = branch_template_file.read()
    branch_template = Environment(loader=FileSystemLoader("templates/")).from_string(branch_template_text)

    page=branch_template.render(faq_name=faq_name, convert_name=convert_name, targets=targets)

    f = open(os.path.join(output_dir, parent_path, "index.html"), "w")
    f.write(page)
    f.close()

# Generate json index
f = open(os.path.join(output_dir, "faqindex.json"), "w")
f.write(json.dumps(target_index))
f.close()

def generate_html(infilename, tofilename):
    template_file = open(infilename,'r')
    template_text = template_file.read()
    template = Environment(loader=FileSystemLoader("templates/")).from_string(template_text)

    page=template.render()

    f = open(os.path.join(output_dir, tofilename), "w")
    f.write(page)
    f.close()


generate_html('templates/index.jinja2', 'index.html')
generate_html('templates/about.jinja2', 'about.html')
generate_html('templates/contribute.jinja2', 'contribute.html')
generate_html('templates/sources.jinja2', 'sources.html')
