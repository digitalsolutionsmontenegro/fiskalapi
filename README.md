# fiskalapi
fiskal api interface for efiskal.me service

url: [https://fiskalapi.efiskal.me/api/](https://fiskalapi.efiskal.me/api/)

### 1. Oauth2 Authentication: 
**get access_token (expiration 3600s)**

OAuth2 : 
    grant_type: "client_credentials"

```python
client_id = 'yourClientIDKey'
client_secret = 'yourClientSuperDuperSecretKey'
token_url = 'https://fiskalapi.efiskal.me/api/authentication/oauth2/token'
...
...
access_token = response.json()['access_token']
```
use access token in headers:
```python
headers = {
    'Authorization': f'Bearer {access_token}'
}
```
### 2. multicompany - use company_id: 
- company_id is required for live database use !
- for testing, the company_id is not required, it will always be #1 by default
- for production, use of the company_id is mandatory

### 3. manage products:
#### 3.1 search products : method \[GET\] 
url: [/api/search/product.template](https://fiskalapi.efiskal.me/api/search/product.template "/api/search/product.template")

**attributes** (optional): 
`{"domain" : []}` #put domain for filtering results

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


#### 3.3 create product : method \[POST\] 
url: [/api/create/product.template](https://fiskalapi.efiskal.me/api/create/product.template "/api/create/product.template")

**attributes:** "values" : {
    "name" : "product name", 
    "lst_price" : "5.0",
}

**response:** will be the ID of the new recod
[
    6
]


#### 3.4 write product: **method \[PUT\]** 
- will update the product values for the product ID
url: [/api/write/product.template](https://fiskalapi.efiskal.me/api/write/product.template "/api/write/product.template")

**attributes: **
`"ids" : "3"
"values" : {
    "name" : "product name", 
    "lst_price" : "5.0",
}`

**response:** will return true if success
`true`


##4. manage invoicing & fiscalisation:
**TBD**
 
