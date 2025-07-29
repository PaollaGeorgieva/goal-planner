from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Note(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    goal = GenericForeignKey('content_type', 'object_id')

    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='note_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (for {self.goal})"
