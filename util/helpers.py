from tqdm import tqdm
import sys

def log_error(url, error_message):
  # Outputs the metadata of the request in the console
  tqdm.write("Error encountered while fetching {url}, error_message: {error_message}\n".format(url=url, error_message=error_message))

def get_image_objects(soup, url, depth_idx):
  # Returns formatted image objects
  img_tags = soup.find_all('img', src=True)
  img_urls = [img['src'] for img in img_tags]
  return [{'imageUrl': img_url, 'sourceUrl': url, 'depth': depth_idx} for img_url in img_urls]


def validate_url(url_object, url):
  # Performs a basic validation for checking presence of netloc and scheme
  if '' in [url_object.netloc, url_object.scheme]:
    tqdm.write("Invalid URL: '{url}', Expected format: https://google.com".format(url=urls[idx]))
    sys.exit()




