# API для реферальной системы

## документация есть в документе Redoc
`/api/v1/schema/redoc/`

## postman collection

[click here](https://www.postman.com/ds-8809303/simplereferralapi/collection/t1rvu2c/referral-system)
or paste it:
```
https://www.postman.com/ds-8809303/simplereferralapi/collection/t1rvu2c/referral-system
```
## Эндпоинты

---

### **1. Авторизация по номеру телефона**  
**URL:** `/api/v1/authorisation/phone/`

**Request:** `POST`  
```json
{
  "phone_number": "string"
}
```

**Response:** `200 OK`  
```json
{
  "phone_number": "string",
  "code": "string"
}
```

---

### **2. Подтверждение авторизации по номеру телефона**  
**URL:** `/api/v1/authorisation/phone_confirm/`   

**Request:** `POST`  
```json
{
  "phone_number": "string",
  "code": "string"
}
```

**Response:** `200 OK`  
```json
{
  "token": "string"
}
```

---

### **3. Получение всех профилей**  
**URL:** `/api/v1/users/`

**Request:** `GET`  

**Response:** `200 OK`  
```json
[
  {
    "id": 0,
    "phone_number": "string",
    "referral_number": "string",
    "child_referrals": []
  }
]
```

---

### **4. Получение профиля по ID**  
**URL:** `/api/v1/users/{id}/`   

**Request:** `GET`  

**Response:** `200 OK`

```json
{
  "id": 0,
  "phone_number": "string",
  "referral_number": "string",
  "child_referals": [
    {
      "id": 0,
      "phone_number": "string"
    }
  ]
}
```

---

### **5. Установка реферального кода**  
**URL:** `/api/v1/users/input_referal_code/`   

**Request:** `POST`  
```json
{
  "code": "string"
}
```

**Response:** `200 OK`

```json
{
  "id": 0,
  "phone_number": "string",
  "referral_number": "string",
  "child_referals": [
    {
      "id": 0,
      "phone_number": "string"
    }
  ]
}
```

---