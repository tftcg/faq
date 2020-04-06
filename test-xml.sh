for i in "faqxml/*.xml"
do
    xmllint --noout --schema Faq.xsd $i
done
