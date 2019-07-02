import requests
from lxml import etree
import re
from uitls import tool
import time
import json
"""


"""




class sougou_1():
   
    tools=tool()
    headers=tools.headers()
    dict_ = tools.dict_()

    def response(self,keyword):
        url = 'https://search.sohu.com/search/meta'
        data=tools.data(keyword)
        response = requests.get(url=url, params=data)
        datas = json.loads(response.text)['data']['media']
        return datas


    def parse(self,data): #解析个人的信息并进行存储到mysql中，只有大于10000粉丝数的才会被存储
        try:
            totalPv=data['scoreMap']['totalPv']
            newsCount=data['scoreMap']['newsCount']
            if totalPv>=100000 and newsCount>=20:
                author = data['userName']  # 用户昵称
                home_url = data['weiboUrl']  # 用户主页地址
                avatar=data['avatorUrl']  # 用户头像地址
                if avatar.split('//')[0]=="http:":
                    avatar_url=avatar
                else:
                    avatar_url='http:'+avatar
                brief = data['description']  # 作者简介
                # fans_num = re.findall('fans_num.*?:\"(.*?)\",', html)[0]  # 粉丝数量
                create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 创建时间
                source_name = '搜狐号'  # 来源名称
                biz="souhu"+str(data['id'])
                # follow_num = re.findall('follow_num.*?:\"(.*?)\",', html)[0] #关注数
                tags=keyword

                sql1='select * from spider_user_info where author="%s"'%author
                cursor=self.tools.sqll(sql1)
                result=cursor.fetchall()
                if not result:
                    sql2='insert into spider_user_info(id,author,biz,avatar_url,home_url, source_name, brief, create_time,tags) values("%s","%s","%s","%s","%s","%s","%s","%s","%s")'%(id,author,biz, avatar_url, home_url,source_name, brief, create_time,tags)
                    self.tools.sqll(sql2)
                    print(id, biz, author, home_url, avatar_url, source_name, brief, create_time, tags)

                else:
                    pass
            else:
                pass
        except Exception as e:
            print(e)


if __name__ == '__main__':
    sougou_1=sougou_1()
    tools = tool()
    list_=tools.list_()
    for keyword in list_:
        datas=sougou_1.response(keyword)
        for data in datas:
            sougou_1.parse(data)

    # f = open("tag.txt", encoding='utf-8')
    # keyword = f.readline()
    # while keyword:
    #     print(keyword)
    #     try:
    #         datas=sougou_1.response(keyword.replace('\n',''))
    #         for data in datas:
    #             sougou_1.parse(data)
    #     except:
    #         pass
    #     keyword = f.readline()
    # f.close()











