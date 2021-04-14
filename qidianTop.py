# coding=utf-8

import requests
from bs4 import BeautifulSoup
import xlwt

total = 2 # 10(页) * 20(个) = 200条

config = {
    'url': 'https://www.qidian.com/rank/yuepiao',
    'headers': {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 FS"
    },
    'timeout': 30
}


def get_list(page=1, books=[{'name':'书名','author':'作者','href':'链接地址','update':'最近更新','date':'时间','status':'状态'}]):
    if not config['url']:
        return 'no url'

    req = requests.get(url = config['url'], params={'page': page}, headers = config['headers'],timeout = config['timeout'])
    req.encoding="utf8"

    print(f'当前请求地址: {req.request.url}, {len(books)}')

    # bs4转换
    html = BeautifulSoup(req.text,'html.parser')

    # 阈值判断
    if not html.find('div', class_='book-img-text').ul:
        print('下载完成')
        return books

    # 获取列表
    items = html.find('div', class_='book-img-text').ul.find_all('li')

    # 数据处理
    for i in items:
        tag_a = i.find('div', class_='book-mid-info').h4.a
        auth = i.find('div', class_='book-mid-info').find('p',class_="author")
        update = i.find('div', class_='book-mid-info').find('p',class_="update").a.text
        date = i.find('div', class_='book-mid-info').find('p',class_="update").span.text

        # 打包数据
        obj = {
            'name': tag_a.text,
            'author': auth.find('a',class_='name').text,
            'href': tag_a['href'],
            'update':update,
            'date': date,
            'status': auth.find('span').text,

        }
        books.append(obj)

    # 下载页数
    if(page >= total):
        return books

    page+=1
    items=''
    
    # 递归
    return get_list(page, books)


# 保存数据到excel
def save_file(arr):
    
    # 创建excel
    wb = xlwt.Workbook()
    ws = wb.add_sheet('完本统计')
    ws.col(0).width = 256 * 30
    ws.col(1).width = 256 * 20
    ws.col(2).width = 256 * 40
    ws.col(3).width = 256 * 40
    ws.col(4).width = 256 * 30

    # 数据写入
    for idx,item in enumerate(arr):
        for i,c in enumerate(item):
            ws.write(idx,i,item[c])

    # 保存
    wb.save(f'./起点排行top{20*total}.xls')
    print('完成！')


if __name__ == "__main__":
    end_list = get_list()
    save_file(end_list)