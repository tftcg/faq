Icons MIT licensed from https://feathericons.com/

This project takes XML files in the faqxml/ directory and, using the generate_site.py script, merges them with Jinja2 templates in the templates/ directory to create a HTML/JavaScript/CSS website in the docs/ directory. 

Top level files:

generate_site.py - This is the Python3 script that takes the data in faqxml/ and generates lots of HTML files.
README.md - This document.
docs/ - This is where the generated HTML files go. There are also a few manually created files here (JavaScript and CSS).
faqxml/ - This is the database of content. 
templates/ - This is where the templates for the website are. Having these saves on putting lots of bits of HTML into the Python script. 
