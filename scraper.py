import requests, re, json
from bs4 import BeautifulSoup

def finder(url):
    res = requests.get(url)
    nsoup = BeautifulSoup(res.content, "html.parser")
    name = nsoup.find("h1").text
    pattern = r"iframe src=\"(.*?)\""
    mat = re.search(pattern,res.text)
    if mat:
        link2 = mat.group(1)
        link = "https:" + link2
        peg = requests.get(link).text
        pattern2 = r'fid="(.*?)"'
        mat2 = re.search(pattern2, peg)
        if mat2:
            slug = mat2.group(1)
        else:
            slug = "ptvpk"
        return name, slug
    return("404")

def iterator(job_elements):
    data = []
    for job_element in job_elements:
        link = job_element.a['href']
        if link=="":
            continue
        info = {}
        try:
            logo = URL + job_element.img['src']
        except:
            logo = "https://me.crichd.tv/assets/images/custom-channels.png"
        name, channelid = finder(link)
        info['name'],info['logo'],info['slug'] = name, logo, channelid
        data.append(info)
        print(name, channelid)
    return data

URL = "https://me.crichd.tv/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="channels")
jobs = results.find_all("div", class_="channels")
jobs2 = results.find_all("li", class_="channel-item")

chdata = {}
data1 = iterator(jobs)
data2 = iterator(jobs2)
data = data1 + data2

chdata['info'] = data
with open("channels.json","w") as w:
    json.dump(chdata,w,indent=2)
