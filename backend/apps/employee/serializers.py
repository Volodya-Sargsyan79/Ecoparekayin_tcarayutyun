from rest_framework import serializers
from . import models

class PersonSerializer(serializers.ManyRelatedField):
    class Meta:
        model = models.Person
        fields = (
            'first_name',
            'last_name',
            'birthday',
            'passport',
            'id_card',
            'hvhh',
            'email',
            'img'
        )