import requests
from urllib.parse import urlparse

def get_response(url):
  # Returns a session object and the response for the URL specified
  session = requests.Session()
  response = session.get(url)
  return response, session


def get_urlparse_object(url):
  # Returns the urlparse object for the url specified
  return urlparse(url)