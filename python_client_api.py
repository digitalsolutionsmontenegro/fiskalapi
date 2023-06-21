### API za CG fiskalizaciju ::: @ https://fiskalapi.efiskal.me/api :::
### ver 12.0.1 | 20.06.2023
### powered by: efiskal.me ::: by digitalsolutions.me 

import json
import requests
from requests.auth import HTTPBasicAuth

CLIENT_ID = 'write your client ID here'
CLIENT_SECRET = 'write your client secret here'

auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)

# base url
base_url = 'https://fiskalapi.efiskal.me'

### dodati data {'db': 'fiskalapi', ... } -> for multi db instances
### dodati verify=False - da ne radi verifikaciju SSL lokalno !!! vazno!

### OAuth2 Authentication & retreive access token ###
api_url = f'{base_url}/api/authentication/oauth2/token'
data = {
    'grant_type': 'client_credentials'
}
response = requests.post(token_url, auth=auth, data=data)
if response.status_code == 200:
    access_token = response.json()['access_token']
    print(response.json())
else:
    print("Token retrieval failed with status code:", response.status_code)

#define access token in headers
headers = {
    'Authorization': f'Bearer {access_token}'
}
data = {}

### GET SESION INFO ###
api_url = f'{base_url}/api/session'
response = requests.get(api_url, headers=headers, data=data)
print('\n### GET SESION INFO ###\n{}'.format(response.json()))

### SEARCH PRODUCTS ###
api_url = f'{base_url}/api/search/product.template'
domain = "[('active','=',True)]"  #OPTIONAL - 
data = {
    'domain': domain,
}
response = requests.get(api_url, headers=headers, data=data)
print('\n### SEARCH PRODUCTS ###\n{}'.format(response.json()))

''' json returns IDs
[1, 3, 4, 5, 6, 8, 2]
'''

### CREATE PRODUCT ###
api_url = f'{base_url}/api/create/product.template'
values = {
    'name' : 'Online karta - cloud dozivljaj',     #MANDATORY# product/service name
    'lst_price' : 4.5,          #sale price
    'type' : 'service',         #product type 
    'default_code' : 'ref#'     #refernce code
}
data = {
    'values': json.dumps(values),
}
response = requests.post(api_url, headers=headers, data=data)
print('\n### CREATE PRODUCT ###\n{}'.format(response.json()))
''' json returns ID
[ 8 ]
'''

### UPDATE PRODUCT ###
api_url = f'{base_url}/api/write/product.template'
values = {
    'lst_price' : 7,        #new sale price
}
data = {
    'ids' : 8,              #id(s) of the record(s) that will be updated
    'values': json.dumps(values),
}
response = requests.put(api_url, headers=headers, data=data)
print('\n### UPDATE PRODUCT ###\n{}'.format(response.json()))
''' json returns status
true
'''
### **** Tip **** ###
### - instead deleting, records can be archived and unarchived by sending payload:
### {'active' : False }     #for archiving
### {'active' : True }     #for activating
### ************* ###


### READ PRODUCT ###
api_url = f'{base_url}/api/read/product.template'
fields = ['id','name','lst_price']      #OPTIONAL# to read only some fields, if omitted all fields and values will return
data = {
    'ids' : 8,              #id(s) of the record(s) that will be updated
    'fields': json.dumps(fields),
}
response = requests.get(api_url, headers=headers, data=data)
print('\n### READ PRODUCT ###\n{}'.format(response.json()))
''' json returns data
[
    {
        "id": 8,
        "lst_price": 7.0,
        "name": "Online karta - cloud dozivljaj"
    }
]
'''


### KREIRA RACUN I FISKALIZUJE GA jednim pozivom !!! ###
## *** automatski se otvara novi dan, ukoliko nije prijavljen depozit na EFI 
## *** metoda vraca podatke fiskalizacije
api_url = f'{base_url}/api/call/account.invoice/create_and_fiskal_invoice'

### OPTION 1 single product - single line detail
values = {
    'invoice_line': 
        {'product_id': 2, 'name': 'probna karta5 - single', 'qty': 3, 'price': 3.5, 'tax': '21%'},
    'order_id': 'ONLINEKARTA-23-00023',
    'return_qr_binary': True,
}
### OPTION 2 multiple products - multiple line details
values = {
    'invoice_lines': [
        {'product_id': 2, 'name': 'probna karta3', 'qty': 3, 'price': 5, 'tax': '21%'},
        {'product_id': 2, 'name': 'probna karta4', 'qty': 1, 'price': 8.5, 'tax': '21%'},
    ],
    'order_id': 'ONLINEKARTA-23-00023',         # postoji kontrola da ne dozvoli dva puta isti order reference da se posalje !
    'return_qr_binary': True,
}
data = {
    'kwargs': json.dumps(values),
}

response = requests.post(api_url, headers=headers, data=data)
print('\n### KREIRAJ U FISKALIZUJ ###\n{}'.format(response.json()))
''' json returns FISKALNE PODATKE
{
    "access_url": "/my/invoices/9",
    "fiskal_id": 4,
    "id": 9,
    "ikof": "9baabbcaa776ef1f80e0dbf993d0b2b1",
    "jikr": "aef0476b-e8c7-485f-8555-0dc875035cf6",
    "racun": "bh543ko548/4/2023/kj218fr171",
    "reference": "ONLINEKARTA-23-00001",
    "url": "https://efitest.tax.gov.me/ic/#/verify?iic=9baabbcaa776ef1f80e0dbf993d0b2b1&tin=03010864&crtd=2023-06-21T02:27:38+02:00&ord=4&bu=bh543ko548&cr=kj218fr171&sw=rm081uq203&prc=42.00"
}
'''
