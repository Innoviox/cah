import requests as r
from urllib.request import urlretrieve as ur
from bs4 import BeautifulSoup
import os 

url = 'https://www.gocomics.com/calvinandhobbes/{}/{}/{}'
name = 'cah/{}/{}/{}.jpg'
y = '1995'
m = '1'
d = '1'

def fmat(s):
    return s.format(y, m.zfill(2), d.zfill(2))
    
'''
req = r.get(fmat(url))
print(req)
print(req.text)
bs = BeautifulSoup(req.text, 'html5lib')
div = bs.find('div', id='js-item-start')
print(div)
ur(div.attrs['data-image'], fmat(name))
'''

for i in range(500):
    try:
        f = '/'.join(fmat(name).split('/')[:-1])
        if not os.path.isdir(f):
            os.makedirs(f)
        #ur(BeautifulSoup(r.get(fmat(url)).text, 'html5lib').find('div', id='js-item-start').attrs['data-image'], fmat(name))
        ur(BeautifulSoup(r.get(fmat(url)).text, 'html5lib').find('picture', class_='item-comic-image').find('img').attrs['src'], fmat(name))
        print('saved to', fmat(name))
    except Exception as e:
        # raise e
        print(f'got {e}, trying a mod')
    finally:
        d = str(int(d) + 1)
        if int(d) > 31:
            d = '1'
            m = str(int(m) + 1)
            if int(m) > 12:
                m = '1'
                y = str(int(y) + 1)
