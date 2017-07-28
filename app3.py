import urllib
import json

url = "http://situr.boyaca.gov.co/wp-json/wp/v2/atractivo_turistico?orderby=relevance&orderby=relevance&offset=0&search=laguna"
response = urllib.urlopen(url)
content = response.read()
data = json.loads(content.decode("utf8"))
test = ['1', '2', '3', '4', '5', '6', '7', '8', '9','10']

#print(data)
#print(data['slug'])
print data[1]['title']['rendered']
print data[2]['title']['rendered']
print data[3]['title']['rendered']
print data[4]['title']['rendered']
print data[5]['title']['rendered']
print data[6]['title']['rendered']
print data[7]['title']['rendered']
print data[8]['title']['rendered']
print data[9]['title']['rendered']
print data[10]['title']['rendered']

#print data(['title']['rendered'])

#if __name__ == '__app__':
#    ruta = 'http://situr.boyaca.gov.co/wp-json/wp/v2/atractivo_turistico?orderby=relevance&orderby=relevance&offset=0&search=laguna'
#    cargar_datos(ruta)

for i in xrange(len(test)):
  print test[i]
