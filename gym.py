import requests
from bs4 import BeautifulSoup


def get_timetable():
    flyefit = "https://www.flyefit.ie/gyms/ranelagh/"
    page = requests.get(flyefit)
    soup = BeautifulSoup(page.content, "lxml")
    results = soup.find_all(class_="timetable__table schedule-this-week active")
    today = results[0].find_all(class_="day active")[0]
    class_text = [class_.get_text() for class_ in today.find_all(class_="class")]
    class_text = ["\n".join(text.split("\n")[1:4]) for text in class_text if len(text) > 2]
    return "\n\n".join(class_text)

def accuweather():
    link = "https://www.accuweather.com/en/ie/dublin/207931/hourly-weather-forecast/207931"
    header = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0 X-Middleton/1"
}
    page = requests.get(link, headers=header)
    soup = BeautifulSoup(page.content, "lxml")
    results = list(soup.find_all(class_ = "accordion-item hourly-card-nfl hour non-ad" ))
    fields = ["date", "phrase", "precip", "temp metric", "real-feel"]
    out = ""
    # translator to remove escape strings
    escapes = ''.join([chr(char) for char in range(1, 32)])
    remover = str.maketrans("", "", escapes)
    for result in results:
        curr_fields = [result.find_all(class_ = field)[0].text.translate(remover) for field in fields]
        curr_fields[0] = curr_fields[0].split("M")[0] + "M" # clean time
        curr_fields[-1] = curr_fields[-1].split("®")[-1] # clean realfeel
        timestamp, phrase, precip, temp, realfeel = curr_fields
        out += f"{timestamp}: {phrase}\nP: {precip} T: {temp} RF: {realfeel}\n\n"
    
    return out
