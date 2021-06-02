import requests as r
from bs4 import BeautifulSoup
import re
import sys

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

def content(page):
    req = r.get(page)
    soup = BeautifulSoup(req.content, "lxml")
    bs = soup.find_all("div", attrs={"class":"question"})
    print(f"len of bs -> {len(bs)} on page -> {page}")
    bs = [remove_tags(re.findall(r'g>[^"\\]+(?:\\.[^"\\]*)*</p>',\
        str(i))[0].replace("</p>", '').replace("g>", '').replace("\xa0", "").replace("\xa02", '').replace("\n", '').strip())\
        for i in bs if len(i) != 0]
    return bs[1:]

def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--num_of_pages", type=int)
    # args = parser.parse_args()
    count_of_pages = int(sys.argv[1])
    result = []
    link = "https://db.chgk.info"
    page = r.get(link)
    page_bs4 = BeautifulSoup(page.content, "lxml")#.prettify()
    page_numbers = page_bs4.find("ul", attrs={"class":"pager"})
    numbers = [re.findall(r'"[^"\\]+(?:\\.[^"\\]*)*"', str(i))[1].replace('"', '') for i in page_numbers.find_all("a")\
        if "pager-current" not in str(i)]
    for i in range(count_of_pages):
        page_link = "https://db.chgk.info" + "/last?page={}".format(i)
        print(page_link)
        page = r.get(page_link)
        page_bs4 = BeautifulSoup(page.content, "lxml")#.prettify()
        table = page_bs4.find("table", attrs={"class":"last_packages"})
        links_a = [str(i) for i in table.find_all("a")]
        links_a = [re.findall(r'"[^"\\]+(?:\\.[^"\\]*)*"', i) for i in links_a]
        links_a = [i[0].replace('"', "") for i in links_a]
        for j in range(len(links_a)):
            tmp = 0
            try:
                if "person" not in (link + links_a[j]) and "user" not in (link + links_a[j]):
                    tmp = content(link + links_a[j])
            except:
                pass
            if tmp != 0:
                result.append(tmp)

    count = 0

    for i in range(len(result)):
        for j in range(len(result[i])):
            count += 1
            if len(result[i][j]) != 0:
                with open("dataset_/data_{}.txt".format(count), "w+") as f:
                    f.write(result[i][j])

    # with open("text.txt", "w+") as f:
    #     for i in result:
    #         for j in i:
    #             f.write(j)
    #             f.write("\n")
    #             count += 1
    print(f"Done with {count} sentences!")
        

if __name__ == "__main__":
    main()