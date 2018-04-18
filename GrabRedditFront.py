import time
import urllib.request
import json
import logging

def main():
  logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
  keepGoing = True
  delayBetweenRequestsSeconds = 5

  while keepGoing:
    try:
      grabRedditFront("earthporn")
      keepGoing = False
    except urllib.error.HTTPError as e:
      logging.warning("Got an HTTPError:{0} ,retrying in {1} seconds...".format(e,delayBetweenRequestsSeconds))
      time.sleep(delayBetweenRequestsSeconds)
    except Error as e:
      logging.error("Unexpected error {0}, exiting...".format(e))
      keepGoing = False


def grabRedditFront(subreddit):
  apiurl = 'http://www.reddit.com/r/' + subreddit + '/hot.json?sort=hot'
  resp = urllib.request.urlopen(apiurl).read()
  holdinfo = json.loads(resp.decode())
  temptime = time.localtime();
  for x in range(25):
    pictureurl = holdinfo['data']['children'][x]['data']['url']
    logging.debug(holdinfo['data']['children'][x]['data']['url'])
    logging.debug(holdinfo['data']['children'][x]['data']['domain'])
    if "imgur.com" in holdinfo['data']['children'][x]['data']['domain']:
      logging.debug("imgur link found")
      if holdinfo['data']['children'][x]['data']['domain'] == 'imgur.com':
        pictureurl = pictureurl + ".jpg"
      logging.info('[{}] '.format(x) + pictureurl)
      urllib.request.urlretrieve (pictureurl, shortenname(pictureurl))
    elif "i.redd.it" in holdinfo['data']['children'][x]['data']['domain']:
      logging.info('[{}] '.format(x) + pictureurl)
      urllib.request.urlretrieve (pictureurl, shortenname(pictureurl))
    else:
      logging.warning('[{}] '.format(x) + "Unrecognized domain:{0}".format(holdinfo['data']['children'][x]['data']['domain']))
  logging.info("Done!") 

def shortenname(name):
  found = False
  gothrough = len(name)
  gothrough -= 1
  holdstr = list(name)
  while gothrough > -1:
      if name[gothrough] == '/' and found == False:
          found = True
      if found:
          del(holdstr[gothrough])
      gothrough -= 1
  name = "".join(holdstr)
  return name

if __name__ == "__main__":
  main()

