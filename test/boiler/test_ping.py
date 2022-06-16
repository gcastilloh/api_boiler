
import json
from django.urls import reverse

def test_ping(client):
    # ------ Given: ---------
    # nada que manipular en la base de datos


    # ------ When: ---------
    
    # obtenemos la url
    url = reverse("ping")
    # hacemos una petición get con la url
    # recibimos un Json como respuesta
    response = client.get(url)
    #convertimos el json a diccionario
    content = json.loads(response.content)

    #------ Entonces: -------
    # revisamos si hemos recibido un 200 (funcionamiento normal)
    assert response.status_code == 200
    # revisamos la respuesta
    assert content["ping"] == "pong!"
    
