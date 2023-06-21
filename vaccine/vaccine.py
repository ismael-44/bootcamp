import requests
import bs4

url = "https://clientes.open6hosting.com/clientarea.php"

def get_form():
    
    html = requests.get(url)
    soup = bs4.BeautifulSoup(html.text, "html.parser")
    forms = soup.find_all("form")
    print(forms)

get_form()
