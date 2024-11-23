from django.db import models

# Create your models here.
# models.py
from django.db import models

class Application(models.Model):
    dsaref_code = models.CharField(max_length=100)
    # Other fields as necessary

    def __str__(self):
        return self.dsaref_code
