for i in *.bit
do
    newhtml=`echo $i | sed 's/bit$/html/'`
    cat header.inc $i footer.inc > ${newhtml}
done
