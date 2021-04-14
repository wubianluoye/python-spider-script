import requests
from bs4 import BeautifulSoup
import threadpool
import os
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 FS",
    "Referer": "http://www.xbiquge.la/modules/article/waps.php",
}

url = 'http://www.xbiquge.la/'

# 书名
fname = ''

#总樟树
total_len = 0

def init():
    qy = input('搜索:').strip()
    res = search(qy)

    # 未找到
    if len(res)==0:
        return print('未找到相关内容')
    # 返回结果
    print(f'已找到{len(res)}条：')

    # 搜索结果
    search_result(res)

def search(query):
    # 参数
    q = { 'searchkey': query }
    res = requests.post(url= url+'/modules/article/waps.php', data= q, headers= headers)
    res.encoding='utf8'
    html = BeautifulSoup(res.text, 'html.parser')

    # 获取搜索结果，第一行是表头，去除
    result = html.find('form',id="checkform").find_all('tr')[1:7]

    # 结果拼装
    rr = []
    for item in result:
        obj = {
            'name': item.find_all('td')[0].a.text,
            'author': item.find_all('td')[2].text,
            'href': item.find_all('td')[0].a['href']
        }
    rr.append(obj)

    return rr

def search_result(res):
    for item in res:
        print(f"{res.index(item)}.{item['name']} - {item['author']}")

    # 选择结果
    while(True):
        inp = input('请输入序号：').strip()
        if int(inp)>=0 and int(inp)<len(res):
            break
        else:
            print(f'请输入0 - {len(res)-1}(包含)的数字')
    
    # 文件夹名称获取
    global fname
    fname = res[int(inp)]['name']

    # 选择的书的url
    selectd_href = res[int(inp)]['href']

    # 获取章节信息
    get_book_list(selectd_href)

def get_book_list(href):
    res = requests.get(url = href, headers = headers)
    res.encoding='utf8'
    html = BeautifulSoup(res.text, 'html.parser')
    
    # 樟树
    lis = html.find('div', id="list").find_all('a')
    items = [{'url':url+item['href'],'title': f'{lis.index(item)} - {item.text}'} for item in lis ]

    # 获取总章数，搞个进度显示
    global total_len
    total_len = len(items)

    # 未找到
    if len(items)==0:
        return print('未找到章节内容')

    # 文件夹创建(书名文件夹)
    if(not os.path.exists(f'./files/{fname}')):
        # 深度递归创建文件makedirs , all is ok!
        # 当前创建mkdir,深度时，报错
        os.makedirs(f'./files/{fname}')

    get_item(items)

def get_item(arr):
    print('要开始下载了！')

    # 线程池
    pool = threadpool.ThreadPool(50)
    task_list = threadpool.makeRequests(save_file, arr)
    [pool.putRequest(item) for item in task_list]
    pool.wait()
    print('完成 all done!')

    while(True):
        n_to_1 =input('是否需要合并成一个txt文件？(y/n)').strip()
        if n_to_1=='y':
            merge_book()
            break
        elif n_to_1=='n':
            break
        else:
            print('无效输入，请输入y或n')

def save_file(items):
    res = requests.get(items['url'], headers= headers)
    res.encoding='utf8'
    html = BeautifulSoup(res.text,'html.parser')

    # 标题特殊字符清除
    title = items['title']
    reg = re.compile(r'[\\/:*?"<>|\0]+')
    # sub替换字符串
    title = re.sub(reg, '', title)

    # 内容获取
    content = html.find('div',id='content').text
    bbk = title+'\r\n'+content

    # 文件写入
    with open(f'./files/{fname}/{title}.txt', 'w', encoding='utf-8') as f:
        f.write(bbk)

    # 获取当前已下载数量
    dowloads = len(os.listdir(f'./files/{fname}'))
    if dowloads%100 == 0:
        pec = round(100 * (dowloads/total_len))
        print(f'已完成({pec}%)')

def merge_book():
    print('制作中，请稍后。。。')

    # 合并后的名字
    name = f'./files/{fname}-全本.txt'

    # 拿到所有文件
    flist = os.listdir(f'./files/{fname}')
    # 排序，不然会有['1','10','2','3']问题
    flist.sort(key=lambda x: int(x.split(' - ')[0]))

    # 合并
    for item in flist:
        fpath = f'./files/{fname}/{item}'
        with open(fpath, mode='r+', encoding='utf8') as f1, open(name, mode='a', encoding='utf8') as f2:
            content = f1.read()
            content = content + '\r\n'
            f2.write(content)

    print(f'合并完成!输出文件所在路径：{name}')

if __name__ == '__main__':
    init()
