import time
from . import Model


class Mail(Model):
    def __init__(self, form):
        self.id = None
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.ct = int(time.time())
        self.ut = self.ct
        self.read = False
        self.sender_id = -1
        self.receiver_id = int(form.get('to', -1))

    def set_sender(self, sender_id):
        self.sender_id = sender_id
        self.save()

    def mark_read(self):
        self.read = True
        self.save()
