from rest_framework import serializers
from shared.response.api_response import ApiResponse

class ApiResponseSerializer(serializers.Serializer):
    """
    Serializer for the standardized ApiResponse structure.
    Compatible with drf-yasg for API documentation.
    """
    data = serializers.JSONField(
        help_text='The response data. Can be any valid JSON structure.',
        allow_null=True,
        required=False
    )
    timestamp = serializers.CharField(
        help_text='ISO 8601 formatted timestamp of when the response was generated.',
        max_length=50
    )
    success = serializers.BooleanField(
        help_text='Indicates whether the request was successful.'
    )
    status_code = serializers.IntegerField(
        help_text='HTTP status code of the response.',
        min_value=100,
        max_value=599
    )
    message = serializers.CharField(
        help_text='Descriptive message about the response.',
        max_length=500
    )
    metadata = serializers.DictField(
        help_text='Additional metadata about the response.',
        required=False,
        allow_empty=True,
        child=serializers.CharField(allow_blank=True)
    )

    def to_representation(self, instance):
        """
        Handle both dataclass instances and dictionary representations.
        """
        if isinstance(instance, ApiResponse):
            return {
                'data': instance.data,
                'timestamp': instance.timestamp,
                'success': instance.success,
                'status_code': instance.status_code,
                'message': instance.message,
                'metadata': instance.metadata
            }
        return super().to_representation(instance)

class ApiResponseWithListSerializer(ApiResponseSerializer):
    """
    ApiResponse serializer for list responses with pagination metadata.
    """
    data = serializers.ListField(
        help_text='List of items',
        child=serializers.DictField()
    )
    
    class PaginationMetadataSerializer(serializers.Serializer):
        page = serializers.IntegerField(help_text='Current page number')
        page_size = serializers.IntegerField(help_text='Number of items per page')
        total_count = serializers.IntegerField(help_text='Total number of items')
        total_pages = serializers.IntegerField(help_text='Total number of pages')
        has_next = serializers.BooleanField(help_text='Whether there is a next page')
        has_previous = serializers.BooleanField(help_text='Whether there is a previous page')
    
    metadata = PaginationMetadataSerializer(help_text='Pagination information')

class ApiErrorResponseSerializer(ApiResponseSerializer):
    """
    ApiResponse serializer specifically for error responses.
    """
    success = serializers.BooleanField(default=False, help_text='Always False for error responses')
    data = serializers.DictField(
        help_text='Error details',
        required=False,
        child=serializers.ListField(child=serializers.CharField())
    )

