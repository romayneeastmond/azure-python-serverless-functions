import http.client
import re
from bs4 import BeautifulSoup

def find_urls(text):
  url_pattern = r"""(?:(?:https?|ftp)://)?(?:(?:[A-Z0-9-\.]+\.)+[A-Z]{2,}|localhost)(?::\d+)?(?:/[^\s]*)?(?:\?\S*)?"""
  
  urls = re.findall(url_pattern, text, flags=re.IGNORECASE)

  return urls

def get_body_content(content):
  soup = BeautifulSoup(content, "html.parser")
  body = soup.find("body")

  if body:
    def remove_excess_whitespace(text):
      return re.sub(r"\s+", " ", text)

    for header in body.find_all("header"):
      header.decompose()

    for footer in body.find_all("footer"):
      footer.decompose()

    for navigation in body.find_all("nav"):
      navigation.decompose()

    return remove_excess_whitespace(body.get_text(strip=False)).strip()
  else:
    return content

def get_webpage_content(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    scheme = url.split("://")[0]
    host = url.split("//")[1].split("/")[0]
    path = "/" + "/".join(url.split("//")[1].split("/")[1:])

    headers = {
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
       "Accept": "*/*", 
       "Connection": "keep-alive"       
    }

    try:
      if scheme == "https":
          connection = http.client.HTTPSConnection(host)
      else:
          connection = http.client.HTTPConnection(host)

      connection.request("GET", path, headers=headers)
      response = connection.getresponse()

      if response.status == 200:
          content = response.read().decode("utf-8", errors="replace")
      else:
          content = None

      connection.close()
      
      return content
    except:
      return None