grep  ' id="' faqxml/* | grep -v 'xref' | sed 's/.xml: *<entry id="/__/' | sed 's/".*//' | sed 's/faqxml\//#/' | sort -u > FAQ_IDS
find docs/ -type f -name '*.html' | xargs grep 'faq_entry' | sed 's/^.* id="/#/' | sed 's/".*//' | sort -u > PUBLISHED_IDS
diff FAQ_IDS PUBLISHED_IDS > DIFF_IDS
rm FAQ_IDS PUBLISHED_IDS
