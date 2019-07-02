import json
import re
import requests
import os
import time
from uitls import tool
from concurrent.futures import ThreadPoolExecutor,as_completed,ProcessPoolExecutor

"""

"""

class souhu_2():
    tools = tool()
    dict_ = tools.dict_()



    def checksql(self):     # 检查没有爬取过文章的作者信息2
        sql1='select * from spider_user_info where status = 0 and source_name = "搜狐号" limit 0,1 '
        cursor = self.tools.sqll(sql1)
        result = cursor.fetchall()
        info=result[0]
        return info

    def article(self,info): #获取100篇文章文章的页面
        author_id = info['biz'].replace('souhu',"")
        datas=[]
        try:
            for i in range(1,6):
                url = 'https://v2.sohu.com/author-page-api/author-articles/wap/{}?pNo={}'.format(author_id,i)
                response = requests.get(url=url)
                data = json.loads(response.text)['data']['wapArticleVOS']
                datas.extend(data)
            return datas
        except:
            return datas

    def read_num(self, article_id):  # 获取点赞量和阅读量
        url = 'https://v2.sohu.com/author-page-api/articles/pv?articleIds={}'.format(article_id)
        response = requests.get(url=url)
        num = json.loads(response.text)[str(article_id)]
        return num

    def content(self,article_id):
        content_replys = []
        url = 'https://api.interaction.sohu.com/api/comments/maincomments?source_id=mp_{}&page_no=1&page_size=10&reply_count=10&type=0'.format(article_id)
        try:
            response = requests.get(url=url)
            comments = json.loads(response.text)
            for comment in comments:
                content_reply = {
                    'thumb_num': comment['displayStatus'],
                    'content': comment['content']
                }
                content_replys.append(content_reply)
            return content_replys
        except:
            content_replys= None
            return content_replys

    def parse(self,info):
        datas=self.article(info)
        if len(datas)==0:
            pass
        else:
            return datas

    def parse_2(self,data):
        article ={}
        try:
            article_id=data['id']
            num=self.read_num(article_id)
            article['read_num'] =num
            article['author']=info['author']
            article['avatar_url']=info['avatar_url']
            article['title']= data['title']
            article['source_url'] = "https://"+data['link']
            article['source_name'] = '搜狐号'
            article['baidu_url']= "https://"+data['link']
            article['source_type'] = 'ai_writer'
            img_url = data['cover']
            if img_url.split('//')[0] == "http:":
                article['img_url'] = img_url
            else:
                article['img_url'] = 'http:' + img_url
            article['published_time'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(str(data['publicTime'])[:-3])))
            article["author_info"] = {
                    "biz":info['biz'].replace('souhu',''),  # bizID
                    "brief":self.utils.filter_emoji(info['brief']) # 摘要信息
            }
            content_replys=self.content(str(article_id))
            article['content_reply'] = content_replys
            print(article)
            
        except:
            pass




if __name__ == '__main__':
    souhu_2 = souhu_2()
    tools = tool()
    while True:
        info = souhu_2.checksql()
        datas = souhu_2.parse(info)
        if datas == None:
            biz = info['biz']
            sql3 = 'update spider_user_info set status=3 where biz="%s"' % biz
            tools.sqll(sql3)
            pass
        else:
            biz = info['biz']
            sql2 = 'update spider_user_info set status=2 where biz="%s"' % biz
            tools.sqll(sql2)
            with ThreadPoolExecutor(max_workers=10) as thread_pool:
                task_list = [thread_pool.submit(souhu_2.parse_2, data) for data in datas]
                for item in as_completed(task_list):
                    print(item.result())


