# Routing Service

A HTTP microservice that finds the routes and minimizes the total delivery
duration.

### Tech Stack

* #### Python & Flask
* #### openrouteservice
* #### MongoDB

---

### Install & Run

Build service and db

```bash
docker-compose build
```

Run them

```bash
docker-compose up -d
```

---

## API

#### [POST] /api/v1/routes

Helps to find routes that it minimizes the total delivery duration.

Request Schema

```bash
{
    "vehicles": [
        {
            "id": {
                "type": "int",
                "required": true
            },
            "start_index": {
                "type": "int",
                "required": true
            },
            "capacity": {
                "type": "list",
                "required": false
            }
        }
    ],
    "jobs": [
        {
            "id": {
                "type": "int",
                "required": true
            },
            "location_index": {
                "type": "int",
                "required": true
            },
            "delivery": {
                "type": "list",
                "required": false
            },
            "service": {
                "type": "int",
                "required": false
            }
        }
    ],
    "matrix": [
        {
            "type": "list",
            "required": true
        }
    ]
}
```

# Configuration

### What if my openrouteservice API token got expired, or I need to get a new one somehow?



[Easily login with your GitHub account here](https://openrouteservice.org/dev/#/login)

After logged in, you can create a new token by selecting the token's type and entering its name  just under the title of Request a token .