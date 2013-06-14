"""
"""

# Taken from http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
import os, errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


#

def translate(string, translator):
    
    return reduce(
        lambda s, key: s.replace(key, translator[key]),
        translator,
        string
    )

doi_translator = {
    '.' : '_dot_',
    '/' : '_slash_',
}
def escape_doi(doi):
    
    return translate(doi, doi_translator)
