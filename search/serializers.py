
from rest_framework import serializers
from .models import SearchHistory

class SearchSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=255)
    
    def validate_query(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("يجب أن يكون نص البحث مكون من حرفين على الأقل")
        return value

class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ['id', 'query', 'searched_at']
        read_only_fields = ['id', 'searched_at']