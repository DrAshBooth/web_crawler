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
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]
    
def lookup(index,keyword):
    if keyword in index: return index[keyword]
    return None
    
def add_page_to_index(index, url, content):
    words = content.split()
    for word in words: add_to_index(index,word,url) #better idea to remove repeats from words
    
def crawl_web(seed):
    tocrawl=[seed]
    crawled = []
    index={}
    graph = {}
    while tocrawl:
        page = tocrawl.pop() # Depth crawl
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index,page,content)
            outlinks = get_all_links(content)
            graph[page]=outlinks
            union(tocrawl,outlinks)
            crawled.append(page)
    return index, graph

def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0/npages
    for i in range(numloops):
        newranks = {}
        for page in graph:
            newrank = (1.0-d)/npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank +d* ranks[node]/float(len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks

def lucky_search(index, ranks, keyword):
    result=''
    for elem in index:
        if elem == keyword:
            result = index[elem]
    best = 0
    site = None
    for elem in result:
        if ranks[elem] > best:
            best = ranks[elem]
            site = elem
    return site

def time_execution(code):
    start = time.clock()
    result = eval(code)
    run_time = time.clock()-start
    return result, run_time

###################################################################
####################### Hash table Stuff ##########################
###################################################################
        
def hash_string(keyword,buckets):
    tot = 0
    for c in keyword: tot = (tot + ord(c)) % buckets
    return tot%buckets

def make_hashtable(nbuckets):
    table = []
    for i in range(nbuckets): table.append([])
    return table

def hashtable_get_bucket(htable, keyword):
    return htable[hash_string(keyword,len(htable))]

def hashtable_lookup(htable,key):
    rtn = None
    for entry in hashtable_get_bucket(htable, key):
        if entry[0] == key: rtn = entry[1]
    return rtn

def hashtable_update(htable,key,value):
    found =False
    for entry in hashtable_get_bucket(htable, key):
        if entry[0] == key: 
            entry[1]=value
            found=True
    if found==False: hashtable_get_bucket(htable, key).append([key,value])
    return htable

###################################################################
###################################################################
###################################################################


def fibonacci(n):
    n2=0
    n1=1
    i=0
    while i<n:
        n2, n1 = n1,n1+n2
        i+=1
    return n2

    
def triangular(n):
    if n==1: return 1
    else: return n + triangular(n-1)

def get_next_tag(s):
    start_tag = s.find('<')
    if start_tag==-1: return None
    end_tag = s.find('>',start_tag+1)
    tag = s[start_tag:end_tag+1]
    return tag
    
def remove_tags(s):
    while True:
        tag = get_next_tag(s)
        if tag: s = s.replace(tag, " ")
        else: break
    return s.split()

def date_converter(dic,s):
    if s[1]=='/':
        month=int(s[0])
        if s[3]=='/':
            day=s[2]
            year = s[4:]
        else: 
            day = s[2:4]
            year = s[5:]
    else: 
        month=int(s[:2])
        if s[4]=='/':
            day=s[3]
            year = s[5:]
        else: 
            day = s[3:5]
            year = s[6:]
    return day + ' ' + dic[month] + ' ' + year

from copy import deepcopy

def is_list(p):
    return isinstance(p, list)

def deep_reverse(p):
    temp = deepcopy(p)   # stops inputted list from being mutated
    temp.reverse()       # reverses intital depth
    replace(temp) 
    return temp

def replace(p):
    if p == [] or is_list(p) == False:
        return []
    else:
        for i in range(0, len(p)):
            if is_list(p[i]) == True:
                p[i].reverse()         # reverses current depth
                replace(p[i])      # recursive loop until p == []    



def isColluding (targetNode,page,graph,k):
    toCrawl = [page]
    nextDepth = []
    while k:
        while toCrawl:
            tmpNode = toCrawl.pop()
            if tmpNode in graph: #if it is not in the graph, than it needs to be crawled
                for url in graph[tmpNode]:
                    if url == targetNode:
                        return True
                    else:
                        nextDepth.append(url)
        k-=1
        toCrawl = []+nextDepth
        nextDepth = []
    return False

#def compute_ranks(graph,k):
#    d = 0.8 
#    numloops = 10
#    ranks = {}
#    npages = len(graph)
#    for page in graph:
#        ranks[page] = 1.0 / npages
#    for i in range(0, numloops):
#        newranks = {}
#        for page in graph:
#            s = 0
#            #newrank = (1 - d) / npages
#            for node in graph:
#                if page in graph[node]:
#                    if page != node and not isColluding(node,page,graph,k):
#                        s += (ranks[node]/len(graph[node]))
#                        #newrank = newrank + d * (ranks[node]/len(graph[node]))
#            newranks[page] = (1 - d) / npages + d*s
#            #newranks[page] = newrank
#        ranks = newranks
#    return ranks

def get_transformation(compare_set,patterns):
    for entry in patterns:
        if entry[0] == compare_set:
            return entry[1]

def cellular_automaton(string, pattern, generations):
    patterns = [ ['...', '.'], ['..x', '.'], ['.x.', '.'], ['.xx', '.'], ['x..', '.'], ['x.x', '.'], ['xx.', '.'], ['xxx', '.'] ]
    for i in range(8)[::-1]:
        if pattern / (2 ** i) != 0:
            patterns[i][1] = 'x'
        pattern %= 2 ** i

    string_copy = ''
    for turns in range(generations):
        for i in range(len(string)):
            if i+1 == len(string):
                compare_set = string[i-1] + string[i] + string[0]
            else:
                compare_set = string[i-1] + string[i] + string[i+1]
            string_copy += get_transformation(compare_set,patterns)
        string = string_copy
        string_copy = ''
    return string
