# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.request

from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template

app = Flask(__name__)

slack_token = "xoxp-501387243681-505169228468-506795408608-6da7d98444cfc486181f3f44c5e38428"
slack_client_id = "501387243681.506928506337"
slack_client_secret = "7d6dce8d2f85b23eb8901b31e8e195f1"
slack_verification = "5o65xOPV2xja5ufayEOz5SIP"
sc = SlackClient(slack_token)
url_list = {
    "광주" : "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EA%B4%91%EC%A3%BC%EB%82%A0%EC%94%A8&oquery=%EB%8C%80%EC%A0%84%EB%82%A0%EC%94%A8&tqi=UtVEcspySERssup%2FyWKssssssLC-131166",
    "서울" :  "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%84%9C%EC%9A%B8%EB%82%A0%EC%94%A8&oquery=%EA%B4%91%EC%A3%BC%EB%82%A0%EC%94%A8&tqi=UtVxZdpySDVsstsFt84ssssssuR-157551",
    "대전" :  "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%8C%80%EC%A0%84%EB%82%A0%EC%94%A8&oquery=%EA%B4%91%EC%A3%BC%EB%82%A0%EC%94%A8&tqi=UtVyodpySENsscXDhpGssssst3G-300663",
    "제주" :  "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%A0%9C%EC%A3%BC%EB%82%A0%EC%94%A8&oquery=%EB%8C%80%EC%A0%84%EB%82%A0%EC%94%A8&tqi=UtV1RwpVuENsstxO1OdssssstzK-174883",
    "대구" :  "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%8C%80%EA%B5%AC%EB%82%A0%EC%94%A8&oquery=%EC%A0%9C%EC%A3%BC%EB%82%A0%EC%94%A8&tqi=UtV1AlpVuEGssZF%2FT%2B4ssssssWZ-387128",
    "인천" :  "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%9D%B8%EC%B2%9C%EB%82%A0%EC%94%A8&oquery=%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80&tqi=UtV1%2FspVuFdsscarjGNssssssG4-089038",
    "경기" :  "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EA%B2%BD%EA%B8%B0%EB%82%A0%EC%94%A8&oquery=%EC%9D%B8%EC%B2%9C%EB%82%A0%EC%94%A8&tqi=UtV24lpVuECsstgdLxRssssssks-281102",
    "강원" :  "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EA%B0%95%EC%9B%90%EB%82%A0%EC%94%A8&oquery=%EA%B2%BD%EA%B8%B0%EB%82%A0%EC%94%A8&tqi=UtV2MwpVuFRssc0V790ssssssUd-468802",
    "충남" :  "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%B6%A9%EB%82%A8%EB%82%A0%EC%94%A8&oquery=%EA%B0%95%EC%9B%90%EB%82%A0%EC%94%A8&tqi=UtV2plpVuE0ssvKreRRssssssmR-176239",
    "세종" :  "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%84%B8%EC%A2%85%EB%82%A0%EC%94%A8&oquery=%EC%B6%A9%EB%82%A8%EB%82%A0%EC%94%A8&tqi=UtV2WspVuFKssum%2BCjZssssst40-349225",
    "충북" :  "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%B6%A9%EB%B6%81%EB%82%A0%EC%94%A8&oquery=%EC%84%B8%EC%A2%85%EB%82%A0%EC%94%A8&tqi=UtV2XwpVuEwsssKlRuVssssssoR-155890",
    "경북" :  "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EA%B2%BD%EB%B6%81%EB%82%A0%EC%94%A8&oquery=%EC%B6%A9%EB%B6%81%EB%82%A0%EC%94%A8&tqi=UtV2wlpVuEossbLdehdssssssQR-122213",
    "전북" :  "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%A0%84%EB%B6%81%EB%82%A0%EC%94%A8&oquery=%EA%B2%BD%EB%B6%81%EB%82%A0%EC%94%A8&tqi=UtV2ywpVuE4ssa3KeQVssssssAG-078473",
    "전남" :  "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%A0%84%EB%82%A8%EB%82%A0%EC%94%A8&oquery=%EC%A0%84%EB%B6%81%EB%82%A0%EC%94%A8&tqi=UtV20dpVuFRssscymJKssssstbw-455584",
    "경남" :  "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EA%B2%BD%EB%82%A8%EB%82%A0%EC%94%A8&oquery=%EC%A0%84%EB%82%A8%EB%82%A0%EC%94%A8&tqi=UtV22spVuFsssts1fWhssssssEd-139947",
    "울산" :  "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%9A%B8%EC%82%B0%EB%82%A0%EC%94%A8&oquery=%EA%B2%BD%EB%82%A8%EB%82%A0%EC%94%A8&tqi=UtV23lpVuElssaO8PXdssssss%2Fs-419881",
    "부산" :  "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%B6%80%EC%82%B0%EB%82%A0%EC%94%A8&oquery=%EC%9A%B8%EC%82%B0%EB%82%A0%EC%94%A8&tqi=UtV2HspVuEVssc%2BqTOdssssssrd-505300"    
}
# 크롤링 함수 구현하기
def _crawl_naver_keywords(text):
    
    #여기에 함수를 구현해봅시다.
    #url = re.search(r'(https?://\S+)', text.split('|')[0]).group(0)
    
    textlist = text.split()
    keywords = []
    dicts = {}
    url = ""
    if "미세먼지" in textlist :
        url = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80"
    else :
        if textlist[1] in url_list :
            url = url_list[textlist[1]]
        else :
            keywords.append("없는 지역입니다!!!")
            return u'\n'.join(keywords)

    req = urllib.request.Request(url)
    sourcecode = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")
  
    if "미세먼지" in textlist :
        keylist = []
        valuelist = []
        box = soup.find("div", class_ = "tb_scroll")
        for data in box.find_all("th") :
            keylist.append(data.get_text())
        keylist = keylist[4:]
       
            
        for data in box.find_all("td") :
            valuelist.append(data.get_text())
            
        for index in range(len(keylist)) :
            valueindex = index * 3
            s = " 미세먼지는" + " " + valuelist[valueindex] + "로 "
            state = ""
            value = int(valuelist[valueindex])

            if value >= 0 and value <= 15 :
                state = "좋음 입니다. 오늘은 좋은 사람과 소풍가시는게 어때요?"
            elif value >= 16 and value <= 35 :
                state = "보통 입니다. 높진 않아서 다행이네요!"
            elif value >= 36 and value <= 74 :
                state = "나쁨 입니다. 마스크를 착용하시는게 어때요?"
            elif value >= 75 and value <= 149 :
                state = "매우나쁨 입니다. 미세먼지 주의보가 발령 됬어요!!! 마스크는 필수!!!"
            elif value >= 150 :
                state = "매우나쁨 입니다. 미세먼지 경보가 발령 됬어요!!! 마스크는 필수!!! 외출도 자제하세요!!!"
            s += state    
            s += ", 오전예보: " + valuelist[valueindex + 1] + ", 오후예보: " + valuelist[valueindex + 2] + "입니다."
            dicts[keylist[index]] = s

        if textlist[1] in dicts :
            keywords.append(textlist[1] + dicts[textlist[1]])    
        else :
            keywords.append("그건 잘 모르겠어요 ㅠㅠ")
    elif "날씨" in textlist:
        now_temp=[]
        low_temp=[]
        high_temp=[]

        for data in soup.find_all("span",class_="todaytemp"):
            if not data.get_text() in keywords :
                now_temp.append(data.get_text())
              
        now_temps = now_temp[0]
        
        for data in soup.find_all("span",class_="merge"):
            if not data.get_text() in keywords:
                low_temp.append(data.get_text())
        
        low_temps = low_temp[0]

        keywords.append("현재 온도는 " + str(now_temps) + "도 입니다\n" + "최저/최고온도는 " + str(low_temps) + "입니다\n" )            
    else :
        keywords.append("그건 잘 모르겠어요 ㅠㅠ")
    
    # 한글 지원을 위해 앞에 unicode u를 붙혀준다.
    return u'\n'.join(keywords)

# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])

    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]

        keywords = _crawl_naver_keywords(text)
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=keywords
        )

        return make_response("App mention message has been sent", 200,)

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})

@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                             "application/json"
                                                            })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})
    
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})

@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"

if __name__ == '__main__':
    app.run('127.0.0.1', port=8080)
