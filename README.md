# Simple REST API for chat system

## Setting up

Install dependencies:
```bash
pipenv install
```
Activate virtual environment:
```bash
pipenv shell
```

Go to working directory:
```bash
cd src/
```

_If you don't have pipenv installed, please visit https://pipenv-fork.readthedocs.io/en/latest/install.html#installing-pipenv_

## Running
Run the application on localhost:
```bash
python3 manage.py runserver
```

**Do not use in production, it's not configured for deployment**

## API usage

### Create users
API uses token authentication, so please create users at admin page. Admin page is located at `/admin/`.

### Obtain tokens
Obtain a token at admin page or send a POST request to `/auth/` with username and password.

### Sending requests to API
In order to access the API, provide your token for each subsequent request: `AUTHORIZATION: Token <your_token>`

### Available actions

**Create a new message:** `POST /api/messages/ {receiver:int, text:str}`

`receiver` is the id of user that you want send a message to.

Note that `receiver` can be the same user, it's intended behaviour and should be used as "saved messages".
___


**List your messages:** `GET /api/messages/`

See all the messages that are relevant for you (you are either sender or receiver).

Example response:
```json
    [{
        "id": 1,
        "text": "hi there!",
        "created_at": "2020-05-11T20:02:43.680950+03:00",
        "sender": 1,
        "receiver": 2
    },
    {
        "id": 2,
        "text": "hello",
        "created_at": "2020-05-11T20:03:02.434049+03:00",
        "sender": 2,
        "receiver": 1
    },
    {
        "id": 3,
        "text": "do not forget to buy some butter",
        "created_at": "2020-05-11T20:03:40.921901+03:00",
        "sender": 1,
        "receiver": 1
    }] 
```
___


**View particular message:** `GET /api/messages/<pk:int>/`

This action is allowed if you are sender or receiver of the message. 
___


**Update the message:** `PUT/PATCH /api/messages/<pk:int>/ {receiver:int, text:str}`

This action is allowed if you are sender of the message.
___

**Delete the message:** `DELETE /api/messages/<pk:int>/`

This action is allowed if you are sender of the message.
___


## Testing
Run tests with:
```bash
python3 manage.py test api/tests/
```

## Contributing
Feel free to open an issue or PR, make sure you are formatting your code with [black](https://github.com/psf/black) and sorting imports with [isort](https://github.com/timothycrosley/isort).
