import requests
from bs4 import BeautifulSoup

def get_forecast(national = False):
    dublin = "https://www.met.ie/forecasts/dublin"
    page = requests.get(dublin)
    soup = BeautifulSoup(page.content, "lxml")
    results = soup.find_all(id = "National-Forecast-Map")
    headings = [result.text for result in results[0].find_all("h2")]
    pars = [par.text for par in results[0].find_all("p")[1:-2]]
    forecast = list(zip(headings, pars))
    return forecast[:-1] if not national else forecast
