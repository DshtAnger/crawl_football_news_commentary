#!/usr/bin/env python
#coding:utf8
try:
    import requests,re,sys
    from bs4 import BeautifulSoup
except ImportError,e:
    print '[*]',e
    print '[*]请安装以上模块!'
finally:
    exit(0)

def crawl_football_commentary(gid_url,filename):
    filename = filename+'-commentary'
    HOST = None
    headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'__cfduid=d8a226c01bf4bdcd0b3c8c84485d3c42c1476281600; bdshare_firstime=1476281683121; ASP.NET_SessionId=xmbody453fxedl55wa14vm45; Hm_lvt_dee537944ee53fa0a74f9331eb267090=1476282309,1476355791; Hm_lpvt_dee537944ee53fa0a74f9331eb267090=1476355918; Hm_lvt_ed0d5c974af42c3059b9628b90d84901=1476281989,1476282046,1476282177,1476355517; Hm_lpvt_ed0d5c974af42c3059b9628b90d84901=1476358368; Hm_lvt_ee4c6d61150fa5612601a3f321e3b3f2=1476281989,1476282177,1476355517,1476355879; Hm_lpvt_ee4c6d61150fa5612601a3f321e3b3f2=1476358368',
    'Host':HOST,
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }
    
    #该网站通过Ajax加载，需要从框架页面源码中取到gid再请求另一个接口页面
    HOST = 'wlive.7m.cn'
    gid_response = requests.get(gid_url,headers=headers)

    assert(gid_response.status_code != 404)

    gid_html = gid_response.content
    gid = re.search(r"gid=(.*?);", gid_html).group(1)

    #请求真正的接口页面,获得json数据
    HOST = 'js.wlive.7m.cn'
    target_url = 'http://js.wlive.7m.cn/livedata.aspx?l=gb&d=' + gid
    target_reponse = requests.get(target_url,headers=headers)
    target_html = target_reponse.content

    #从数据中提取时间、主队、客队信息，用作文件名
    # game_date = re.findall(r'"date":"(.*?)"', target_html)[0].split()[0]
    # game_hTeam = re.findall(r'"hTeam":"(.*?)"', target_html)[0]
    # game_vTeam = re.findall(r'"vTeam":"(.*?)"', target_html)[0]
    # filename = game_date + '-' + game_hTeam + 'vs' + game_vTeam

    #每段json都从"textFeed"字样后开始直播正文，截取到这里，方便后续匹配
    commentary_begin_index = target_html.index('"textFeed"')
    target_html = target_html[commentary_begin_index:]

    #每行一条时间+事件，text_message将所有条目串联为一个字符串，写入文件
    data = re.findall(r'"time":(\d*?),"msg":"(.*?)"',target_html)
    text_message = ''.join(["{0[0]}分{0[1]}秒:{1}\n".format(map(str,divmod(int(i[0]),60)),i[1]) for i in data])
    with open('./'+filename,'w') as f:
        f.write(text_message)
    print '[done]'+filename


def crawl_football_news(news_url,filename):
    filename = filename+'-news'
    headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'UOR=www.baidu.com,sports.sina.com.cn,; SINAGLOBAL=61.150.43.121_1476281132.545073; U_TRS1=00000079.d73e73a6.57fe4332.5f0d52f6; SGUID=1476281415537_37486726; bdshare_firstime=1476281475419; _ct_uid=57fe44c3.8a401ee; vjuids=-1853c7234f.157b93d5e7f.0.badbb99444762; lxlrtst=1476359906_o; vjlast=1476368466; sinaGlobalRotator_http%3A//sports.sina.com=799; SCF=ApLZEIjlOOuvuwutTeqJSSSK-sDcfFjuNJZaquwkBhL3lkZRI7_b8uLV7blImUgOA4s4WRcyIE-HWTJdbEzRL00.; sso_info=v02m6alo5qztKWRk5yljpOQpZCToKWRk5iljoOgpZCjnLONk5C0jbOcuYyDkLeJp5WpmYO0s42TkLSNs5y5jIOQtw==; Apache=113.140.11.123_1476424221.564663; U_TRS2=0000007b.3c742b0b.5800721e.c5bc03ca; ULV=1476424418610:5:5:5:113.140.11.123_1476424221.564663:1476424261782; ALF=1507961618; rotatecount=4; ArtiFSize=14; Hm_lvt_35ddcac55ce8155015e5c5e313883b68=1476365181,1476368264,1476368586,1476424262; Hm_lpvt_35ddcac55ce8155015e5c5e313883b68=1476432422; DCVideoRat_all=3; SUB=_2AkMvXB01dcNhrABUnPwSy2LiaIpH-jzEiebBAn7tJhMyOBgv7gouqSVMRIPynKYBTKeWSFzmso9kwdjpJw..; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WW1DE1jDPF0yz9uJDoOoMpX; DCVideoRat_vhead1,vhead2,vhead4,vhead5=1; lxlrttp=1476359906; DCVideoRat_vbanner=1; DCVideoRat_vcorner=1; DCVideoRat_vtrail=4',
    'Host':'sports.sina.com.cn',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }
    response = requests.get(news_url,headers=headers)

    assert(response.status_code != 404)

    html = response.content
    soup = BeautifulSoup(html,"lxml")
    artibody = ''.join([p.get_text().rstrip()+'\n' for p in soup.select('#artibody > p')]).encode('utf-8')
    with open('./'+filename,'w') as f:
        f.write(artibody)
    print '[done]'+filename


