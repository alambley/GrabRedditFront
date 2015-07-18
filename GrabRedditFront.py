import time
import urllib.request
import json

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
 
apiurl = 'http://www.reddit.com/r/earthporn/hot.json?sort=hot'
resp = urllib.request.urlopen(apiurl).read()
holdinfo = json.loads(resp.decode())
temptime = time.localtime();
for x in range(25):
    pictureurl = holdinfo['data']['children'][x]['data']['url']
    if holdinfo['data']['children'][x]['data']['domain'] == 'imgur.com' or holdinfo['data']['children'][x]['data']['domain'] == 'i.imgur.com':
        if holdinfo['data']['children'][x]['data']['domain'] == 'imgur.com':
            pictureurl = pictureurl + ".jpg"
        print ('[{}] '.format(x) + pictureurl)
        urllib.request.urlretrieve (pictureurl, shortenname(pictureurl))
print ("Done!") 



