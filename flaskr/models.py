# coding:utf-8
import sys
import re
import pprint
import MeCab
import json, config
import collections
import warnings
from requests_oauthlib import OAuth1Session
from operator import itemgetter

warnings.filterwarnings('ignore')

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET

def mecab_analyze(twitter_name):
    twitter = OAuth1Session(CK, CS, AT, ATS)
    twitter_params ={'count' : 300}
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=" + twitter_name
    res = twitter.get(url, params = twitter_params)

    combined_text = ""

    if res.status_code == 200:
        timelines = json.loads(res.text)
        for line in timelines:
            #text += unicode.encode(re.sub("https?://[\w/:%#\$&\?\(\)~\.=\+\-]+", "", line['text']), "utf-8") + "\n"
            text = re.sub("https?://[\w/:%#\$&\?\(\)~\.=\+\-]+", "", line['text']) + "\n"
            combined_text += re.sub("@[\w]+", "", text) + "\n"

        words = []
        m = MeCab.Tagger("-Ochasen")
        node = m.parseToNode(combined_text)
        while node:
            if node.feature.startswith("名詞,一般") or node.feature.startswith("名詞,固有名詞") or node.feature.startswith("名詞,形容動詞") or node.feature.startswith("名詞,サ変接続"):
                words.append(node.surface)
            node = node.next
            
        counter = collections.Counter(words)
        counter = sorted(counter.items(), key=itemgetter(1), reverse=True)

        result = counter[0:10]

        return result

    else: #正常通信出来なかった場合
        return false
