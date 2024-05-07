from payments.models import Gateway
from rest_framework import serializers


class GatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gateway
        fields = ('id', 'title', 'description', 'avatar')
