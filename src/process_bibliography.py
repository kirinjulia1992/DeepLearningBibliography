#!/usr/bin/env python

import bibtexparser
#from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import *
import codecs
#import sys

HTML = 1
LATEX = 2

def customizations(record):
    """Use some functions delivered by the library

    :param record: a record
    :returns: -- customized record
    """
    record = type(record)
    record = author(record)
    record = editor(record)
    record = journal(record)
    record = keyword(record)
    record = link(record)
    record = page_double_hyphen(record)
    record = doi(record)
    return record

def build_topics_to_titles_with_id(bib_database):
    id_to_entry = {}
    topics_to_titles_with_id = {}

    for entry in bib_database.entries:
        if entry.has_key('id'):  # probably unecessary, but for now
            id_to_entry[entry['id']] = entry

        if entry.has_key('keyword'):
            keywords = [keyword.strip().lower() for keyword in entry['keyword'].split(',')]
            for keyword in set(keywords):
                if not topics_to_titles_with_id.has_key(keyword):
                    topics_to_titles_with_id[keyword] = []
                if entry.has_key('title') and entry.has_key('id'):
                    topics_to_titles_with_id[keyword].append((entry['id'], entry['title']))

    return (topics_to_titles_with_id, id_to_entry)


def create_hyperlinks_to_topics(topics_to_titles_with_id, ignore_topics, out_fh, output_type):
    #global topic, topic_line_len, spaceless_topic
    topic_line_len = 0

    for topic in sorted(topics_to_titles_with_id):
        topic = topic.lower().strip()
        if not topic.lower().strip() in ignore_topics:
            topic_line_len += len(topic) + 3
            if topic_line_len > 100:
                out_fh.write(u"<br>\n")
                topic_line_len = 0
            spaceless_topic = topic.replace(u' ', u'_')
            out_fh.write(u'''<a href="#%s">[%s]</a> ''' % (spaceless_topic, topic))
            # print topic, len(topics_to_titles_with_id[topic]), topics_to_titles_with_id[topic][:2]


def create_list_of_titles_per_topic(topics_to_titles_with_id, ignore_topics, out_fh, output_type):
    for topic in sorted(topics_to_titles_with_id):
        print
        topic = topic.lower().strip()
        if not topic in ignore_topics:
            spaceless_topic = topic.replace(' ', '_')
            out_fh.write(u'''<h2><a name="%s"></a>%s</h2>''' % (spaceless_topic, topic.title()))
            out_fh.write(u"\n")
            out_fh.write(u"<ol>")
            out_fh.write(u"\n")
            for (pubid, title) in topics_to_titles_with_id[topic]:
                out_fh.write(u'''<li><a href="#%s">%s</a>\n''' % (pubid, title))
                out_fh.write(u"\n")
            out_fh.write(u"</ol>")
            out_fh.write(u"\n")
            out_fh.write("<br>")


def main(bibtexfilepath, out_fh, output_type):
    with open(bibtexfilepath) as bibtex_file:
        bibtex_str = bibtex_file.read()
        bib_database = bibtexparser.loads(bibtex_str)
        # print(bib_database.entries)

        (topics_to_titles_with_id, id_to_entry) = build_topics_to_titles_with_id(bib_database)

        ignore_topics = ['', 'misc']

        # a) create hyperlinks to topics
        create_hyperlinks_to_topics(topics_to_titles_with_id, ignore_topics, out_fh, output_type=HTML)

        # b) create list of titles per topic
        create_list_of_titles_per_topic(topics_to_titles_with_id, ignore_topics, out_fh, output_type=HTML)

        # c) create bibtex list at the end, that get pointed to by 2
        #for pubid in sorted(id_to_entry):
        #    print '''<a name="%s"></a>''' % (pubid)

        #parser = BibTexParser()
        #parser.customization = customizations
        #bib_database = bibtexparser.loads(bibtex_str, parser=parser)
        #print(bib_database.entries)


if __name__ == "__main__":
    out_fh = codecs.open("deeplearningbibliography.html", "wb", encoding="utf-8")
    main(bibtexfilepath = '../bibtex/deeplearninggpuwithkeywords2014.bib', out_fh=out_fh, output_type=HTML)
    out_fh.close()

