# 使用import导入requests模块
import requests
import re

# 使用from..import从bs4模块导入BeautifulSoup
from bs4 import BeautifulSoup

# 将User-Agent以字典键对形式赋值给headers
headers = {"User-Agent": "你的浏览器User-Agent值"}
    
# 使用for循环遍历range()函数生成的0-1的数字
for i in range(0, 2):

    # 取遍历中的每个数和25相乘计算每页的数值，并赋值给page
    page = i * 25

    # 用"https://movie.douban.com/top250?start="和page转换成的字符串格式相连，接着连上"&filter="，并赋值给url
    url = "https://movie.douban.com/top250?start=" + str(page) + "&filter="

    # 将字典headers传递给headers参数，添加进requests.get()中，赋值给response
    response = requests.get(url, headers=headers)

    # 将服务器响应内容转换为字符串形式，赋值给html
    html = response.text

    # 使用BeautifulSoup()传入变量html和解析器lxml，赋值给soup
    soup = BeautifulSoup(html, "lxml")

    # 使用find_all()查询soup中class="pic"的节点，赋值给content_all
    content_all = soup.find_all(class_="pic")

    # for循环遍历content_all
    for content in content_all:

        # 使用find()查询content中的img标签，并赋值给imgContent
        imgContent = content.find(name="img")

        # 使用.attrs获取alt对应的属性值，并赋值给imgName
        imgName = imgContent.attrs["alt"]
        # 去除文件名中的非法字符（Windows不允许 \ / : * ? " < > |）
        imgName = re.sub(r'[\\/:*?"<>|]', '', imgName).strip()

        # 使用.attrs获取src对应的属性值，并赋值给imgUrl
        imgUrl = imgContent.attrs["src"]

        # 使用replace()函数将链接中的s_ratio_poster替换成m，并赋值给imgUrlHd
        imgUrlHd = imgUrl.replace("s_ratio_poster", "m")

        # 将链接添加进requests.get()中，赋值给imgResponse
        # 添加Referer和User-Agent请求头，绕过豆瓣防盗链机制
        img_headers = {
            "User-Agent": headers["User-Agent"],
            "Referer": "https://movie.douban.com/"
        }
        imgResponse = requests.get(imgUrlHd, headers=img_headers, timeout=15)

        # 检查响应状态码，确认图片下载成功
        if imgResponse.status_code != 200:
            print(f"下载失败：{imgName}，状态码：{imgResponse.status_code}")
            continue

        # 使用.content属性将响应消息转换成图片数据，赋值给img
        img = imgResponse.content

        # 通过文件头魔数验证下载内容是否真的是图片，并确定真实格式
        # JPEG: FF D8 FF, PNG: 89 50 4E 47, WebP: 52 49 46 46 (RIFF), GIF: 47 49 46 38
        if len(img) < 100:
            print(f"下载失败：{imgName}，文件太小")
            continue
        if img[:3] == b'\xff\xd8\xff':
            ext = "jpg"
        elif img[:4] == b'\x89PNG':
            ext = "png"
        elif img[:4] == b'RIFF' and img[8:12] == b'WEBP':
            ext = "webp"
        elif img[:3] == b'GIF':
            ext = "gif"
        else:
            print(f"下载失败：{imgName}，无法识别格式")
            continue

        # 使用with语句配合open()函数以图片写入的方式打开文件
        # 用格式化将图片名字和正确的扩展名组合
        # 打开的文件赋值为f
        with open(f"\\你的路径\\{imgName}.{ext}", "wb") as f:
            # 使用write()将图片写入
            f.write(img)
            print(f"下载成功：{imgName}.{ext}")