import os
import requests
import json
import datetime
from bs4 import BeautifulSoup

appID = "wxacbaeae369c406a8"
appSecret = "a4fd030851a3ce115c932e44ed43fa2c"
openId = "o4i936tLt4YVADlUoffmiYBk7Zyk"
boxoffice_template_id = "cHJ5FRS09CMlsP_4tqUxUW2oRd5gRCMPxHstFEzHBuk"

def get_box_office(url):
    resp = requests.get(url)
    text = resp.content.decode("utf-8")
    soup = BeautifulSoup(text, 'html5lib')
    
    # 提取电影名称
    movie_name_data = soup.find("meta", {"name": "title"})
    movie_name = movie_name_data["content"] if movie_name_data else "No movie name found."
    
    # 提取所有票房数据
    box_office_elements = soup.find_all("span", class_="money")
    box_office_data = [element.text for element in box_office_elements] if box_office_elements else "No box office data found."
    
    # 返回电影名称和票房数据
    return movie_name, box_office_data
    print(box_office_data.text)

def get_access_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(appID.strip(), appSecret.strip())
    response = requests.get(url).json()
    access_token = response.get('access_token')
    return access_token

def send_box_office(access_token, movie_name, box_office):
    today = datetime.date.today()
    today_str = today.strftime("%Y年%m月%d日")
    body = {
        "touser": openId.strip(),
        "template_id": boxoffice_template_id.strip(),
        "url": "https://weixin.qq.com",
        "data": {
            "date": {
                "value": today_str
            },
            "moviename": {
                "value": movie_name
            },
            "boxoffice": {
                "value": box_office # 假设box_office是一个字符串
            }
        }
    }
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)
    response = requests.post(url, json.dumps(body, ensure_ascii=False).encode('utf-8'))
    print(response.text)

def box_office_report(url):
    access_token = get_access_token()
    movie_name, box_office_data = get_box_office(url)
    if isinstance(box_office_data, list) and box_office_data:
        # 发送第一个票房数据作为示例
        send_box_office(access_token, movie_name, box_office_data[2])
    else:
        print("未找到票房数据。")

# 示例用法
url = "https://www.boxofficemojo.com/title/tt15239678/?ref_=bo_se_r_3"
box_office_report(url)
