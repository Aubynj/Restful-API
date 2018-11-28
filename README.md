# Restful-API
### What is a RESTful API?

One of the most popular types of API is REST or, as they’re sometimes known, RESTful APIs. REST or RESTful APIs were designed to take advantage of existing protocols. While REST - or Representational State Transfer - can be used over nearly any protocol, when used for web APIs it typically takes advantage of HTTP. This means that developers have no need to install additional software or libraries when creating a REST API.
In this scripts i build a simple Restful API with Flask

#### Core Libraries
* Flask
  * Flask-SQLAlchemy
  * Flask-HTTPAuth
  * Flask-Bcrypt
* Itsdangerous (Python Library)

### Step 1
After starting the server, create a client info.

**POST http://127.0.0.1:5000/client/create**

**Body** Formdata

__client_user__    *clientusername*

__client_password__    *clientpassword*

### Step 2
Make a POST request to gain Authorization code by passing a Basic Authentication (Thus: from step 1: client_user and client_password as your username and password) to the endpoint

**POST http://127.0.0.1:5000/authorization/connect**

**RESPONSE** _OK_
```
{
  Authorization Code : *Authorization_code*   
}
```
### Step 3
After the Authorization code is return, we make a GET request to obtained our Authentication Token, and Refresh Token

**GET http://127.0.0.1:5000/authorization/token**

**Body** Formdata

__grant__    *grant* Leave as grant

__code__    *Authorization_code*

**RESPONSE** _OK_
```
{
  'access_token' : access_token,
  'refresh_token' : refresh_token,
  'type' : 'bearer',
  'expires_in' : 3600
}
```

### STEP 4
Our access token also get expired for an hour. In other to make sure we are still active to the system, we have to make a POST request to the refresh endpoint to refresh our tokens. **NB** BASIC Authentication is needed for this endpoint

**POST http://127.0.0.1:5000/token/refresh**

**Body** Formdata

__grant__    *grant* Leave as grant

__refresh_token__    *refresh_token*

**RESPONSE** _OK_
```
{
  'access_token' : access_token,
  'refresh_token' : refresh_token,
  'type' : 'bearer',
  'expires_in' : 3600
}
```
### Step 5
This is step depends on the user on how request data. Passed Authentication token to the endpoint headers. For example as implemented in the scripts for users


**GET http://127.0.0.1:5000/api/users**

**HEADERS**

__Authorization__     Bearer _access_token_


**RESPONSE** _OK_
```
{
  'username' : username,
  'secret' : secret
}
```

# Author

* John Aubyn Initial Work [Developer](https://aubynj.github.io/)    

# License
This work is licensed by [Swedish Ason Group AB](https://www.dangstons.se/)















