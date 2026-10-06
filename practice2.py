import json
import urllib.request
import urllib.error

BASE = 'http://127.0.0.1:8001'
def request(path, body=None):
    req = urllib.request.Request(BASE + path, data=body,
                                 headers={'Content-Type': 'application/json'})
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        print(('POST' if body else 'GET'), path, 'HTTP', response.status)
        print(response.read().decode('utf-8'))

print('PRACTICAL WORK 2 - PYTHON LIST AND HTTP')
for path in ['/', '/about/', '/tasks/', '/tasks/1/', '/tasks/999/']:
    request(path)
print('\nPOST ECHO - VALID JSON')
request('/echo/', json.dumps({'message': 'Hello Django', 'number': 4}).encode())
print('\nPOST ECHO - INVALID JSON')
request('/echo/', b'{bad}')
