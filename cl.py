import requests

#res = requests.get('http://127.0.0.1:5000/find_post?city=shenzhen')
res = requests.post('http://127.0.0.1:5000/addition',json={'a':1,'b':2})
print(res.json())