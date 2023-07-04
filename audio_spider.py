import requests
import re
import json
import os


"""
根据bv号和自定义文件名得到filename、url、headers
    bv：视频bv号
    name：自己给待下载文件取的名字
"""


def bv_name(bv, name):
    if not os.path.exists("D:/video"):
        os.mkdir("D:/video")

    fileName = f"D:/video/{name}"
    URL = f'https://www.bilibili.com/video/{bv}'

    headers = {
        'referer': f'https://www.bilibili.com/video/{bv}?spm_id_from=333.337.search-card.all.click',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }

    return fileName, URL, headers


"""
获取网页源代码
    url：网页链接
    headers：请求头
"""


def send_request(url, headers):
    response = requests.get(url=url, headers=headers)
    return response


"""
解析视频数据
html_data：页面源代码，相当于上个函数response.text
"""


def get_video_data(html_data):
    # 提取视频对应的json数据
    # <script>window\.__playinfo__=(.*?)</script>是在网络上找的，随便百度都找的到
    json_data = re.findall('<script>window\.__playinfo__=(.*?)</script>', html_data)[0]
    json_data = json.loads(json_data)

    # 提取音频的url地址
    audio_url = json_data['data']['dash']['audio'][0]['backupUrl'][0]
    return audio_url


"""
下载音频
file_name：待下载文件地址
audio_url：音频文件在网页中的地址
headers：请求头
"""


def save_data(file_name, audio_url, headers):
    # 请求数据
    audio_data = send_request(audio_url, headers).content
    with open(file_name + '.mp3', mode='wb') as f:
        f.write(audio_data)
    # print("音频下载完毕！！！")


"""
测试使用，可以注释掉。GUI界面会调用之前的函数
"""
# if __name__ == '__main__':
#     filename, URL, headers = bv_name('BV1t14y1F7kd', '英文歌')
#     res = send_request(URL, headers).text
#     video = get_video_data(res)
#     print(video)