def crawl_main(url):
    headers = {
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection':'keep-alive',
    'Cookie':'UOR=www.baidu.com,sports.sina.com.cn,; SINAGLOBAL=61.150.43.121_1476281132.545073; U_TRS1=00000079.d73e73a6.57fe4332.5f0d52f6; SGUID=1476281415537_37486726; vjuids=-1853c7234f.157b93d5e7f.0.badbb99444762; lxlrtst=1476359906_o; vjlast=1476368466; ArtiFSize=14; SCF=ApLZEIjlOOuvuwutTeqJSSSK-sDcfFjuNJZaquwkBhL3lkZRI7_b8uLV7blImUgOA4s4WRcyIE-HWTJdbEzRL00.; ALF=1507907683; sso_info=v02m6alo5qztKWRk5yljpOQpZCToKWRk5iljoOgpZCjnLONk5C0jbOcuYyDkLeJp5WpmYO0s42TkLSNs5y5jIOQtw==; Apache=113.140.11.123_1476424221.564663; U_TRS2=0000007b.3c742b0b.5800721e.c5bc03ca; PLATFORM_APACHE2_YF=bbe80e3d8b48fd0784febee3eab7ff98; PLATFORM_APACHE2_JA=c9feed950dcef2c620977e270ce9e068; ULV=1476424418610:5:5:5:113.140.11.123_1476424221.564663:1476424261782; lxlrttp=1476359906',
    'Host':'platform.sina.com.cn',
    'Referer':'http://sports.sina.com.cn/g/pl/fixtures.html',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }

    response = requests.get(url,headers=headers)
    assert(response.status_code != 404)
    html = response.content

    #日期用来命名文件，主客队信息是从7m数据中筛选的关键
    game_info = re.findall(r'"date":"(.*?)".*?"Team1":"(.*?)","Team2":"(.*?)".*?"NewsUrl":"(.*?)"',html)

    
    for each_game in game_info:

        date = each_game[0]
        hTeam = each_game[1].decode('unicode_escape').encode('utf-8')
        vTeam = each_game[2].decode('unicode_escape').encode('utf-8')

        filename = date + '-' + hTeam + 'vs' + vTeam

        #oid在7m首页中获得，是点击`直播`按钮时，跳转链接中的变量数字,同样是动态加载,api如下,由6位数字的年月值请求到该时间下所有比赛的数据页
        url_7m_get_oid = 'http://wlive.7m.cn/gamedata/gb/{0}.js'.format(''.join(date.split('-')[:2]))
        response_7m_get_oid = requests.get(url_7m_get_oid)

        assert(response_7m_get_oid != 404)

        html_7m_get_oid = response_7m_get_oid.content
        #从某具体年月时间下所有比赛数据中进行匹配，过滤的关键词为主队与客队的名字
        #手工测试时未发现一个月内两队有多次交手的情况，该情况未考虑，可考虑后续改进
        oid = re.findall(r'"oid":(\d*?),.*?"hTeam":"{0}","vTeam":"{1}"'.format(hTeam,vTeam), html_7m_get_oid)
        #因为有的比赛有战报但没被7m收录，所以要判断findall是否匹配到
        if not oid:
            continue
        else:
            oid = oid[0]

        commentary_get_gid_url = 'http://wlive.7m.cn/live/gb/{0}.shtml'.format(oid)
        newsUrl = each_game[3].replace("\\","")
        if not newsUrl:
            continue
        try:
            #进入解说主页面，函数内将动态加载的内容请求出来
            crawl_football_commentary(commentary_get_gid_url,filename)
            #进入新闻主页面，页面为直接全部加载，bs4匹配
            crawl_football_news(newsUrl, filename)
        except:
            print '[erro]'+filename

if __name__ == '__main__':
    #战报信息来源:http://sports.sina.com.cn/g/pl/fixtures.html
    #直播信息来源:http://wlive.7m.cn
    
    #新浪足球战报接口api
    url = 'http://platform.sina.com.cn/sports_all/client_api?_sport_t_=livecast&_sport_a_=matchesByType&app_key=3571367214&type={type}&rnd={rnd}&season={season}'
    #type参数表示比赛类型 1:意甲,2:西甲,3:德甲,4:英超,5法甲
    #rnd标示轮次,一般都是38轮
    #season表示赛季,取值为2012-2015
    
    #由于7m只收录上述5种比赛中的英超和西甲,so type取值2和4
    for season in xrange(2012,2016):
        for type in [2,4]: 
            for rnd in xrange(1,39):
                crawl_main(url.format(season=season,type=type,rnd=rnd))
