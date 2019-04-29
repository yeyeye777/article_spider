import json
import re
import requests
import os
import time
from uitls import tool


"""
本模块的作用是爬取作者的文章，由于没有返回最大的文章数量字段，所以这个地方我按照100篇
文章进行爬取，如果不够，他会取实际的文章量，还有评论字段，点赞字段，阅读量等，具体页面
数据没有爬取，有url。
"""

class baijia_3():
    tools = tool()
    headers = tools.headers()
    dict_ = tools.dict_()
    browser = tools.browser()


    def checksql(self): #检查没有爬取过文章的作者信息
        sql1='select * from spider_user_info where status = 1 and source_name = "百家号" limit 0,1 '
        cursor = self.tools.sqll(sql1)
        result = cursor.fetchall()
        info=result[0]
        return info


    def article(self,info): #获取100篇文章文章的页面
        uk = info['biz'].split('/')[1]
        for i in self.dict_:
            self.browser.add_cookie({
                'name': i,
                'value': self.dict_[i],
            })
        url = 'https://author.baidu.com/list?type=article&tab=2&uk={}&num=100'.format(uk)
        try:
            self.browser.get(url)
        except:
            pass
        html = self.browser.page_source
        return html,uk


    def read_point(self,dynamic,thread,uk): #获取点赞量和阅读量
        bian = '%5b%7b%22user_type%22%3a%223%22%2c%22dynamic_id%22%3a%22{}%22%2c%22dynamic_type%22%3a%222%22%2c%22dynamic_sub_type%22%3a%222001%22%2c%22thread_id%22%3a%22{}%22%2c%22feed_id%22%3a%22{}%22%7d%5d'.format(
            dynamic, thread, dynamic)
        response = requests.get(
            'https://mbd.baidu.com/webpage?type=homepage&action=interact&format=jsonp&params={}&uk={}'.format(bian, uk),
            timeout=10)
        nums = json.loads(response.text.replace('callback(', '').replace(')', ''))['data']['user_list']
        return nums


    def content(self,thread): #获取评论数
        comment_url = 'https://ext.baidu.com/api/comment/v1/comment/getlist?appid=101&start=0&num=10&thread_id={}'.format(
            thread)
        try:
            r1 = requests.get(url=comment_url, timeout=10)
            comments = json.loads(r1.text)['ret']['list']
            content_replys = []
            if len(comments)>=10:
                for i in range(10):
                    content_reply = {
                        'thumb_num': comments[i]['like_count'],
                        'content': comments[i]['content']
                    }
                    content_replys.append(content_reply)
                return content_replys
            else:
                for comment in comments:
                    content_reply = {
                        'thumb_num': comment['like_count'],
                        'content': comment['content']
                    }
                    content_replys.append(content_reply)
                return content_replys
        except:
            content_replys= None
            return content_replys




    def parse(self,info):
        html,uk=self.article(info)
        articles=[]
        try:
            new=json.loads(re.findall('.*">(.*?)<',html)[0])
            datas=new['data']['list']
            for data in datas:
                article ={}
                try:
                    dynamic=data['dataAttrs']['dynamic-id']
                    thread=data['dataAttrs']['thread-id']
                    nums=self.read_point(dynamic,thread,uk)
                    article['reply_num']=tuple(nums.values())[0]['comment_num']  #评价数
                    article['read_num']=tuple(nums.values())[0]['read_num']  #阅读量
                    article['thumb_num'] = tuple(nums.values())[0]['praise_num']  # 点赞数
                    article['author']=info['author']  # 作者
                    article['avatar_url']=info['avatar_url']  # 头像
                    article['title']= data['title']  # 文章标题
                    article['source_url'] = data['url']  # 文章链接
                    article['source_name'] = '百家号'
                    article['img_url'] = data['cover_images'][0]['src'] #文章图片，有三张取第一个
                    article['published_time'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(data['publish_at'])) #创作时间
                    article["author_info"] = {
                            "biz":info['biz'],  # bizID
                            "fans_num":info['fans_num'], # 粉丝数量
                            "brief":(info['brief']) # 摘要信息
                    }
                    content_replys=self.content(thread)
                    article['content_reply'] = content_replys #评价信息
                    print(article)
                    articles.append(article)
                except:
                    pass
            biz = info['biz']
            sql2 = 'update spider_user_info set status=2 where biz="%s"' % biz
            self.tools.sqll(sql2)
            return articles
        except Exception as e:
            print(e)
            biz = info['biz']
            sql3 = 'update spider_user_info set status=3 where biz="%s"' % biz
            self.tools.sqll(sql3)
            return  articles




if __name__ == '__main__':
    while True:
        baijia_3=baijia_3()
        info=baijia_3.checksql()
        articles=baijia_3.parse(info)
        if len(articles)==0:
            continue
        else:
            for article in articles:
                baijia_3.parse_detail(article)






