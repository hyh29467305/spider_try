import re
from bs4 import BeautifulSoup
import requests
s = requests.Session()
url_login = 'https://accounts.douban.com/passport/login'
url_contacts = 'https://accounts.douban.com/people/****/contacts'
formdata = {
    'redir':'https://accounts.douban.com',
    'form_email':'t.t.panda@hotmail.com',
    'form_password':'',
    'login':u'登录'
}
headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'}
r = requests.post(url_login,data=formdata,headers=headers)
content = r.text
soup = BeautifulSoup(content,'html5lib')
captcha = soup.find('img',id='captcha_image')
if captcha:
    captcha_url = captcha['src']
    re_captcha_id = r'<input type="hidden" name="captcha-id" value="(*?)"'
    captcha_id = re.findall(re_captcha_id,content)
    print(captcha_id)
    print(captcha_url)
    captcha_text = input("Please input the captcha")
    formdata['captcha_solution'] = captcha_text
    formdata['captcha_id'] = captcha_id
    r = s.post(url_login,data=formdata,headers=headers)
r = s.get(url_contacts)
with open('contacts.txt','w+',encoding='utf-8') as f:
    f.write(r.content)