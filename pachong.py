# 使用import导入requests模块
import requests

# 从bs4中导入BeautifulSoup
from bs4 import BeautifulSoup

# 使用import导入jieba模块
import jieba

# 从pyecharts.charts中导入WordCloud模块
from pyecharts.charts import WordCloud

# ============================================================
# ⚠️ 使用前请先获取豆瓣Cookie，步骤：
# 1. 用Chrome浏览器打开: https://movie.douban.com/subject/36246195/comments?status=P
# 2. 如果未登录，先登录豆瓣账号
# 3. 按 F12 打开开发者工具 → 点击「Application」标签 → 左侧「Cookies」
# 4. 找到 movie.douban.com，复制下面两个值填到这里:
# ============================================================
YOUR_DBCL2 = "你的dbcl2的值"   # ← 把这里的字符串替换掉
YOUR_BID   = "你的bid的值"     # ← 把这里的字符串替换掉
# ============================================================

# 将豆瓣电影评论URL地址，赋值给变量url
url = "想要爬取网评的网址"

# 将User-Agent以字典键对形式赋值给headers
headers = {
    "User-Agent": "浏览器的User-Agent值",
    "Cookie": f"dbcl2={YOUR_DBCL2}; bid={YOUR_BID}",
}

# 将 url 和 headers参数，添加进requests.get()中，给赋值给response
response = requests.get(url, headers=headers, timeout=10)

# 将服务器响应内容转换为字符串形式，赋值给html
html = response.text

# 使用BeautifulSoup()传入变量html和解析器lxml，赋值给soup
soup = BeautifulSoup(html, "lxml")

# 使用find_all()查询soup中class="short"的节点，赋值给content_all
content_all = soup.find_all(class_="short")

# 创建一个空白列表wordList
wordList = []

# for循环遍历content_all
for content in content_all:

    # 获取每个节点中标签内容，赋值给contentString
    contentString = content.string

    # 使用jieba.lcut()将contentString进行分词，赋值给words
    words = jieba.lcut(contentString)

    # 将列表wordList和列表words进行累加
    wordList = wordList + words

# 创建一个空白字典wordDict
wordDict = {}

# for循环遍历列表wordList
for word in wordList:

    # 判断为这几个词语时
    if word == ".." or word == "......":
        # 继续下次循环
        continue

    # 如果列表中的元素长度大于1
    if len(word) > 1:
        # 如果该元素不存在字典的键中
        if word not in wordDict.keys():
            # 将字典中键所对应的值设置为1
            wordDict[word] = 1
        # 否则
        else:
            # 将字典中键所对应的值累加
            wordDict[word] = wordDict[word] + 1

# 创建WordCloud对象，赋值给wordCloud
wordCloud = WordCloud()

# 使用add()函数，series_name的值设置为空
# data_pair的值为字典wordDict转换成由元组组成的列表；
# 将word_size_range的值设置为[20,80]。
wordCloud.add(series_name = "", data_pair = wordDict.items(), word_size_range = [20,80])

# 使用wordCloud.render()存储文件，设置文件名为wordcloud.html
wordCloud.render("wordcloud.html")

# 使用print输出 success
print("success")