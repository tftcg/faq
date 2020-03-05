Icons MIT licensed from https://feathericons.com/

This project takes XML files in the faqxml/ directory and, using the generate_site.py script, merges them with Jinja2 templates in the templates/ directory to create a HTML/JavaScript/CSS website in the docs/ directory. 

Top level files:

* generate_site.py - This is the Python3 script that takes the data in faqxml/ and generates lots of HTML files.
* README.md - This document.
* docs/ - This is where the generated HTML files go. There are also a few manually created files here (JavaScript and CSS).
* faqxml/ - This is the database of content. 
* templates/ - This is where the templates for the website are. Having these saves on putting lots of bits of HTML into the Python script. 

== FAQ XML Format ==

The XML format for the FAQ format is as follows:

<pre>
 faq (name, source, published_date, sourced_at)
   target (name, source)
     entry (id, mode, xref)
       question
       answer
</pre>

Each target has a different web page generated for it. Targets can contain two types of entry, a canonical entry or a cross-referenced entry. Questions and Answers currently are purely text with no formatting markup supported.

A canonical entry is one that contains the text for a question and an answer. A cross-referenced entry is one that points to another FAQ entry and copies it into the generated HTML. This way a FAQ about three different cards can appear in all three of those cards' FAQS. Its format is "file-id#entry-id", where the file-id points to a file inside the faqxml directory, without the '.xml' and the entry-id points to an entry in that file with that id. If it's in the same file then a file-id is not needed, the xref string can just be "#entry-id". 

Date formats are ISO; ie: 2020-12-30.
Source formats are URLs. If a target has a source, it will override the faq element's source attribute for any practical uses within the site generation. 
