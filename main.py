'''
Created on Nov 27, 2012

@author: user
'''

import time

if __name__ == '__main__':
    pass

def get_page(url):
        
    try:
        if url == "http://www.udacity.com/cs101x/index.html":
            return  '<html> <body> This is a test page for learning to crawl! <p> It is a good idea to  learn to crawl before you try to  walk or  fly. </p> </body> </html> '
        elif url == "http://www.udacity.com/cs101x/crawling.html":
            return  '<html> <body> I have not learned to crawl yet, but I am quite good at  kicking. </body> </html>'
        elif url == "http://www.udacity.com/cs101x/walking.html":
            return '<html> <body> I cant get enough  crawling! </body> </html>'
        elif url == "http://www.udacity.com/cs101x/flying.html":
            return '<html> <body> The magic words are Squeamish Ossifrage! </body> </html>'
        else:
            import urllib
            return urllib.urlopen(url).read()
    except:
        return ""
    return ""

def get_next_target(s):
    start_link = s.find('<a href=')
    if start_link==-1: return None,0
    start_quote = s.find('"',start_link)
    end_quote = s.find('"',start_quote+1)
    url = s[start_quote+1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

def record_user_click(index,keyword,url):
    for entry in index:
        if entry[0] == keyword:
            for urlEntry in entry[1]:
                if urlEntry[0] == url:
                    urlEntry[1] += 1

def add_to_index(index, keyword, url):
    for entry in index:
        if entry[0] == keyword:
            for urlEntry in entry[1]:
                if url == urlEntry[0]:
                    return
            entry[1].append([url,0])
            return
    # not found, add new keyword to index
    index.append([keyword, [[url,0]]])
    
def lookup(index,keyword):
    for entry in index:
        if entry[0]==keyword:
            return entry[1]
    return []
    
def add_page_to_index(index, url, content):
    words = content.split()
    for word in words: add_to_index(index,word,url) #better idea to remove repeats from words
    
def crawl_web(seed):
    tocrawl=[seed]
    crawled = []
    index=[]
    while tocrawl:
        page = tocrawl.pop() # Depth crawl
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index,page,content)
            union(tocrawl,get_all_links(content))
            crawled.append(page)
    return index

def time_execution(code):
    start = time.clock()
    result = eval(code)
    run_time = time.clock()-start
    return result, run_time

def spin_loop(n):
    i = 0
    while i<n:
        i+=1
        
print time_execution('spin_loop(10**7)')[1]