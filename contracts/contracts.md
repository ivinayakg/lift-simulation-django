# Entity Relationship Diagram
  ![LIFT Simulation UML - Page 3 (1)](https://user-images.githubusercontent.com/73058928/215698340-15bff0f3-758d-48b3-a8d3-9d1dc757e36c.png)

## **Requests**

|                          Route                           |                       Description                        |
| :------------------------------------------------------: | :------------------------------------------------------: |
|      [POST /api/initiate](#create-elevator-session)      |                Create and return Session                 |
|            [GET /api](#get-elevator-session)             |                      Return Session                      |
|      [POST /api/request](#create-elevator-request)       |            Create and return Elevator request            |
|    [GET /api/request/all](#get-all-elevator-requests)    |               Return all elevator requests               |
| [GET /api/request/latest](#get-latest-elevator-requests) | Return latest elevator request (or the next destination) |
|       [GET /api/elevator/all](#get-all-elevators)        |          Return all the elavtors of the session          |
| [PATCH /api/elevator/:id/update](#update-elevator-data)  |     Update and return the elavtor data with id `:id`     |
|     [GET /api/elevator/:id/:key](#get-elevator-data)     |   Return the elavtor all or `:key` data with id `:id`    |

## **Create Elevator Session**

Create and return Session

- **Body**
  ```
    {
          elevators: INT,
          floors: INT
    }
  ```
- **Code:** 200

  Content :

  ```
    {
      message: "success created",
      session: <session__object>
    }
  ```

- **Error:** 500

  Content :

  ```
    {
      message: "Something Went Wrong",
      error: <error_message>
    }
  ```

## **Get Elevator Session**

Return Session

- **Cookie:**

  django-lift-session: <session_id>

- **Code:** 200

  Content :

  ```
    {
      message: "success",
      session: <session__object>
    }
  ```

- **Error:** 500

  Content :

  ```
    {
      message: "Something Went Wrong",
      error: <error_message>
    }
  ```

## **Create Elevator Request**

Create and return Elevator request

- **Body**
  ```
    {
      destination: INT,
      elevator: <elevator_id>
    }
  ```
- **Cookie:**

  django-lift-session: <session_id>

- **Code:** 200

  Content :

  ```
    {
      message: "success created",
      elevator_request: <elevator_request__object>
    }
  ```

- **Error:** 500

  Content :

  ```
    {
      message: "Something Went Wrong",
      error: <error_message>
    }
  ```

## **Get All Elevator Requests**

Return all elevator requests

- **Query:**

  id = <elevator_request_id>, elevator = <elevator_id>, destination = INT, completed= Boolean

- **Cookie:**

  django-lift-session: <session_id>

- **Code:** 200

  Content :

  ```
    {
      message: "success created",
      elevator_requests: [<elevator_request__object>]
    }
  ```

- **Error:** 500

  Content :

  ```
    {
      message: "Something Went Wrong",
      error: <error_message>
    }
  ```

## **Get Latest Elevator Request**

Return latest elevator request (or the next destination)

- **Cookie:**

  django-lift-session: <session_id>

- **Code:** 200

  Content :

  ```
    {
      message: "success created",
      elevator_request: <elevator_request__object>
    }
  ```

- **Error:** 500

  Content :

  ```
    {
      message: "Something Went Wrong",
      error: <error_message>
    }
  ```

## **Get All Elevators**

Return all the elavtors of the session

- **Query:**

  id = <elevator_id>, curr_floor = INT, direction = String , status = String, gates = String

- **Cookie:**

  django-lift-session: <session_id>

- **Code:** 200

  Content :

  ```
    {
      message: "success created",
      elevators: [<elevator__object>]
    }
  ```

- **Error:** 500

  Content :

  ```
    {
      message: "Something Went Wrong",
      error: <error_message>
    }
  ```

## **Update Elevator Data**

Update and return the elavtor data with id `:id`

- **Body**
  ```
    {
      curr_floor: INT,
      status: String,
      direction: String,
      gates: String
    }
  ```
- **Cookie:**

  django-lift-session: <session_id>

- **Code:** 200

  Content :

  ```
    {
      message: "success created",
      elevator: <elevator__object>
    }
  ```

- **Error:** 500

  Content :

  ```
    {
      message: "Something Went Wrong",
      error: <error_message>
    }
  ```

## **Get Elevator Data**

Return the elavtor all or `:key` data with id `:id`

- **Params:**

  id = <elevator_request_id>, key = [id, curr_floor ,direction, status, gates, session]

  **Key is optional, if no key is specified then all the data attributes are to be returned**

- **Cookie:**

  django-lift-session: <session_id>

- **Code:** 200

  Content :

  ```
    {
      message: "success created",
      elevator: <elevator__object>
    }
  ```

- **Error:** 500

  Content :

  ```
    {
      message: "Something Went Wrong",
      error: <error_message>
    }
  ```
