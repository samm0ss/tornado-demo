"""
Test script to locally mock POST requests to /events endpoint
"""
import http.client
import pathlib
import time

payload = '{"events": [{"id": "id", "dt": "2021-02-02T21:34:58+00:00", "record": {"x": 0, "y": 0, "name": "name"}}, {"id": "id", "dt": "2021-02-02T21:34:58+00:00", "record": {"x": 1, "y": 1, "name": "name"}}, {"id": "id", "dt": "2021-02-02T21:34:58+00:00", "record": {"x": 2, "y": 2, "name": "name"}}, {"id": "id", "dt": "2021-02-02T21:34:58+00:00", "record": {"x": 3, "y": 3, "name": "name"}}, {"id": "id", "dt": "2021-02-02T21:34:58+00:00", "record": {"x": 4, "y": 4, "name": "name"}}, {"id": "id", "dt": "2021-02-02T21:34:58+00:00", "record": {"x": 5, "y": 5, "name": "name"}}, {"id": "id", "dt": "2021-02-02T21:34:58+00:00", "record": {"x": 6, "y": 6, "name": "name"}}, {"id": "id", "dt": "2021-02-02T21:34:58+00:00", "record": {"x": 7, "y": 7, "name": "name"}}, {"id": "id", "dt": "2021-02-02T21:34:58+00:00", "record": {"x": 8, "y": 8, "name": "name"}}, {"id": "id", "dt": "2021-02-02T21:34:58+00:00", "record": {"x": 9, "y": 9, "name": "name"}}]}'  # noqa


if __name__ == "__main__":
    conn = http.client.HTTPConnection("localhost", 3000)
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": pathlib.Path("secret.txt").read_text()}
    while True:
        conn.request("POST", "/events", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        time.sleep(1)
