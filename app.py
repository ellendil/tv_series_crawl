#!/usr/bin/python

import yaml
from urllib.request import Request, urlopen

# TODO:
#  -> find latest episode:
#     * file names search / deluged / db fil
#  -> extract season and episode number from name

url_headers={'User-Agent': 'Mozilla/5.0'}

def getContent(url):
  request = Request(url, headers=url_headers)
  req_content = urlopen(request).read()
  data = req_content.decode('utf-8')
  return data

def findTorrentLinks(html_data):
  lines = html_data.split('\n')
  result = []
  for l in lines:
    if ".torrent\"" in l and "<a href" in l:
      search_str = "href=\""
      start_idx = l.find(search_str)
      end_idx = l.find("\" class=", start_idx)
      result.append(l[start_idx+len(search_str): end_idx])
  return result

def downloadTorrentFile(url, file_name):
  request = Request(url, headers=url_headers)
  with urlopen(request) as response, open(file_name, 'wb') as out_file:
    data = response.read() # a `bytes` object
    out_file.write(data)

with open("config-local.yaml", 'r') as config_file:
  conf = yaml.load(config_file)
  print(conf)

  for entry in conf['tv_series']:
      print('Entry: ')
      print(entry['name'])
      print(entry['url'])
      content = getContent(entry['url'])
      links = findTorrentLinks(content)
      for l in links:
        print(l)
      downloadTorrentFile(links[0], "/home/maras/supernatural_test.torrent")
