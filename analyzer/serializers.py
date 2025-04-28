from rest_framework import serializers
from .models import QueryLog

class QuerySerializer(serializers.Serializer):
    """
    Serializer for incoming query requests.
    """
    query = serializers.CharField(required=True, help_text="Text message to analyze")

class QueryLogSerializer(serializers.ModelSerializer):
    """
    Serializer for QueryLog model.
    """
    class Meta:
        model = QueryLog
        fields = '__all__'