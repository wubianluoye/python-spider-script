## 二、某趣阁多线程小爬虫(requests + bs4 + threadpool + os + re)

爬取小说，合并小说。

- 遇到到的一些问题：
  - requests请求数据回来的文件编码，通过给encode='utf8'解决。
  - 文件名特殊符号导致下载失败，通过re模块的sub函数替换为空解决。
  - os.listdir读回来的列表乱序，导致后面合并文件排序问题，通过sort的排序方式(key)传入lambda函数解决。
  - 判断文件夹是否存在os.path.exists，通过os.makedirs创建深层文件夹

## Project setup
```
pip install requests threadpool beautifulsoup4
```

## Project run
```
python xbiquge.py
```

## 一、某点月票排行小爬虫(requests + bs4 + xlwt)

爬取月票排行榜默认前200条数据，并导出为excel。
也可通过total值改变要爬取的总数

## Project setup
```
pip install requests beautifulsoup4 xlwt
```

## Project run
```
python qidianTop.py
```

- 纯属练手，请勿乱用！