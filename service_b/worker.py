import sys
import secrets
from types import FrameType
from gunicorn.workers.sync import SyncWorker
import gunicorn.util as util


class CustomWorker(SyncWorker):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance_id = secrets.token_hex(6)
        self.clients = []

    def _log(self, msg):
        print(f"[CUSTOM WORKER][{self.instance_id}]: {msg}")

    def accept(self, listener):
        client, addr = listener.accept()
        self.clients.append(client)
        client.setblocking(1)
        util.close_on_exec(client)
        self.handle(listener, client, addr)

    def close_clients_gracefully(self, status=200, msg="OK FROM WORKER"):
        self._log(f"closing {len(self.clients)} clients gracefully")
        size = len(msg)
        response_data = (
            f"HTTP/1.1 {status} {msg}\r\nContent-Length: {size}\r\n\r\n{msg}"
        )
        response_data = response_data.encode("utf-8")
        try:
            for _socket in self.clients:
                _socket.sendall(response_data)
                _socket.close()
        except Exception as e:
            print(e)

    def notify_error(self):
        self._log(f"notifying errors")
        if hasattr(self, "wsgi") and self.wsgi:
            if hasattr(self.wsgi, "incomplete_jobs") and isinstance(
                self.wsgi.incomplete_jobs, dict
            ):
                jobs = self.wsgi.incomplete_jobs

                for key, payload in jobs.items():
                    self._log(f"sending notification for job {key}")

    def handle_exit(self, sig: int, frame: FrameType):
        self._log(f"handling signal {sig}")
        self.notify_error()
        self.close_clients_gracefully()
        sys.exit(0)
