import requests

from bs4 import BeautifulSoup

def consulta_asegurado(nro_cic):

    def clean_data(data):
        return data.get_text().replace('\n', '').replace('\t', '').strip()
        
    url = 'https://servicios.ips.gov.py/consulta_asegurado/comprobacion_de_derecho_externo.php'
    form_data = {'nro_cic': str(nro_cic), 'recuperar': 'Recuperar', 'elegir': '', 'envio':'ok'}
    session = requests.Session()
    try:
        soup = BeautifulSoup(
            session.post(
                url, 
                data=form_data,
                timeout=10,
                headers={'user-agent': 'Mozilla/5.0'},
                verify=True
            ).text, 
            "html.parser"
        )
        
        master = soup.select('form > table')[1]
        head = master.select('th')
        data_row = master.select('td')
        
        return dict(zip(map(clean_data, head), map(clean_data,data_row)))
        
    except requests.ConnectionError:
        print("Connection Error")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    data = consulta_asegurado(1234567)
    print(data)