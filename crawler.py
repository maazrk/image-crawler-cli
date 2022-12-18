import argparse
from tqdm import tqdm
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from json import dump
from re import compile

# imports from other files
from util.scraping_utils import get_response, get_urlparse_object
from util.helpers import log_error, validate_url, get_image_objects

def cmdline_args():
  # Creates the parser
  my_parser = argparse.ArgumentParser(
    prog='crawler',
    usage='%(prog)s [options] base_url depth',
    allow_abbrev=False,
    description='Crawl specified webpage for images and follow links as per depth',
    epilog='Refer to the README.txt for additional details'
  )

  my_parser.add_argument(
    'base_url',
    metavar='base_url',
    type=str,
    help='base url to start crawling from'
  )

  my_parser.add_argument(
    'depth',
    metavar='depth',
    type=int,
    help='depth of the crawl'
  )

  # Execute the parse_args() method
  args = my_parser.parse_args()
  return args



# Begin execution
args = cmdline_args()

# Initial custom validation
urlparse_object = get_urlparse_object(args.base_url)
validate_url(urlparse_object, args.base_url)

unprocessed_urls = [ args.base_url.rstrip('/') ]

processed_url_set = set(unprocessed_urls)
output = {
  'results': []
}

# Start processing
for depth_idx in tqdm(range(args.depth + 1)):
  is_success = False
  error_message = ''
  tqdm.write("Processing depth: {depth_idx}".format(depth_idx=depth_idx))
  
  next_depth_urls = []
  for url in unprocessed_urls:
    url_object = urlparse(url)
    try:
      tqdm.write("Processing url: {url}".format(url=url))
      response, session = get_response(url)
      response.raise_for_status() # Raise HTTPError if not successful
      is_success = True
    except requests.exceptions.Timeout:
      # Maybe set up for a retry, or continue in a retry loop
      error_message = "Request Timeout"
    except requests.exceptions.TooManyRedirects:
      # Tell the user their URL was bad and try a different one
      error_message = "Too many redirects!"
    except requests.exceptions.HTTPError as err:
      # received an error status code from server
      error_message = str(err)
    except requests.exceptions.RequestException as e:
      # something wrong with the URL
      error_message = "Invalid URL"
    finally:
      if not is_success:
        log_error(url, error_message)
        continue

    soup = BeautifulSoup(response.text, 'html.parser')

    # Fetch images
    image_objects = get_image_objects(soup, url, depth_idx)

    output['results'].extend(image_objects)

    pattern = compile(r'.*(html|htm|xhtml|php|asp|jsp)$')
    webpage_link_tags = soup.find_all('a', href=True)
    webpage_links = [webpage['href'] for webpage in webpage_link_tags]
    for l in webpage_links:
      l_object = urlparse(l)
      
      if l_object.scheme and not l_object.scheme.startswith('http'):
        continue

      if l_object.hostname and l_object.hostname != url_object.hostname:
        continue
      
      if not pattern.match(l_object.path) and '.' in l_object.path:
        continue
      
      new_url = '{scheme}://{hostname}/{path}'.format(scheme=url_object.scheme, hostname=url_object.hostname, path=(l_object.path.strip('/'))).strip('/')
      if new_url not in processed_url_set:
        
        processed_url_set.add(new_url)
        next_depth_urls.append(new_url)


  unprocessed_urls = next_depth_urls 
      

    
with open('results.json', 'w') as file:
  dump(output, file)
  tqdm.write('Saved image links successfully to results.json')
