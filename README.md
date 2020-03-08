# Transformers Trading Card Game FAQ

This project takes XML files in the faqxml/ directory and, using the generate_site.py script, merges them with taglist.xml and Jinja2 templates in the templates/ directory to create a HTML/JavaScript/CSS website in the docs/ directory. 

Top level files:

* generate_site.py - This is the Python3 script that drives everything.
* README.md - This document.
* docs/ - This is where the generated HTML files go. There are also a few manually created files here (JavaScript and CSS).
* faqxml/ - This is the database of content. 
* taglist.xml - This describes the generated website. Pages will only generate for a tag if there is content.
* templates/ - This is where the templates for the website are. Having these saves on putting lots of bits of HTML into the Python script. 

## Taglist XML Format

The XML format for the Taglist file is as follows:

<pre>
 tags (name)
  category (name)
    ...  note that category can be nested infinitely ...
      tag (name, markup_required?)
</pre>

Catagories lead to menu pages, while tags lead, if they have content in the faqxml, to faq pages. The markup_required attribute is optional and turns off the automatic inclusion of any question or answer including that tag's name. This is to stop more common words like "Brave" or "Bold" from including every entry that mentions the term.

## FAQ XML Format

The XML format for the FAQ format is as follows:

<pre>
 faq (name, source, published_date, sourced_at)
   target
     entry (id, mode, xref)
       question
       answer
       tags?
</pre>

Targets can contain two types of entry, a canonical entry or a cross-referenced entry. Questions and Answers currently are purely text with no formatting markup supported.

A canonical entry is one that contains the text for a question and an answer. A cross-referenced entry is one that points to another FAQ entry and copies it into the generated HTML. This way a FAQ about three different cards can appear in all three of those cards' FAQS. Its format is "file-id#entry-id", where the file-id points to a file inside the faqxml directory, without the '.xml' and the entry-id points to an entry in that file with that id. If it's in the same file then a file-id is not needed, the xref string can just be "#entry-id". 

Date formats are ISO-8601; ie: 2020-12-30.

Source formats are URLs. 

The site generation will automatically include any FAQ entry that references a tag's full name, unless markup_required is turned on for that tag. . 

The 'tags' tag is optional and is for use when a FAQ entry does not reference a card, but it would be valuable for that card's page to include that FAQ entry. 

Questions and answers can contain a markup to indicate that a tag applies to that text. This markup is implemented via two square brackets on each side of the term. For example, [[Ion Blaster of Optimus Prime]]. 

## Content source

Icons MIT licensed from https://feathericons.com/

All Official FAQ Content, Transformers Images, and Transformers Trading Card Images are Copyright Hasbro, Inc. Transformers and Transformers Trading Card names, characters, images, trademarks and logos are protected by trademark and other Intellectual Property rights owned by Hasbro, Inc. or its subsidiaries, licensors, licensees, suppliers and accounts. Other provided content is the property of the project contributors. 
