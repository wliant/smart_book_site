from core.utils import decode_base64_file
from core.models import Book, BookContent, Category
from rest_framework import serializers


class MigrationSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    author = serializers.CharField(required=False, allow_blank=True, max_length=300)
    categories = serializers.ListField(
        child=serializers.CharField(max_length=300)
    )
    img = serializers.CharField(max_length=None)
    paragraphs = serializers.ListField(
        child=serializers.CharField(max_length=None, allow_blank=True, required=False)
    )
    storyline = serializers.CharField(max_length=None)
    title = serializers.CharField(max_length=300)
    total_pages = serializers.CharField(max_length=10)
    views = serializers.CharField(max_length=20)

    def create(self, validated_data):
        pars = validated_data.get('paragraphs')
        cats = validated_data.get('categories')
        cats_obj = []

        for cat in cats:
            try:
                c = Category.objects.get(name=cat)
            except Category.DoesNotExist:
                c = Category.objects.create(name=cat)
            cats_obj.append(c)
        v = validated_data.get("views")
        if v:
            try:
                v = int(v.replace(",", ""))
            except:
                v = None

        book = Book.objects.create(title=validated_data.get("title"),
                                   thumbnail=decode_base64_file(validated_data.get("img")),
                                   story_line=validated_data.get("storyline"),
                                   author=validated_data.get("author"),
                                   views=v
                                   )
        for c in cats_obj:
            book.categories.add(c)

        counter = 1
        for par in pars:
            BookContent.objects.create(book=book, sequence_num=counter, content=par)
            counter += 1
        return book