#!/usr/bin/python3

import yaml
from urllib.request import Request, urlopen

from os import listdir
from os.path import isfile, join

import re

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

def extractEpisodeTag(filename):
  p = re.compile('S\d\dE\d\d', re.IGNORECASE)
  tag = p.findall(filename)
  if(len(tag) == 1):
    return tag[0]
  else:
    return ""

def getLatestEpisode():
  location = "/home/maras/Supernatural/"
  movie_ext="mkv"
  files = [f for f in listdir(location) if isfile(join(location, f)) and f.endswith(movie_ext)]
  episodes_tags = sorted(list(map(extractEpisodeTag, files)))
  return episodes_tags[-1]

if __name__ == "__main__":
#==================================================#
  last_episode = getLatestEpisode()
  with open("config.yaml", 'r') as config_file:
    conf = yaml.load(config_file)
    print(conf)

    for entry in conf['tv_series']:
      print('Entry: ')
      print(entry['name'])
      print(entry['url'])
      content = getContent(entry['url'])
      links = findTorrentLinks(content)
      for l in links:
        link_tag = extractEpisodeTag(l)
        if(link_tag > last_episode and ("720p" not in l)):
          print(l+" | "+link_tag)
      
#      downloadTorrentFile(links[0], "/home/maras/supernatural_test.torrent")
