import requests, json, time, threading
from bs4 import BeautifulSoup

start = time.perf_counter()


def getSource(url):  # vrati source kod v soup
    req = requests.get(url)
    if req.status_code != 200:
        raise Exception(f"Error {req.status_code}")
    return BeautifulSoup(req.content.decode("utf-8"), "html.parser")


def crop(soup,):  # vymaze text v strongu (Miesto výkonu práce, Platové ohodnotenie) aby zostalo len info
    soupS = len(soup.find("strong").get_text())
    return soup.get_text()[soupS:]


def getPonuku(soup):  # zoberie info z source codu pre jednu ponuku (job detail page)
    soups = soup.find_all("div", class_="col-md-4 icon")

    title = soup.find("h1").get_text()
    place = crop(soups[0].find("p"))
    salary = crop(soups[1].find("p"))
    contract_type = crop(soups[2].find("p"))

    contract_email = soup.find("a", class_="position-button")["href"]
    index = contract_email.index(":")  # vymaze mailme ktore je pred adresov aby sa dala na webe kliknut
    contract_email = contract_email[index + 1 :]

    return {
        "title": title,
        "place": place,
        "salary": salary,
        "contract_type": contract_type,
        "contract_email": contract_email,
    }


def asyncCall(i, url):
    soupPonuka = getSource(url)
    ponuky[i] = getPonuku(soupPonuka)


url = "https://www.hyperia.sk"
threads = []

soup = getSource(f"{url}/kariera")  # nacita web zo vsekymi ponukami
soup = soup.find("section", id="positions")
soup = soup.find_all("a")

ponuky = [None for _ in range(len(soup))]

for i, a in enumerate(soup):  # zacne volat async funkcie na kazdu ponuku
    ponuka = a["href"]
    threads.append(threading.Thread(target=asyncCall, args=(i, url + ponuka)))
    threads[-1].start()  # spustenie async funkcie

for thread in threads:  # caka kym neskoncia async funkcie
    thread.join()

with open("output.json", "w", encoding="utf-8", errors="replace") as file:  # export do json
    file.write(json.dumps(ponuky, ensure_ascii=False))

print(f"program bezal {time.perf_counter()-start}s")
