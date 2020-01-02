# Django Oauth2 

## Login
### password-based

/auth/
```
Client-id:{client-id}
Client-secret:{Client-secret}
username:{id}
userpassword:{password}
```
Response token with:
```=
{
    "access_token": "{token}",
    "expires_in": 36000,
    "token_type": "Bearer",
    "scope": "read write groups",
    "refresh_token": "{refresh_token}"
}
```



