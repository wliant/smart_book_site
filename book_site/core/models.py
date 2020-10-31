from django.db import models


class BookAccess(models.Model):
    view_date = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey("Book", related_name="user_views", on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey("auth.User", related_name="view_histories", on_delete=models.CASCADE, db_index=True)


class Book(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=300, blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    story_line = models.TextField(blank=True, null=True)
    categories = models.ManyToManyField("Category")
    thumbnail = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('author', 'title')


class Review(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    writer = models.CharField(max_length=300)
    content = models.TextField()
    book = models.ForeignKey("Book", related_name="reviews", on_delete=models.CASCADE, db_index=True)

    class Meta:
        ordering = ['-created']


class Category(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.name

    @property
    def book_count(self):
        return Book.objects.filter(categories__id=self.pk).count()


class BookContent(models.Model):
    """
    Many to One relationship with book. i.e. one book has multiple book content.
    Each content represents a paragraph of the book.
    sequence_num track the ordering of the paragraph
    """
    book = models.ForeignKey(Book, related_name='paragraphs', on_delete=models.CASCADE, db_index=True)
    sequence_num = models.IntegerField()
    content = models.TextField()

    class Meta:
        ordering = ['sequence_num']

    def __str__(self):
        return self.content
