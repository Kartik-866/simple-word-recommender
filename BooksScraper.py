from bs4 import BeautifulSoup
import requests
import urllib.request as ur
from threading import Thread
from os import mkdir



def downloadBook(url):
	try:
		mkdir('NLPBooks')
	except FileExistsError:
		pass

	global count
	if '/ebooks/' in str(url):
		name = str(url).split('">')[1].split('<')[0]
		sub_url = HOME + str(url).split('"')[1]

		sub_r = requests.get(sub_url)
		sub_soup = BeautifulSoup(sub_r.content, 'html5lib')
		sub_urls = sub_soup.findAll('a', attrs={'type': 'text/plain; charset=utf-8'})

		if len(sub_urls) == 1:
			download_link = HOME + str(sub_urls[0]).split('href="')[1].split('"')[0]
			ur.urlretrieve(download_link, 'NLPBooks/' + name + '.txt')
		print(count, '. Downloaded ', name, sep='')
		count += 1


count = 1
URL = 'https://www.gutenberg.org/browse/scores/top'
HOME = 'https://www.gutenberg.org'
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')
urls = soup.findAll('li')

print('Request Done')

threads = []
for url in urls:
	threads.append(Thread(target=downloadBook, args=[url]))

for thread in threads:
	thread.start()
	thread.join()
