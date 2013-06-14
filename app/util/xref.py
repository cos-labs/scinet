"""
"""

# Imports
import json
import time
import requests
import urlparse

doi_url = 'http://dx.doi.org/'

# Get crawl-delay parameter from robots.txt
from reppy.cache import RobotsCache
robots = RobotsCache()
doi_delay = robots.delay(doi_url, '*')

def doi_to_csl(doi):
    """ Fetch CSL-formatted reference by DOI. """

    # Build URL
    url = urlparse.urljoin(doi_url, doi)
    
    # Send request
    req = requests.get(
        url, 
        headers={
            'accept' : 'application/citeproc+json'
        }
    )

    # Wait for crawl-delay
    time.sleep(doi_delay)

    # Parse CSL JSON
    csl = json.loads(req.text)

    # Return parsed CSL
    return csl
