import requests
import re,time,json
from uitls import tool


"""
本模块任务是爬取拥有大于10000粉丝数的作者他所关注的人的信息，因为他所关注的人的质量会更高。
目标还是获取大量的作者信息

"""

class baijia_2():
    tools = tool()
    headers = tools.headers()
    dict_ = tools.dict_()
    browser = tools.browser()


    def checksql(self): #通过判断status的数值判断书否已经爬取过这个人的关注的人
        sql1='select biz from spider_user_info where status = 0 and source_name = "百家号" limit 0,1 '
        cursor = self.tools.sqll(sql1)
        result = cursor.fetchall()
        biz=result[0]['biz']
        uk=biz.split('/')[1]
        sql2='update spider_user_info set status=1 where biz="%s"' % biz
        self.tools.sqll(sql2)
        return uk


    def response(self,id):  #获取这个人的关注的好友列表页面源码
        for i in self.dict_:
            self.browser.add_cookie({
                'name': i,
                'value': self.dict_[i],
            })
        if id.isdigit():
            url = 'https://author.baidu.com/profile?context={%22from%22:%22dusite_sresults%22,%22app_id%22:%22' + id + '%22}&cmdType=&pagelets[]=root&reqID=0&ispeed=1'
        else:
            url = 'https://author.baidu.com/profile?context={%22from%22:%22dusite_sresults%22,%22uk%22:%22' + id + '%22}&cmdType=&pagelets[]=root&reqID=0&ispeed=1'
        try:
            self.browser.get(url)
        except:
            pass
        html = self.browser.page_source
        return html


    def fans(self,uk):  # 获取关注的信息
        ids=[]
        try:
            url = 'https://mbd.baidu.com/webpage?action=personaljumpsublist&type=subscribe&uk={}'.format(uk)
            response = requests.get(url=url)
            response.encoding = 'utf-8'
            html = response.text
            datas = json.loads(html)
            follows = datas['data']['follow_list']['modify']
            for follow in follows:
                id = follow['third_id']
                ids.append(id)
            return ids
        except Exception as e:
            print(e)
            return ids


    def parse(self,id):  # 解析他所关注的人的个人信息，并检查是否存在于数据库，不存在插入
        html=self.response(id)
        try:
            html = html.replace("\\", "")
            author = re.findall('display_name\":\"(.*?)\"', html)[0].encode("gb18030", "ignore").decode("utf8","ignore").replace("\\", "")  # 用户昵称
            third_id=re.findall('third_id\":\"(.*?)",', html)[0]
            home_url = 'https://author.baidu.com/home/' + third_id  # 用户主页地址
            avatar_url = re.findall('avatar_raw\":\"(.*?)",', html)[0]  # 用户头像地址
            brief = str(re.findall('sign\":\"(.*?)\",', html)[0]).encode("gb18030", "ignore").decode("utf8","ignore").replace("\\","")  # 作者简介
            fans_num = re.findall('fans_num.*?:\"(.*?)\",', html)[0]  # 粉丝数量
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 创建时间
            source_name = '百家号'  # 来源名称
            follow_num = re.findall('follow_num.*?:\"(.*?)\",', html)[0]  # 关注数
            uk = re.findall('uk.*?:\"(.*?)\",', html)[0]  # uk码
            biz = third_id + '/' + uk
            if int(fans_num) >= 10000:
                sql3='select biz from spider_user_info where biz="%s"' % biz
                cursor = self.tools.sqll(sql3)
                result = cursor.fetchall()
                if not result:
                    sql4='insert into spider_user_info(author,home_url,fans_num,avatar_url,source_name,brief,biz,create_time) values("%s","%s","%s","%s","%s","%s","%s","%s")' % (
                        author, home_url, fans_num, avatar_url, source_name, brief, biz, create_time)
                    self.tools.sqll(sql4)
                    print(author, home_url, third_id, fans_num, avatar_url, source_name, brief, biz, create_time,follow_num, uk)
                else:
                    pass

        except Exception as e:
            print(e)


if __name__ == '__main__':
    baijia_2 = baijia_2()
    while True:
        uk=baijia_2.checksql()
        ids=baijia_2.fans(uk)
        if len(ids)==0:
            continue
        else:
            for id in ids:
                baijia_2.parse(str(id))
