# encoding: utf-8

import sys
import os.path
from workflow import Workflow


def main(wf):
    import bibtexparser

    p = os.path.expanduser("~/.bibtex_alfred")
    filepaths = open(p).readlines()
    
    bibliography = []

    for filepath in filepaths:
        filecontent = open(os.path.expanduser(filepath.strip())).read()
        for entry in bibtexparser.loads(filecontent).entries:
            bibliography.append(entry)

    query = None

    if len(wf.args):
        query = wf.args[0]
    
    def filter_entry(entry):
        return u"{} {}".format(entry["ID"], entry["title"])

    if query:
        bibliography = wf.filter(query, bibliography, filter_entry)

    for entry in bibliography:
        try:
            wf.add_item(
                title=entry["ID"],
                subtitle=entry["title"],
                modifier_subtitles={"alt": entry["author"]},
                arg=entry["ID"],
                valid=True
            )
        except:
            pass

    # send the results to Alfred as XML
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow(libraries=['./lib'])
    sys.exit(wf.run(main))
