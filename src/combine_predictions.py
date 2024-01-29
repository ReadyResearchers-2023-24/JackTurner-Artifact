import http.client, urllib.parse, json

conn = http.client.HTTPSConnection('api.marketaux.com')

params = urllib.parse.urlencode({
    'api_token': 'YrnxgrKvZsSxEYVJDLsN0Ly2EdRBh0ZbDIcJOxud',
    'symbols': 'AAPL,TSLA',
    'limit': 50,
})

conn.request('GET', '/v1/news/all?{}'.format(params))

res = conn.getresponse()
data = res.read()

# Parsing the response data to a dictionary
data_dict = json.loads(data.decode('utf-8'))

# Extracting 'symbol', 'highlight' and 'sentiment'
extracted_data = []
for item in data_dict['data']:
    for entity in item.get('entities', []):
        symbol = entity.get('symbol', 'N/A')  # Default to 'N/A' if symbol is not available
        for highlight in entity.get('highlights', []):
            extracted_data.append({
                'symbol': symbol,
                'highlight': highlight['highlight'],
                'sentiment': highlight['sentiment']
            })

# Writing the extracted data to a JSON file
with open('highlights_sentiments_symbols.json', 'w') as json_file:
    json.dump(extracted_data, json_file, indent=4)

conn.close()
