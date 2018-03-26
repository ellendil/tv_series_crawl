#!/usr/bin/python

import yaml
import urllib.request

# TODO:
#  -> find latest episode:
#     * file names search / deluged / db fil
#  -> extract season and episode number from name


# This is done to create custom agent for web requests
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

def getContent(url):
  request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
  req_content = urllib.request.urlopen(request).read()
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
  urllib.request.urlretrieve(url, file_name)

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
      downloadTorrentFile(links[0], "/home/maras/supernatural.torrent")
