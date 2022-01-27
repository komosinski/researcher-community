from locust import HttpUser, TaskSet, task


def index(l):
    l.client.get("/")

class UserBehavior(TaskSet):
    tasks = {index: 1}

class WebsiteUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/")
