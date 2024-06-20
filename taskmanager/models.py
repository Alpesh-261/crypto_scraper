from django.db import models
import uuid
import json

class Job(models.Model):
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    job = models.ForeignKey(Job, related_name='tasks', on_delete=models.CASCADE)
    coin = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='pending')
    data = models.TextField(null=True, blank=True)  # Changed from JSONField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_data(self, data):
        self.data = json.dumps(data)

    def get_data(self):
        if self.data:
            return json.loads(self.data)
        return None
