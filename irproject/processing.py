
with open("../links.txt", 'rb') as f:
    content = f.readlines()

links = [x.strip() for x in content]

articles=[]

for i in links:
    words=i.split('/')
    if len(words)>3:
        if words[1]=='sports' or words[1]=='features':
            articles.append("https://moraspirit.com"+i)
articles=set(articles)
articles=list(articles)
print articles
for i in articles:
    print i
print len(articles)