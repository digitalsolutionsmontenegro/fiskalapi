# fiskalapi
### API za CG fiskalizaciju ::: @ https://fiskalapi.efiskal.me/api :::
### ver 12.0.1 | 20.06.2023


url: [https://fiskalapi.efiskal.me/api/](https://fiskalapi.efiskal.me/api/)

example python client API code availabe with the: python_client_api.py

# 1. Oauth2 : get access_token / expiration 3600s

OAuth2 : 
    grant_type: "client_credentials"


client_id = 'yourClientIDKey'
client_secret = 'yourClientSuperDuperSecretKey'
token_url = 'https://fiskalapi.efiskal.me/api/authentication/oauth2/token'
...
...
access_token = response.json()['access_token']

use access token in headers:

headers = {
    'Authorization': f'Bearer {access_token}'
}

# 2. use company_id: company_id is required for live database use !
for testing, the company_id is not required, it will always be #1 by default
for production, use of the company_id is mandatory

# 3. manage products:
### 3.1 search products : method \[GET\] 

url: https://fiskalapi.efiskal.me/api/search/product.template
attributes (optional): {"domain" : []} #put domain for filtering results
response (JSON) retun ids of the products:
[
    3,
    4,
    5,
]

### 3.2 read products : method \[GET\] 
url: https://fiskalapi.efiskal.me/api/read/product.template
attributes (list of ids): 
"ids" : [3]
"fields" : ["id","name","lst_price","taxes_id"]

**response** (JSON) retun ids of the products:
`[ 3, 4, 5, ]`


#### 3.2 read products : method \[GET\] 
url: [/api/read/product.template](https://fiskalapi.efiskal.me/api/read/product.template "/api/read/product.template")

**attributes** (list of ids): 
`"ids" : [3]
"fields" : ["id","name","lst_price","taxes_id"]`

**response:** will return results for a fields defined (or all the fields if fields values is omitted)
`[
    {
        "id": 3,
        "lst_price": 12.5,
        "name": "Karta test",
        "taxes_id": [
            1
        ]
    }
]`

### 3.3 create product : method \[POST\] 
url: https://fiskalapi.efiskal.me/api/create/product.template
attributes: "values" : {
    "name" : "product name", 
    "lst_price" : "5.0",
}

**response:** will be the ID of the new recod
[
    6
]

### 3.4 write product : method \[PUT\] - will update the product values for the product ID
url: https://fiskalapi.efiskal.me/api/write/product.template
attributes: 
"ids" : "3"
"values" : {
    "name" : "product name", 
    "lst_price" : "5.0",
}`

**response:** will return true if success
`true`


# 4. manage invoicing:
### 4.1 create and fiscal invoice
*** automatski se otvara novi dan, ukoliko nije prijavljen depozit na EFI 
*** metoda vraca podatke fiskalizacije u JSON response

api_url = https://fiskalapi.efiskal.me/api/call/account.invoice/create_and_fiskal_invoice

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

**response:** json response sample: Invoice fiscalisation details
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

 
