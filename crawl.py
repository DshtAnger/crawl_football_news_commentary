#!/usr/bin/env python
#coding:utf8
try:
    import requests,re,json,datetime
    from bs4 import BeautifulSoup
    from selenium import webdriver
except ImportError as e:
    print '[*]',e
    print '[*]请安装以上模块!'
finally:
    exit()

def getYesterday(date_time=None):
    '''
    args:
        date_time = 'year-mon-day' e.g '2016-10-24'
        if set up date_time,the function returns all days before date_time.
        if not , the function returns all days before today.
    '''
    if date_time:
        year,mon,day = map(int,date_time.split('-'))
        today = datetime.datetime(year,mon,day).date()
    else:
        today = datetime.date.today()

    day_count = 0
    while 1:
        oneday = datetime.timedelta(days=day_count)
        yesterday = today - oneday 
        yield yesterday
        day_count += 1

def get_news_from_163(url,filename):
    #'http://goal.sports.163.com/39/match/report/2016/1643183.html'
    html = requests.get(url).content
    soup = BeautifulSoup(html,'lxml')
    p_head = ''.join([i.get_text().strip()+'\n' for i in soup.select('#endText > div:nth-of-type(1) > p')]).encode('utf-8')
    p_foot = ''.join([i.get_text().strip()+'\n' for i in soup.select('#endText > p')]).encode('utf-8')
    p = p_head + p_foot
    with open('./'+filename+'_news_163','w') as f:
        f.write(p)
    print '[done]'+filename+'_news_163'

def get_news_from_sina(url,filename):
    #'http://sports.sina.com.cn/g/pl/2016-10-23/doc-ifxwztru6912664.shtml'
    html = requests.get(url).content
    soup = BeautifulSoup(html,"lxml")
    artibody = ''.join([p.get_text().rstrip()+'\n' for p in soup.select('#artibody > p')]).encode('utf-8')
    with open('./'+filename+'_news_sina','w') as f:
        f.write(artibody)
    print '[done]'+filename+'_news_sina'

def get_commentary(url,filename):
    #'http://match.sports.sina.com.cn/livecast/9/iframe/scroll_iframe.php?opta_id=879260'
    #'http://match.sports.sina.com.cn/livecast/1/iframe/live_log.html?148424'

    driver = webdriver.PhantomJS(executable_path="/home/DshtAnger/phantomjs/bin/phantomjs")
    driver.get(url)
    html = driver.page_source

    soup = BeautifulSoup(html,"lxml")
    commentary = soup.select('table')[0].select('tr')

    text = ''.join([column.get_text().replace(' ','')+' ' for row in commentary for column in row.contents if row.contents.index(column)!=0])
    text = re.sub("(?P<every_row>(\S*\s){3})", lambda matched:matched.group("every_row")[:-1]+'\n',text).encode('utf-8')

    with open('./'+filename+'_commentary','w') as f:
        f.write(text)
    print '[done]'+filename+'_commentary' 

def get_vaild_teamlist_from_sina(date_time):
    headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'U_TRS1=0000007c.38f8745.580a0303.8d9d3649; UOR=www.baidu.com,blog.sina.com.cn,; SINAGLOBAL=113.140.11.124_1477051139.978885; vjuids=-998d437c6.157e71be4b4.0.7df38ce201085; SCF=AqipzjEOj7WKHad7Faly9zwC8OXgsG_pW-ntUWxlFauS_NzS-X9jVoAFK0XQ7fIBibO-14ynhU06ImCp-i83Swc.; sso_info=v02m6alo5qztKWRk5yljpOQpZCToKWRk5iljoOgpZCjnLONk5C0jbOcuYyDkLeJp5WpmYO0s42TkLSNs5y5jIOQtw==; Apache=2488804210389.5767.1477222369400; ULV=1477222369556:2:2:1:2488804210389.5767.1477222369400:1477051146847; U_TRS2=0000007a.31ac47ca.580c9fe0.0d1bc185; PLATFORM_APACHE2_YF=17bc65eab15c08a7d8eed110f8d1e349; PLATFORM_APACHE2_JA=3bcc72c6e7b514813bc37f8c88915c78; vjlast=1477224230; SGUID=1477224420707_53749116; lxlrttp=1477110876; SUB=_2AkMvUCjddcNhrABUnPwSy2LiaIpH-jzEiebBAn7tJhIyOBgv7lYPqSVIvCBQz8yMkTAjIlJLx8VUgUItRw..; rotatecount=3; ArtiFSize=14;',
    'Host':'platform.sina.com.cn',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    }

    url = 'http://platform.sina.com.cn/sports_other/livecast_dateschedule?app_key=3633771828&date={0}'.format(date_time)

    response = requests.get(url,headers=headers)

    assert(response.status_code != 404)

    html = response.content
    data = json.loads(html)

    team_list = [[i['Team1'].encode('utf-8'),i['Team2'].encode('utf-8'),i['NewsUrl'],i['shilu_url']]for i in data['result']['data'] if i['ShortTitle']!=u'\u4e2d\u8d85' and i['NewsUrl']!='' and i['shilu_url']!='' and i['Team1']!='']

    return team_list

