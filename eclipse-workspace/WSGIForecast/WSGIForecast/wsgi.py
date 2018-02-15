from urllib2 import Request, urlopen
from urllib import urlencode, quote_plus
from cgi import parse_qs, escape
import json

SERVICE_KEY = 'YOUR KEY HERE' # 공공 API 키 입력
def application(environ, start_response):
    d = parse_qs(environ['QUERY_STRING'])
    
    date = d.get('date', [''])[0]
    time = d.get('time', [''])[0]
    date = escape(date)
    time = escape(time)
    url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData' # 동네 예보조회URI
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
    jsondumps = json.dumps(response)
    
    rain = 0
    humidity = 0
    lowest = 0
    highest = 0
    
    
    items = jsondumps['response']['body']['items']['item']
    for item in items:
        if item['category']=='POP':
            rain = item['fcstValue']
        elif item['category']=='REH':
            humidity = item['fcstValue']
        elif item['category']=='TMN':
            lowest = item['fcstValue']
        elif item['category']=='TMX':
            highest = item['fcstValue']
    out = {"rain":rain,"humidity":humidity,"lowest":lowest,"highest":highest}
    response_body = json.loads(out) 
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]
    
    start_response(status, response_headers)
    return [response_body]