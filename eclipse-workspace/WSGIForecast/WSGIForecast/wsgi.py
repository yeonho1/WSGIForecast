from urllib2 import Request, urlopen
from urllib import urlencode, quote_plus
from cgi import parse_qs, escape
import json
from django.contrib.admin.utils import quote

with open(r'/usr/local/service_keys/forecast.txt') as service_keyfile:
    SERVICE_KEY = service_keyfile.read()
def application(environ, start_response):
    d = parse_qs(environ['QUERY_STRING'])
    
    date = d.get('date', [''])[0]
    time = d.get('time', [''])[0]
    date = escape(date)
    time = escape(time)
    url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData'
    queryParams = '?' \
        + 'ServiceKey=' + SERVICE_KEY + '&' \
        + urlencode({
            quote_plus('base_date'): date,
            quote_plus('base_time'): time,
            quote_plus('nx'): '60',
            quote_plus('ny'): '127',
            quote_plus('numOfRows') : '10',
            quote_plus('pageNo') : '1',
            quote_plus('startPage') : '1',
            quote_plus('_type'): 'json'
        })
    print('[' + url + queryParams + ']')
    request = Request(url + queryParams)
    request.get_method = lambda: 'GET'
    response = urlopen(request).read()
    
    status = '200 OK'
    response_body = response
    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]
    
    start_response(status, response_headers)
    return [response_body]