from .models import PMuser
from rest_framework import serializers


class PMuserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PMuser
        fields = ('id', 'username', 'email', 'phone_number', 'url')
