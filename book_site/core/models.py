from django.db import models


class Category(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=300, blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    story_line = models.TextField(blank=True, null=True)
    categories = models.ManyToManyField(Category)
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title


class BookContent(models.Model):
    book = models.ForeignKey(Book, related_name='paragraphs', on_delete=models.CASCADE, db_index=True)
    sequence_num = models.IntegerField()
    content = models.TextField()

    class Meta:
        ordering = ['sequence_num']

    def __str__(self):
        return self.content
