import requests

from lxml import etree
import re
from uitls import tool
import time
import json
"""


"""




class qiehao_1():
    tools=tool()
    headers=tools.headers()
    dict_ = tools.dict_()

    def response(self,keyword):
        url = 'https://r.inews.qq.com/verticalSearch?chlid=_qqnews_custom_search_qiehao&search_from=click&uid=44ce3651532c37f9&omgid=e76c5bfab95b6547ffab46fb08c39bd795f60010213414&trueVersion=5.8.12&qimei=44ce3651532c37f9&appver=25_android_5.8.12&devid=44ce3651532c37f9&Cookie=lskey%3D;skey%3D;uin%3D;%20luin%3D;logintype%3D0;%20main_login%3D;%20&qn-sig=f50e2c8c758767a6bc87be6605573722&qn-rid=219c9f88-e74a-4670-bb7d-3497cec83c8a'
        data=tools.data(keyword)
        response = requests.post(url, data=data, headers=self.headers, timeout=15)
        html = json.loads(response.text)
        datas = html['secList']
        return datas

    def fan_num(self,url):
        try:
            fans_num=json.loads(requests.get(url).text)['channelInfo']['subCount']
        except:
            fans_num=0
        return fans_num


    def parse(self,data): #解析个人的信息并进行存储到mysql中，只有大于10000粉丝数的才会被存储
        try:
            author =data['chlname']  # 用户昵称
            biz = "qiehao" + str(data['chlid'] )
            home_url = 'https://r.inews.qq.com/getSubItem?chlid={}'.format(data['chlid'])  # 用户主页地址
            avatar_url=data['imgurl']  # 用户头像地址
            brief = data['abstract']  # 作者简介
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 创建时间
            source_name = '企鹅号'  # 来源名称
            fans_num = int(self.fan_num(home_url)) # 粉丝数量
            tags=keyword
            sql1='select * from spider_user_info where author="%s"'%author
            cursor=self.tools.sqll(sql1)
            result=cursor.fetchall()
            if not result and fans_num>=1:
                sql2='insert into spider_user_info(id,author,biz,home_url,avatar_url,brief,create_time,source_name,fans_num,tags) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'%(id,author,biz,home_url,avatar_url,brief,create_time,source_name,fans_num,tags)
                self.tools.sqll(sql2)
                print(id,author,biz,home_url,avatar_url,brief,create_time,source_name,fans_num,tags)
            else:
                pass
        except Exception as e:
            print(e)


if __name__ == '__main__':
    qiehao_1=qiehao_1()
    tools = tool()
    # list_=tools.list_()
    # for keyword in list_:
    #     print(keyword)
    #     datas=qiehao_1.response(keyword)
    #     for data in datas:
    #         qiehao_1.parse(data['omList'][0])

    f = open("tag_2.txt", encoding='utf-8')
    keyword = f.readline()
    while keyword:
        print(keyword)
        try:
            datas=qiehao_1.response(keyword.replace('\n',''))
            for data in datas:
                qiehao_1.parse(data['omList'][0])
        except:
            pass
        keyword = f.readline()
    f.close()











