from django.db import models

class Message(models.Model):
    """ Class for the actual message to be sent """
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.timestamp}: {self.content}'