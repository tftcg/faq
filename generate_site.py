import os
import glob
from jinja2 import Template, Environment, FileSystemLoader
import xml.etree.ElementTree as ET 
import json

def safe_name(name):
    return name.lower().replace(' ', '-').replace('---', '-').replace("'", '').replace('?', '').replace('(','').replace(')', '').replace('&-', '').replace(',', '').replace('/-', '')

def clean_markup(text):
    return text.replace('[[', '').replace(']]', '')

def mkdirp(directory):
    # TODO: if os.path.isfile(directory)
    if( not os.path.isdir(directory) ):
        os.makedirs(directory)

# Heavyweight way to get the data for a xref tag
# TODO: USE THE faq_db CACHE!!!
def get_xref(xref):
    # split on #
    xref_data = xref.split('#')
    file = xref_data[0] + ".xml"
    id = xref_data[1]
    # Open file xml file
    tree = ET.parse(os.path.join('faqxml', file))
    faq_node = tree.getroot()
    # Search for <entry id="<id>">
    xpath = "[@id='" + id + "']"
    node = faq_node.find(".//entry[@id='" + id + "']")
    target_node = faq_node.find(".//entry[@id='" + id + "']...")
    # Return node to that entry along with the source data

    source_url = faq_node.attrib['source_url']
    if('source' in faq_node.attrib):
        source_name = faq_node.attrib['source']
    else:
        source_name = faq_node.attrib['name']

    # Override with target's source # TODO: Move away from this
    if('source_url' in target_node.attrib):
        source_url = target_node.attrib['source_url']
        if('source' in target_node.attrib):
            source_name = target_node.attrib['source']
        else:
            source_name = target_node.attrib['name']

    return [source_name, source_url, node]


def source_image_name(source_name):
    if("FAQ" in source_name):
        return 'gold'
    elif("Roundup" in source_name):
        return 'red'
    else:
        return 'blue'

# TODO: Support cross referencing somehow. 
# xreffing is done via an entry with xref="". This points to another entry with an id.
# ids are optional, but must exist on a target. ids must also be unique. 
# Generally ids are only expected to exist when an entry needs to be xrefable. 

# Solution:
#   xrefs should be hierarchical; i.e. they should indicate the file they are found in.
#   thus if an xref is prefixed with a #, then it is in the same file. If it is an alphanum, then a diff file.
#   In the latter case, another file will need to be loaded for a quick scan for the content. 
#   Format is:   xref="#foo"  (same file)   and xref="dir/file#foo"   foo in the dir/file file



# Global
TOP_OUTPUT_DIR ='docs'   # TODO: Move this back to docs


def generate_leaf(node, faq_db, output_dir, leaf_template, parent_node):
    # TODO: Do I want to put all the leaves at a top level /tags/*.html level?
    filename = os.path.join(output_dir, safe_name(node.attrib['name']) + ".html")
    leaf_name = node.attrib['name']
    markup = '[[' + leaf_name + ']]'
    markup_required = False
    if('markup_required' in node.attrib and node.attrib['markup_required'].lower() == 'true'):
        markup_required = True


    found_entries = []    # contains array of name, source_url, node

    # Find FAQ entries for this leaf_name
    # Loop over every key, value in the faq_db
    for name, node in faq_db.items():
        source_url = node.attrib['source_url']
        if('source' in node.attrib):
            source_name = node.attrib['source']
        else:
            source_name = name
        for target_node in node.findall('./target'):
            # TODO: Override source_url/name if the target has one?; though generally moving away from that style
            for entry_node in target_node.findall('./entry'):
                # Look for any <target> with a name that matches the leaf_name
                if target_node.attrib['name'] == leaf_name:
                    found_entries.append( [source_name, source_url, entry_node] )
                # Look for "[[leaf_name]]" in each entry. If found, add that node.
                elif not markup_required and leaf_name in ET.tostring(entry_node).decode():
                    found_entries.append( [source_name, source_url, entry_node] )
                elif markup in ET.tostring(entry_node).decode():
                    found_entries.append( [source_name, source_url, entry_node] )

    if(len(found_entries) != 0):
        page = leaf_template.render(f_safe_name=safe_name, f_clean_markup=clean_markup, entries=found_entries, faq_name=leaf_name, f_source_image_name=source_image_name, parent_node=parent_node, f_get_xref=get_xref)

        f = open(filename, "w")
        f.write(page)
        f.close()

    return len(found_entries)

def generate_branch(node, faq_db, output_dir, tag_blocks, category_blocks, branch_template, parent_node):
    filename = os.path.join(output_dir, 'index.html')

    page=branch_template.render(f_safe_name=safe_name, tag_blocks=tag_blocks, category_blocks=category_blocks, parent_node=parent_node, this_node=node)

    f = open(filename, "w")
    f.write(page)
    f.close()

def walk_branch(node, faq_db, output_dir, leaf_template, branch_template, parent_node=None):

    tag_blocks = []
    category_blocks = []
    total_found = 0
    found_tags = {}   # Used to build the json_index

    mkdirp(output_dir)

    for tag_node in node.findall('./tag'):
        found = generate_leaf(tag_node, faq_db, output_dir, leaf_template, node)
        if(found > 0):
            tag_blocks.append([tag_node, found])
            total_found += found
            found_tags[tag_node.attrib['name']] = (output_dir + "/" + safe_name(tag_node.attrib['name']) + ".html").replace(TOP_OUTPUT_DIR, '')

    for category_node in node.findall('./category'):
        subdir = os.path.join(output_dir, safe_name(category_node.attrib['name']))
        found_data = walk_branch(category_node, faq_db, subdir, leaf_template, branch_template, node)
        if(found_data[0] > 0):
            category_blocks.append([category_node, found_data[0]])
            total_found += found_data[0]
            found_tags.update(found_data[1])

    generate_branch(node, faq_db, output_dir, tag_blocks, category_blocks, branch_template, parent_node)

    return [total_found, found_tags]

# Load Leaf Template
leaf_template_file = open('templates/leaf.jinja2','r')
leaf_template_text = leaf_template_file.read()
leaf_template = Environment(loader=FileSystemLoader("templates/")).from_string(leaf_template_text)

# Load Branch Template
branch_template_file = open('templates/branch.jinja2','r')
branch_template_text = branch_template_file.read()
branch_template = Environment(loader=FileSystemLoader("templates/")).from_string(branch_template_text)

# Load the taglist.xml file
tree = ET.parse('taglist.xml')
taglist_node=tree.getroot()

faq_db = {}
# Load all the FAQ XML files
for file in glob.glob('faqxml/**/*.xml', recursive=True):
    tree = ET.parse(file)
    faq_node=tree.getroot()
    faq_name=faq_node.attrib['name']
    faq_db[faq_name] = faq_node

found_data = walk_branch(taglist_node, faq_db, TOP_OUTPUT_DIR, leaf_template, branch_template)

# Generate json index
f = open(os.path.join(TOP_OUTPUT_DIR, "faqindex.json"), "w")
f.write(json.dumps(found_data[1]))
f.close()

def generate_html(infilename, tofilename):
    template_file = open(infilename,'r')
    template_text = template_file.read()
    template = Environment(loader=FileSystemLoader("templates/")).from_string(template_text)

    page=template.render()

    f = open(os.path.join(TOP_OUTPUT_DIR, tofilename), "w")
    f.write(page)
    f.close()

#generate_html('templates/index.jinja2', 'index.html')
generate_html('templates/about.jinja2', 'about.html')
generate_html('templates/contribute.jinja2', 'contribute.html')
generate_html('templates/sources.jinja2', 'sources.html')
