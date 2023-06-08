# ToDo-List challenge
Web API that allows users to create and manage their tasks. The ability to create user has no retrictions so anyone can create and account, request a token and start creating their tasks.

# Endpoints
## List or Create User [/users/]
- GET: List all users.
- POST: Create a new user.

### List Users [GET]
- Response 200 (application/json)
  - Body
    ```
    [
      {
          "id": 1,
          "username": "Juan",
          "email": "juan@example.com"
      },
      {
          "id": 2,
          "username": "Santiago",
          "email": "santiago@example.com"
      }
    ]
    ```
### Create User [POST]
- Request (application/json)
  - Payload
      ```
    {
        "username": "newuser",
        "email": "newuser@example.com"
        "password: "password
    }
      ```
- Response 201 (application/json)
  - Body
      ```
    {
        "username": "newuser",
        "email": "newuser@example.com"
    } 
      ```
 ## Detail User [/users/{user_id}/]
  - GET: Retrieve user details.
  - PATCH: Update user details.
  - DELETE: Delete a user.

### Retrieve User [GET]
- Response 200 (application/json)
  - Body
      ```
    {
        "username": "newuser",
        "email": "newuser@example.com"
    } 
      ```

 ### Update User [PATCH]
- Request (application/json)
  - Payload
      ```
    {
        "username": "newusername",
    }
      ```
- Response 201 (application/json)
  - Body
      ```
    {
      "username": "newusername",
      "email": "newuser@example.com"
    } 
      ```
 ### Delete User [DELETE]
- Response 204

## List or Create User Tasks [/users/<user_id>/tasks/]
- GET: List all users tasks.
- POST: Create a new user task.

### List User Tasks [GET]
- Response 200 (application/json)
  - Body
    ```
    [
      {
            "id": 1,
            "title": "Do stuff",
            "description": "An explanation of your task",
            "date": "2023-10-10T08:00:00Z",
            "status": "Pendiente",
            "user": 11
      },
      {
            "id": 2,
            "title": "Doctor appointment",
            "description": "Ask for painkillers",
            "date": "2023-10-10T08:00:00Z",
            "status": "Pendiente",
            "user": 11
      }
    ]
    ```
### Create User Task [POST]
- Request (application/json)
  - Payload
      ```
    {
      "title":"Go for a beer",
      "description":"Invite a friend",
      "date":"2023-10-10T08:00",
    }
      ```
- Response 201 (application/json)
  - Body
      ```
    {
      "id": 1,
      "title":"Go for a beer",
      "description":"Invite a friend",
      "date":"2023-10-10T08:00",
      "status": "Pendiente"
    } 
      ```

 ## Detail User Task [/users/{user_id}/tasks/{task_id>]
  - GET: Retrieve user task details.
  - PATCH: Update user task details.
  - DELETE: Delete a user task.
 
### Retrieve User task [GET]
- Response 200 (application/json)
  - Body
      ```
    {
      "id": 1,
      "title": "Go for a beer",
      "description": "Invite a friend",
      "date": "2023-10-10T08:00:00Z",
      "status": "Pendiente"
    } 
      ```

 ### Update User [PATCH]
- Request (application/json)
  - Payload
      ```
    {
        "status": 2, #TODO change this so it allows strings. Temp solution 1: Pendiente; 2: Completado
    }
      ```
- Response 201 (application/json)
  - Body
      ```
    {
    "id": 1,
    "title": "Go for a beer",
    "description": "Invite a friend",
    "date": "2023-10-10T08:00:00Z",
    "status": "2"
    } 
      ```
 ### Delete User task [DELETE]
- Response 204

 ## Search User Task [/users/{user_id}/tasks/search/?title='title'&date='date']
    - GET: Retrieve list of user tasks.
 ### Search User Tasks [GET]
- Response 200 (application/json)
  - Body
    ```
    [
      {
            "id": 1,
            "title": "Do stuff",
            "description": "An explanation of your task",
            "date": "2023-10-10T08:00:00Z",
            "status": "Pendiente",
            "user": 11
      },
      {
            "id": 2,
            "title": "Doctor appointment",
            "description": "Ask for painkillers",
            "date": "2023-10-10T08:00:00Z",
            "status": "Pendiente",
            "user": 11
      }
    ] 

