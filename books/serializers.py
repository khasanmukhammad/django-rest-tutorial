from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Book

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'title', 'subtitle', 'content', 'author', 'isbn', 'price')


    def validate(self, data):
        title = data.get('title', None)
        author = data.get('author', None)

        # check title of it contains only alphabetical chars
        if not title.isalpha():
            raise ValidationError(
                {
                    "status": False,
                    "message": "Title must be alphanumeric"
                }
            )

        #check title and author from database existence
        if Book.objects.filter(title=title, author=author).exists():
            raise ValidationError(
                {
                    "status": False,
                    "message": "Title and author already exists"
                }
            )

        return data

    def validate_price(self, price):
        if price <= 0:
            raise ValidationError(
                {
                    "status": False,
                    "message": "Price must be greater than 0"
                }
            )