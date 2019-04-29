import requests
from lxml import etree
import re
from uitls import tool
import time
"""
此处为第一模块，设置了26个类目爬取每个类目下10页的作者，并且只取粉丝数大于10000的作者
由于百家号网站的特殊性我这里是使用selenium进行访问，而且必须添加cookie，在作者的信息页
面前面还要访问百度页面两次，直接访问会出现 please try again 连续访问两次就可正常返回。

"""




class baijia_1():
    from uitls import tool
    tools=tool()
    headers=tools.headers()
    dict_ = tools.dict_()
    browser = tools.browser()


    def get_author(self,i,j):#获取列表作者的个人主页url
        datas={
            "word":"{}+百家号".format(i),
            "pd":"cambrian_list",
            "atn":"index",
            "title":"{}+百家号".format(i),
            "lid":"8219726775998088715",
            "ms":"1",
            "frsrcid":"206",
            "frorder":"1",
            "sig":"593303",
            "pn":10*j,
            "mod":"1",
        }
        url = 'https://m.baidu.com/sf'
        response=requests.get(url,params=datas,headers=self.headers)
        response.encoding = 'utf-8'
        html = response.text
        tree = etree.HTML(html)
        datas=tree.xpath('//div[@class="sfc-cambrian-list-subscribe"]')
        urls=[]
        for data in datas:
            url=data.xpath('./div/a/@href')[0]
            urls.append(url)
        return urls


    def get_id(self,url): #获取作者id拿到得
        response = requests.get(url=url)
        response.encoding = 'utf-8'
        html = response.text
        try:
            app_id=re.findall('home/(.*)\?from=dusite_sresults"',html)[0]
            return app_id
        except:
            pass


    def homepage(self,app_id):  # 通过id获取个人主页页面信息
        for i in self.dict_:
            self.browser.add_cookie({
                'name': i,
                'value': self.dict_[i],
            })
        url = 'https://author.baidu.com/profile?context={%22from%22:%22dusite_sresults%22,%22app_id%22:%22' + str(
            app_id) + '%22}&cmdType=&pagelets[]=root&reqID=0&ispeed=1'
        self.browser.get(url)
        html = self.browser.page_source
        return html


    def parse(self,html): #解析个人的信息并进行存储到mysql中，只有大于10000粉丝数的才会被存储
        html = html.replace("\\", "")
        author = re.findall('display_name\":\"(.*?)\"', html)[0].encode("gb18030", "ignore").decode("utf8","ignore").replace("\\", "")  # 用户昵称
        home_url = 'https://author.baidu.com/home/' + app_id  # 用户主页地址
        avatar_url = re.findall('avatar_raw\":\"(.*?)",', html)[0]  # 用户头像地址
        brief = str(re.findall('sign\":\"(.*?)\",', html)[0]).encode("gb18030", "ignore").decode("utf8","ignore").replace("\\","")  # 作者简介
        fans_num = re.findall('fans_num.*?:\"(.*?)\",', html)[0]  # 粉丝数量
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 创建时间
        source_name = '百家号'  # 来源名称
        follow_num = re.findall('follow_num.*?:\"(.*?)\",', html)[0] #关注数
        uk = re.findall('uk.*?:\"(.*?)\",', html)[0] #uk码
        biz = app_id+'/'+uk
        if int(fans_num) >= 10000:
            sql1='select biz from spider_user_info where biz="%s"'%biz
            cursor=self.tools.sqll(sql1)
            result=cursor.fetchall()
            if not result:
                sql2='insert into spider_user_info(author,home_url,fans_num,avatar_url,source_name,brief,biz,create_time) values("%s","%s","%s","%s","%s","%s","%s","%s")'%(author,home_url,fans_num,avatar_url,source_name,brief,biz,create_time)
                self.tools.sqll(sql2)
                print(author, home_url, fans_num, avatar_url, source_name, brief, biz, create_time, follow_num, uk)
            else:
                pass


if __name__ == '__main__':
    baijia_1=baijia_1()
    tools = tool()
    list_=tools.list_()
    for i in list_:
        for j in range(0,10):
            urls=baijia_1.get_author(i,j)
            for url in urls:
                app_id=baijia_1.get_id(url)
                html=baijia_1.homepage(app_id)
                baijia_1.parse(html)











