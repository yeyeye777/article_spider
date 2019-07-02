import pymysql
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class tool(object):
    def list_(self):#类目列表
        list_ = ["生活", "情感", "教育", "科研", "美食", "旅行", "政治", "军事", "金融", "经济", "文化", "设计", "科技"
            , "数码", "游戏", "动漫", "自然", "三农", "房地产", "汽车", "健康", "时尚", "体育", "影视", "娱乐", "艺术"]
        return list_


    def dict_(self): #cookie信息
        dict_ = {
            "BAIDUCUID": "g8SKtgu0B8l_u2uNguHn8ga1SuY48Huc0avpigioSaizaB8fgO25i_uqvfYua2tHA",
            "BAIDUID": "93152B7B6EA7D252BE7FF1F22942C5505:FG=1",
            "BDORZ": "AE84CDB3A529C0F8A2B9DCDD1D18B695",
            "MBD_AT": "1555920950",
            "WISE_HIS_PM": "1",
            "fontsize": "1.0",
            "GID": "G1S2QXSERVKJMD5X6821O78AOQ1QJ4P3J8",
            "BAIDULOC": "13523058_3642420_65_289_1555928065154",
            "delPer": "0",
            "PSINO": "5",
            "H_WISE_SIDS": "130510_124622_110086_131021_123289_131093_127417_130611_131210_131264_131263_131257_128806",
        }
        return dict_


    def headers(self): #header头信息
        headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36",
        }
        return headers

    def data(self,keyword):
        data = {
            "keyword": keyword,
            "from": "0",
            "size": "100",
            "terminalType": "wap",
            "source": "wap-sohu",
            "searchType": "media",
        }
        return data

    def connection(self): #mysql数据库连接
        
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='123456',
                                     db='bai',
                                     charset='utf8')
        cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
        return connection,cursor


    def browser(self): #模拟浏览器
        browser = webdriver.Chrome('chromedriver.exe')
        url = 'http://www.baidu.com/'
        browser.get(url=url)
        url = 'https://author.baidu.com/home/1571262428373948?from=dusite_sresults'
        browser.get(url=url)
        browser.delete_all_cookies()
        return browser


    def sqll(self, sql=None): #执行sql语句
        connection, cursor=self.connection()
        cursor.execute(sql)
        connection.commit()
        return cursor


if __name__ == '__main__':
    tools=tool()
















