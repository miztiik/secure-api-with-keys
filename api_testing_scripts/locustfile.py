from locust import HttpUser, task, between


class MyUser(HttpUser):
    wait_time = between(0, 1)

    @task(1)
    def index(self):
        headers = {"X-API-Key": "F9ZufzJTa73OU1V1TEKRn10mfip1q2tG2xjblFCS"}
        self.client.get("/", headers=headers)


# docker run -p 8089:8089 -v $PWD:/mnt/locust locustio/locust -f /mnt/locust/locustfile.py
