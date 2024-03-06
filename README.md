# Handling SIGTERM in Gunicorn
Example of how to handle signals of termination with a custom Gunicorn worker.

## Article
This is a repository was made as reference for the article in my blog:
- [Handling SIGTERM in Gunicorn](https://lucasklassmann.com/devlog/2024-03-05-gunicorn-custom-worker-sigterm/)

## Setup

### With docker-compose
- Build with `docker-compose build`
- Start the `API` with `docker-compose up`

### Just Gunicorn and Python
You can run `Gunicorn` locally, just make sure that:
- Use a recent `Python`, it was tested with `3.10`
- Create a virtual environment
- Install the `requirements.txt`
- Run `gunicorn` command
  - Check `Dockerfile` for an example of how to call `gunicorn`
- You will have to send Gunicorn a signal manually like:
```shell
kill -TERM <Gunicorn PID>
```

>The gunicorn PID can be obtained with `ps aux | grep gunicorn`

## Testing

You can run `service_a_client.py`(which depends on `requests`) or `service_a_client.sh`(which depends on `cURL`)

- Run the client application (It will hang on)
- Cancel the `docker-compose` with `CTRL+C` for gracefully termination (or kill `gunicorn` like mentioned above)
- Check that the client received a HTTP 200 and a custom reason from the `API`


### How to set a custom Gunicorn worker
Use the `-k` parameter and point to the worker `path.module.class`.

Example:
```shell
gunicorn -b 0.0.0.0:8080 --timeout 7200 -w 6 -k service_b.worker.CustomWorker service_b.app:app
```

# License
[Apache 2.0](LICENSE)