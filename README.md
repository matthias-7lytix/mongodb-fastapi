# FastAPI Users and MongoDB

This is a small sample project to use [**FastAPI Users**](https://fastapi-users.github.io/fastapi-users/) with [**MongoDB**](https://www.mongodb.com/).

This project uses

* [**MongoDB**](https://www.mongodb.com/) as the main user database,
* [**Redis** cache](https://redis.io/) as FastAPI's [authentication strategy](https://fastapi-users.github.io/fastapi-users/10.1/configuration/authentication/strategies/redis/), and
* [**Mongo Express**](https://github.com/mongo-express/mongo-express) as admin interface for the MongoDB.

To set up all the required components, you can use [**Docker**](https://www.docker.com/) and [**docker compose**](https://docs.docker.com/compose/). Simply run

```bash
docker compose -f docker-compose.yml up -d --build 
```

This will start 4 containers:

* **app**: This contains the current working directory (with the project's code) as a mounted directory `/app`.
* **mongodb**: the MongoDB, running on port 27017 (mapped to host's port 27017).
* **mongo-express**: the Mongo Express admin interface running on port 8081. _Note the Mongo Express' port is mapped to the host's port **8080**._!
* **redis**: the Redis cache running on port 6379 (mapped to host's port 6379).

To start the app on host's port 8000 run

```bash
docker exec app uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## References

Part of this project was based on the [MongoDB with FastAPI](https://github.com/mongodb-developer/mongodb-with-fastapi) project. The example code therein for handling a stundent's database has been moved to an outdated branch [`student`](https://github.com/matthias-7lytix/mongodb-fastapi/tree/student).
