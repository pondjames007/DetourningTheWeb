import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def get_pages(idx):
    url = "https://editorial.rottentomatoes.com/publications"
    response = requests.get(url, params = {'wpv_view_count': '52769-TCPID52767', 'wpv_paged': idx}, headers = headers)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    headlines = soup.select('a.article_headline')
    publishers = soup.select('a.unstyled.bold')
    date = soup.select('.subtle.small')

    output_hl = []
    output_pub = []
    output_date = []

    # for title in headlines:
    #     output.append(title.text.strip())

    # print(len(headlines))
    # print(len(publishers))
    # print(len(date))

    for i in range(0, len(headlines)):
        output_hl.append(headlines[i].text.strip())
        output_pub.append(publishers[i].text.strip())
        output_date.append(date[i].text.strip())

    return output_hl, output_pub, output_date

for j in range(1,100):
    result_hl, result_pub, result_date = get_pages(j)
    for i in range(0,len(result_hl)):
         print(result_hl[i])
         print(result_pub[i])
         print(result_date[i])
