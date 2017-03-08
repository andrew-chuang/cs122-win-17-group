import threading
import urllib3
import time

pm = urllib3.PoolManager()

start = time.time()
urls = ["http://www.google.com", "http://www.apple.com", "http://www.microsoft.com", "http://www.amazon.com", "http://www.facebook.com"]

def fetch_url(url):
    urlHandler = pm.urlopen(url=url, method='GET')
    html = urlHandler.read()
    #print "'%s\' fetched in %ss" % (url, (time.time() - start))

threads = [threading.Thread(target=fetch_url, args=(url,)) for url in urls]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()


#print "Elapsed Time: %s" % (time.time() - start)


'''
import threading, urllib3
import queue

urls_to_load = [
'http://stackoverflow.com/',
'http://slashdot.org/',
'http://www.archive.org/',
'http://www.yahoo.co.jp/',
]

def read_url(url, queue):
    data = urllib2.urlopen(url).read()
    print('Fetched %s from %s' % (len(data), url))
    queue.put(data)

def fetch_parallel():
    result = Queue.queue()
    threads = [threading.Thread(target=read_url, args = (url,result)) for url in urls_to_load]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return result

def fetch_sequencial():
    result = Queue.queue()
    for url in urls_to_load:
        read_url(url,result)
    return result

    
from threading import Thread
import urllib3
from time import time, sleep
from queue import Queue

pm = urllib3.PoolManager()


WORKERS=10
urls = ['http://docs.python.org/library/threading.html',
        'http://docs.python.org/library/thread.html',
        'http://docs.python.org/library/multiprocessing.html',
        'http://docs.python.org/howto/urllib2.html']*10
results = [None]*len(urls)

def worker():
    while True:
        i, url = q.get()
        # print "requesting ", i, url       # if you want to see what's going on
        results[i]=pm.urlopen(url=url, method='GET').data
        q.task_done()

start = time()
q = Queue()
for i in range(WORKERS):
    t=Thread(target=worker)
    t.daemon = True
    t.start()

for i,url in enumerate(urls):
    q.put((i,url))
q.join()
'''
