# Cloud Computing Midterm Project

Two Flask apps + Redis, all running in Docker containers.

- **App 1** (port 5000) — a feedback form that saves messages to Redis and tracks visits
- **App 2** (port 5001) — a dashboard that reads those stats from Redis and displays them

They talk to each other through a shared Redis instance on a Docker bridge network. Redis data is saved to a volume so it survives restarts.

## How to run

Make sure Docker Desktop is open, then:

```bash
docker-compose up --build
```

- Feedback form → http://localhost:5000
- Dashboard → http://localhost:5001

```bash
docker-compose down      # stop
docker-compose down -v   # stop + wipe data
```

## Structure

```
app1/   → feedback collector
app2/   → dashboard
docker-compose.yml
```
