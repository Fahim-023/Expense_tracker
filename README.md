# Personal Expense Tracker API

A REST API for tracking personal income and expenses, built with FastAPI. Users can register, log in, and manage their own transactions. Each user can only see and change their own records.

Data is stored in a PostgreSQL database through the SQLAlchemy ORM. Passwords are hashed before they are saved and are never returned in any response. Logging in gives the user a JWT access token, and every transaction route requires that token.

**Live Demo ** : https://expense-tracker-2-kwtg.onrender.com/docs


## What the API does

- Registers users and logs them in with a username and password.
- Lets a logged-in user create, view, update and delete transactions.
- Keeps each transaction private to the user who created it.
- Validates all input: the amount must be positive, and the type must be `income` or `expense`.
- Filters a user's transactions by type, category, and a minimum and maximum amount.
- Returns clear 404 errors for missing transactions, and 401 errors for missing or invalid tokens.

## Architecture

The project is split into layers, and each layer has one job.

```
Client (Swagger UI / Postman / frontend)
        |
        v
   Routers          app/routers/auth.py, app/routers/transactions.py
        |           (HTTP endpoints, status codes, error responses)
        v
   Schemas          app/schemas.py
        |           (Pydantic models: validate input, shape output)
        v
   Auth layer       app/auth.py
        |           (password hashing, JWT creation, get_current_user)
        v
   Models           app/models.py
        |           (SQLAlchemy tables and relationships)
        v
   Database         app/database.py -> PostgreSQL
                    (engine, session, get_db dependency)
```

**Routers** define the endpoints. `routers/auth.py` handles `/auth/register` and `/auth/login`. `routers/transactions.py` handles the CRUD and filter routes under `/transactions`.

**Schemas** are Pydantic models. Input models (`UserCreate`, `TransactionCreate`, `TransactionUpdate`) validate incoming data. Output models (`UserOut`, `TransactionOut`, `Token`) control what the API returns, which is how the hashed password is kept out of responses.

**Auth layer** hashes passwords with bcrypt, creates and decodes JWT tokens, and provides the `get_current_user` dependency. Every protected route depends on it, so a request without a valid token is rejected before any route code runs.

**Models** define two tables, `users` and `transactions`. Each transaction has an `owner_id` foreign key to `users.id`, and a two-way relationship links the tables (`user.transactions` and `transaction.owner`).

**Database layer** creates the SQLAlchemy engine and gives each request its own session through the `get_db` dependency, which closes the session when the request ends. The connection string is read from environment variables, so no credentials are stored in the code.

## Data model

| users | | transactions | |
|---|---|---|---|
| id | primary key | id | primary key |
| username | unique | title | text |
| email | unique | amount | float |
| hashed_password | bcrypt hash | type | income or expense |
| | | category | text |
| | | date | date |
| | | owner_id | foreign key to users.id |

One user has many transactions, and each transaction belongs to exactly one user.

## Authentication flow

1. The user registers at `POST /auth/register`. The password is hashed and the user is saved.
2. The user logs in at `POST /auth/login`. The password is checked against the stored hash.
3. If it matches, the API returns a JWT access token with an expiry time, and the token type `bearer`.
4. The client sends the token in the `Authorization: Bearer <token>` header on every transaction request.
5. `get_current_user` decodes the token, finds the user in the database, and passes that user to the route.

## Authorization and ownership

Ownership is enforced in the database queries, not only in the routes' logic.

- When a transaction is created, its `owner_id` is set from the logged-in user, never from the request body.
- Every query for transactions filters on `owner_id == current_user.id`.
- Requesting another user's transaction returns the same 404 as requesting one that does not exist, so users cannot discover which IDs exist.

## API endpoints

| Method | Endpoint | Protected | Description |
|---|---|---|---|
| POST | `/auth/register` | No | Create an account |
| POST | `/auth/login` | No | Get a JWT access token |
| POST | `/transactions` | Yes | Create a transaction |
| GET | `/transactions` | Yes | List the user's transactions |
| GET | `/transactions/filter` | Yes | Filter by type, category, minimum and maximum amount |
| GET | `/transactions/{id}` | Yes | Get one transaction |
| PUT | `/transactions/{id}` | Yes | Update a transaction |
| DELETE | `/transactions/{id}` | Yes | Delete a transaction |

The `/transactions/filter` route is declared before `/transactions/{id}` so the word "filter" is not mistaken for an ID.

## Testing

Pytest covers the core transaction operations: create, list, get one, update and delete. The tests use FastAPI's `TestClient` with an in-memory SQLite database that replaces the real one through a dependency override, so tests never touch production data.

## Tech stack

FastAPI, SQLAlchemy, PostgreSQL, Pydantic, JWT (PyJWT), bcrypt, Pytest

## Deployment

Deployed on Render with an online PostgreSQL database. The live link will be added here."# Expense_tracker" 