def get_data_main(date_time):
    '''
    args:
        date_time:  year-mon-day    e.g date_time='2016-10-23'
    '''
    headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'vinfo_n_f_l_=4c043730517ac81c.1.3.1476282110.1476872312.1476878523; s_n_f_l_=true; vjuids=-3ab880b11.157b9454f94.0.015ca5a390a43; _ntes_nnid=c22f3cc1480de632053322df517fa61d,1476282109856; _ntes_nuid=c22f3cc1480de632053322df517fa61d; Province=029; City=029; __gads=ID=323b1a3387347489:T=1476357401:S=ALNI_MaKUv9S5012ZzKiTzRvACtQ0FgBrg; vinfo_n_f_l_n3=7699e48a13558deb.1.1.1476282114233.1476282119917.1476364862295; P_INFO=conterloving@163.com|1476787807|2|mail163|00&99|sxi&1476719089&mail163#sxi&610100#10#0#0|&0|mail163|conterloving@163.com; vinfo_n_f_l_=4c043730517ac81c.1.2.1476282110.1476788559.1476868193; JSESSIONID-WYZBS=Yf7qu86QWo%2F%2FfT3JWY3BHX30EZqaEV8fvcSWokYOMJ4mZtPxsuYQ9fpGrhzJ1c5BTWxFrgo%2FjBG3vcl61yhhW4q6yMR1p3PdjUdwN4EzP61K%5C1zGZK%5Czd7aq8PsUru63Hoke%2Bu5Aw9gzdh%2BN%2BftQZW7AMElPI9Ye8vJfwoETBk3fyimQ%3A1476870449969; _dxd9zbs=30; cm_newmsg=user%3Dconterloving%40163.com%26new%3D-1%26total%3D-1; NTESifb-tomcatSI=A61488BB9E69F56A44F65C7BD39CD492.bjzw-sports-ifb1.server.163.org-8010; vjlast=1476282110.1476868182.11',
    'Host':'goal.sports.163.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36'
    }

    url = 'http://goal.sports.163.com/schedule/{0}.html'.format(date_time.replace('-',''))

    response = requests.get(url,headers=headers)

    assert(response.status_code != 404)

    html = response.content

    soup = BeautifulSoup(html,'lxml')

    game_tables = soup.select('table')

    game_items = [j for i in game_tables for j in i.select('tr')[1::3]]

    exists_news_tagObj = [i for i in game_items if i.find_all('a',string='战报'.decode('utf-8')) ]

    exists_news_dict = [{'hTeam':i.select('.c1 > a')[0].get_text().encode('utf-8'),
                         'vTeam':i.select('.c2 > a')[0].get_text().encode('utf-8'),
                         'newsUrl':'http://goal.sports.163.com'+i.select('.bg7 > a')[0]['href']
                        } for i in exists_news_tagObj]

    team_list = get_vaild_teamlist_from_sina(date_time)

    for i in exists_news_dict:
        for j in team_list:
            if [i['hTeam'],i['vTeam']]==j[:2]:
                filename = date_time+'_'+i['hTeam']+'vs'+i['vTeam']
                try:
                    get_news_from_163(i['newsUrl'],filename)
                    get_news_from_sina(j[2],filename)
                    get_commentary(j[3],filename)
                except:
                    continue

if __name__ == '__main__':
    dayObj = getYesterday('2014-11-03')

    while 1:
        day = str(dayObj.next())
        try:
            get_data_main(day)
        except:
            continue
