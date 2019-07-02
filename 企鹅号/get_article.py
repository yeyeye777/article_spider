import json
import re
import requests
import os
import time
from bs4 import BeautifulSoup

from concurrent.futures import ThreadPoolExecutor,as_completed,ProcessPoolExecutor
import jsonpath
"""

"""

class qiehao_2():
    tools = tool()
    headers = tools.headers()
    dict_ = tools.dict_()



    def checksql(self):     # 检查没有爬取过文章的作者信息2
        # sql1='select * from spider_user_info where status = 0 and source_name = "企鹅号" and fans_num>500 order by fans_num desc limit 0,1 '
        sql1 = 'select * from spider_user_info where status = 2 and source_name = "企鹅号"'
        cursor = self.tools.sqll(sql1)
        result = cursor.fetchall()
        info=result[0]
        return info
    def get_articles(self,ids):
        try:
            ids=str(ids).replace(']','').replace('[','').replace("'",'').replace(' ','')
            url = 'https://r.inews.qq.com/getSubNewsListItems?ids={}&appver=25_android_5.8.12&devid=44ce3651532c37f9&qn-sig=0b59fd561bfbad40747db5fea582b5af&qn-rid=f4af5a1d-34c1-44dd-aa04-c31b470c03b4'.format(ids)
            response=requests.get(url)
            datas=json.loads(response.text)['newslist']
        except:
            datas=[]
        return datas


    def article(self,info): #获取100篇文章id
        author_id = info['biz'].replace('qiehao',"")
        ids=[]
        try:
            url = 'https://r.inews.qq.com/getSubNewsIndex?chlid={}'.format(author_id)
            response = requests.get(url=url)
            nums = json.loads(response.text)['ids']
            if len(nums)>=100:
                for i in range(100):
                    ids.append(nums[i]['id'])

            else:
                for i in range(len(nums)):
                    ids.append(nums[i]['id'])
            return ids
        except:
            ids=[]
            return ids


    def content(self,article_id,comment_id):#文章获取
        content_replys = []
        url = 'https://r.inews.qq.com/getQQNewsComment?article_id={}&byaid=0&comment_id={}'.format(article_id,comment_id)
        try:
            response = requests.get(url=url)
            comments = json.loads(response.text)['comments']['new']
            if len(comments) >= 100:
                for i in range(100):
                    content_reply = {
                        'content': comments[i][0]['reply_content']
                    }
                    content_replys.append(content_reply)
                return content_replys
            else:
                for comment in comments:
                    content_reply = {
                        'content': comment[0]['reply_content']
                    }
                    content_replys.append(content_reply)
                return content_replys
        except:
            content_replys = None
            return content_replys

    def parse(self,info):
        ids=self.article(info)
        print(ids)
        if len(ids)==0:
            pass
        else:
            datas=self.get_articles(ids)
            return datas

    def parse_2(self,data):
        try:
            article ={}
            article['read_num'] =data['forbidShowReadCount']
            article['author']=info['author']
            article['avatar_url']=info['avatar_url']
            article['title']= data['title']
            article['source_url'] = data['url']
            article['source_name'] = '企鹅号'
            article['img_url'] = data['thumbnails_qqnews'][0]
            article['published_time'] =data['time']
            article["author_info"] = {
                    "biz":info['biz'].replace('qiehao',''),  # bizID
                    "brief":self.utils.filter_emoji(info['brief']) # 摘要信息
            }
            comment_id=data['commentid']
            article_id=data['id']
            content_replys = self.content(article_id,comment_id)
            article['content_reply'] = content_replys
            
            print(article)
        except Exception as e:
            print(e)

    


if __name__ == '__main__':
    qiehao_2 = qiehao_2()
    tools = tool()
    while True:
        info = qiehao_2.checksql()
        datas = qiehao_2.parse(info)
        if datas == None:
            biz = info['biz']
            sql3 = 'update spider_user_info set status=3 where biz="%s"' % biz
            tools.sqll(sql3)
            pass
        else:
            biz = info['biz']
            sql2 = 'update spider_user_info set status=4 where biz="%s"' % biz
            tools.sqll(sql2)
            with ThreadPoolExecutor(max_workers=2) as thread_pool:
                task_list = [thread_pool.submit(qiehao_2.parse_2, data) for data in datas]
                for item in as_completed(task_list):
                    print(item.result())


