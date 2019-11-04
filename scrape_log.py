from bs4 import BeautifulSoup
import requests
import regex as re

def get_pdfs(soup):
    pdf_links = []
    for elem in soup.find_all('a'):
        link = elem.get('href')
        if type(link) == str:
            if '.pdf' in link:
                pdf_links.append(link)
    return pdf_links


def get_dates(pdf_links):
    dates = []
    for link in pdf_links:
        date = re.search(r'files/(.*)\.pdf', link).group(1)
        formatted_date = date[0:2] + "-" + date[2:4] + "-" + date[4:]
        dates.append(formatted_date)
    return dates

def download_pdfs(pdf_links):
    for i in range(len(pdf_links)):
        new_request = requests.get(pdf_links[i], stream=True)
        with open("{}.pdf".format(dates[i]), 'wb') as pdf:
            for chunk in new_request.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)

if __name__ == "__main__":
    r = requests.get('https://ucpd.berkeley.edu/alerts-log-news/daily-crime-log')
    soup = BeautifulSoup(r.content, 'lxml')
    pdf_links = get_pdfs(soup)
    clean_pdfs = sorted(pdf_links)[3:]
    dates = get_dates(clean_pdfs)
    download_pdfs(clean_pdfs)
