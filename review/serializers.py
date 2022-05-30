from rest_framework import serializers
from .models import Book,Publisher,BookContributor,Contributor,Review
from django.contrib.auth.models import User
#
# class PublisherSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     website = serializers.URLField()
#     email = serializers.EmailField()
#
# class BookSerializer(serializers.Serializer):
#     title = serializers.CharField()
#     publication_date = serializers.DateField()
#     isbn = serializers.CharField()
#     publisher = PublisherSerializer()


''''
Technique 2
'''
class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['name','website','email']

class BookSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer()
    class Meta:
        model = Book
        fields = ['title','publication_date','isbn','publisher']


class ContributorSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    class Meta:
        model = BookContributor
        fields = ['book','role']


class ContributorSerializer(serializers.ModelSerializer):
    bookcontributor_set = ContributorSerializer(read_only=True,many=True)
    number_contributor = serializers.ReadOnlyField()

    class Meta:
        model = Contributor
        fields = ['first_names','last_names','email','bookcontributor_set','number_contributor']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email']

class ReviewSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    book = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['pk','content','date_created','date_edited','rating','creator','book','book_id']