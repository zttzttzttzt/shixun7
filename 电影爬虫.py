# 导入BeautifulSoup库，用于网页解析
from bs4 import BeautifulSoup  # 网页解析，获取数据
# 导入正则表达式库，用于文字匹配
import re  # 正则表达式，进行文字匹配
# 导入用于制定URL和获取网页数据的库
import urllib.request, urllib.error  # 制定URL，获取网页数据
# 导入用于进行Excel操作的库
import xlwt  # 进行excel操作
# 定义正则表达式规则，用于匹配影片详情页链接、图片链接、影片中文名、评分等信息
findLink = re.compile(r'<a href="(.*?)">')  # 影片详情链接的规则
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)
# 定义主函数
def main():
    # 设置要爬取的网页链接
    baseurl = "https://movie.douban.com/top250?start="
    # 爬取网页数据
    datalist = getData(baseurl)
    # 设置保存路径
    savepath = "豆瓣电影Top250.xls"
    # 保存数据到Excel文件
    saveData(datalist, savepath)
# 定义爬取网页函数
def getData(baseurl):
    datalist = []  # 用来存储爬取的网页信息
    for i in range(0, 10):  # 调用获取页面信息的函数，10次
        url = baseurl + str(i * 25)
        html = askURL(url)  # 保存获取到的网页源码
        # 逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):  # 查找符合要求的字符串
            data = []  # 保存一部电影所有信息
            item = str(item)
            link = re.findall(findLink, item)[0]  # 通过正则表达式查找
            data.append(link)
            imgSrc = re.findall(findImgSrc, item)[0]
            # findall 返回匹配项的列表
            # [0] 用于获取第一个（在这种情况下是唯一的）匹配项
            # 提取的图片源存储在变量 imgSrc 中
            data.append(imgSrc)
            #将提取的电影图片源（imgSrc）追加到 data 列表中。
            titles = re.findall(findTitle, item)
            # 使用正则表达式模式 findTitle 查找并提取item 字符串中的电影标题（中文和外文）
            # re.findall 返回匹配项的列表

            # 处理电影的标题信息
            if len(titles) == 2:  # 检查提取的标题列表 titles 的长度是否为2。长度为二表示有中文标题和外文标题。
                ctitle = titles[0]  # 如果存在两个标题，将第一个标题（中文标题）存储在变量 ctitle 中。
                data.append(ctitle)  # 将中文标题添加到 data 列表中
                otitle = titles[1].replace("/", "")  # 消除转义字符：如果存在两个标题，将第二个标题（外文标题）存储在变量 otitle 中，并使用 replace("/", "") 去除可能包含的转义字符 "/”。
                data.append(otitle)  # 将外文标题添加到 data 列表中。
            else:  # 如果只存在一个标题，则执行这个分支。
                data.append(titles[0])  # 将唯一的标题添加到 data 列表中。
                data.append(' ')  # 添加一个空字符串到 data 列表中
            rating = re.findall(findRating, item)[0]  # 使用正则表达式模式 findRating 查找并提取 item 字符串中的电影评分
            data.append(rating)
            judgeNum = re.findall(findJudge, item)[0]  # 使用正则表达式模式 findJudge 查找并提取 item 字符串中的评价人数
            data.append(judgeNum)
            inq = re.findall(findInq, item)  # 使用正则表达式模式 findInq 查找并提取 item 字符串中的电影简介
            if len(inq) != 0:
                inq = inq[0].replace("。", "")
                data.append(inq)
            else:
                data.append(" ")
            bd = re.findall(findBd, item)[0]  # 使用正则表达式模式 findBd 查找并提取 item 字符串中的电影详细信息（概况或背景信息）
            bd = re.sub('<br(\s+)?/>(\s+)?', "", bd)  # 使用 re.sub 函数替换 bd 变量中的字符串。具体地，将匹配 <br> 标签及其可能的空格，用空字符串替换，即删除换行标签
            bd = re.sub('/', "", bd)  # 继续使用 re.sub 函数，将斜杠 "/" 用空字符串替换，即删除斜杠
            data.append(bd.strip())  #  添加处理后的电影详细信息（概况或背景信息）到 data 列表中，并使用 strip() 方法去除可能存在的额外空白
            datalist.append(data)
    return datalist # 返回一个2维列表 包含各个电影信息
# 获取指定URL的网页内容
def askURL(url):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html
# 保存数据到表格
def saveData(datalist, savepath):
    print("save.......")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)  # 创建工作表
    col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, 250):
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])  # 数据
    book.save(savepath)  # 保存
if __name__ == "__main__":  # 当程序执行时
    main()
    print("爬取完毕！")