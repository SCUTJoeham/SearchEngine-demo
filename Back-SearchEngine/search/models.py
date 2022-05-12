from django.db import models


# Create your models here.
class InvertedIndex(models.Model):
    term = models.CharField(max_length=150, db_index=True)
    urllist = models.TextField()


class News(models.Model):
    url = models.CharField(max_length=250, db_index=True)
    title = models.CharField(max_length=250)
    content = models.TextField()
