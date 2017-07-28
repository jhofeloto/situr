#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

import re #retira etiquetas HTML de la descripción

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)#Invoca función de consulta y muestra speech al situr3

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "buscarAtractivos":
        return {}
    result = req.get("result")#invocar el result del json
    parameters = result.get("parameters")#invocar el parameters dentro de result
    atractivos = parameters.get("atractivos")#DATO TRAÍDO DE API.AI - ATRACTIVOS

    #URL BASE CONSULTA ATRACTIVOS JSON 1ra posicion
    baseUrlAtractivos = "http://situr.boyaca.gov.co/wp-json/wp/v2/atractivo_turistico?offset=0&search="#URL Base Atractivos
    baseUrlImgAtract = "http://www.situr.boyaca.gov.co/wp-json/wp/v2/media/"#URL Base Imagenes Atractivos
    retirarEspacios = atractivos.replace(" ",  "%20")#Retirar Espacios Atractivos

    leerAtractivo = json.loads(urlopen(baseUrlAtractivos + retirarEspacios).read())
    tituloAtractivo = leerAtractivo[0]['title']['rendered']
    descripcionAtractivo = re.sub("<.*?>", "", leerAtractivo[0]['excerpt']['rendered'])
    urlAtractivo = leerAtractivo[0].get('link')
    idImagenAtractivo = str(leerAtractivo[0]['featured_media'])
    leerImagenAtr = json.loads(urlopen(baseUrlImgAtract + idImagenAtractivo).read())
    imagenAtractivo = leerImagenAtr['media_details']['sizes']['medium']['source_url']

    tituloAtractivo1 = leerAtractivo[1]['title']['rendered']
    descripcionAtractivo1 = re.sub("<.*?>", "", leerAtractivo[1]['excerpt']['rendered'])
    idImagenAtractivo1 = str(leerAtractivo[1]['featured_media'])
    leerImagenAtr1 = json.loads(urlopen(baseUrlImgAtract + idImagenAtractivo1).read())
    imagenAtractivo1 = leerImagenAtr1['media_details']['sizes']['medium']['source_url']


    tituloAtractivo2 = leerAtractivo[2]['title']['rendered']
    descripcionAtractivo2 = re.sub("<.*?>", "", leerAtractivo[2]['excerpt']['rendered'])
    idImagenAtractivo2 = str(leerAtractivo[2]['featured_media'])
    leerImagenAtr2 = json.loads(urlopen(baseUrlImgAtract + idImagenAtractivo2).read())
    imagenAtractivo2 = leerImagenAtr2['media_details']['sizes']['medium']['source_url']

    tituloAtractivo3 = leerAtractivo[3]['title']['rendered']
    descripcionAtractivo3 = re.sub("<.*?>", "", leerAtractivo[3]['excerpt']['rendered'])
    idImagenAtractivo3 = str(leerAtractivo[3]['featured_media'])
    leerImagenAtr3 = json.loads(urlopen(baseUrlImgAtract + idImagenAtractivo3).read())
    imagenAtractivo3 = leerImagenAtr3['media_details']['sizes']['medium']['source_url']

    tituloAtractivo4 = leerAtractivo[4]['title']['rendered']
    descripcionAtractivo4 = re.sub("<.*?>", "", leerAtractivo[4]['excerpt']['rendered'])
    idImagenAtractivo4 = str(leerAtractivo[4]['featured_media'])
    leerImagenAtr4 = json.loads(urlopen(baseUrlImgAtract + idImagenAtractivo4).read())
    imagenAtractivo4 = leerImagenAtr4['media_details']['sizes']['medium']['source_url']


    speech = "El atractivo: " + tituloAtractivo + ". Descripción:" + descripcionAtractivo + "    y la url de la imagen es: " + imagenAtractivo

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "data" :
            {
                "facebook" : {
                    "attachment" : {
                        "type" : "template",
                        "payload" : {
                            "template_type" : "generic",
                           "elements" : [
                                {
                                    "title" : tituloAtractivo,
                                    "image_url" : imagenAtractivo,
                                    "subtitle": descripcionAtractivo,
,
                                    "buttons":  [
                                        {
                                            "type":"web_url",
                                            "url": "http://situr.boyaca.gov.co",
                                            "title": "Ver"
                                        },
                                        {
                                             "type":"web_url",
                                            "url": "http://situr.boyaca.gov.co",
                                            "title": "Ver2"
                                        },
                                        {
                                              "type":"web_url",
                                            "url": "http://situr.boyaca.gov.co",
                                            "title": "Ver3"
                                        }
                                    ]
                                },
                                {
                                    "title": tituloAtractivo1,
                                    "image_url": imagenAtractivo1,
                                    "subtitle": descripcionAtractivo1,
                                    "default_action": {
                                        "type": "web_url",
                                        "url": "https://www.moovrika.com/m/4167",
                                        "webview_height_ratio": "tall"
                                    },
                                    "buttons": [
                                        {
                                            "title": "more info",
                                            "type": "web_url",
                                            "url": "https://www.moovrika.com/m/4082",
                                            "webview_height_ratio": "tall"
                                        },
                                        {
                                             "type":"web_url",
                                            "url": "http://situr.boyaca.gov.co",
                                            "title": "Ver2"
                                        },
                                        {
                                              "type":"web_url",
                                            "url": "http://situr.boyaca.gov.co",
                                            "title": "Ver3"
                                        }
                                    ]
                                }
                           ]
                       }
                    }
                }
            },
#       "contextOut": [{"name":"desdepython", "lifespan":2, "parameters":{"slug":urlAtractivo}}],
        "source": "apiai-situr3"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
