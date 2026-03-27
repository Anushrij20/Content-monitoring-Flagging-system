from rest_framework import serializers
from .models import Keyword, Flag


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ["id", "name", "created_at", "updated_at"]


class FlagSerializer(serializers.ModelSerializer):
    keyword_name = serializers.CharField(source="keyword.name", read_only=True)
    content_title = serializers.CharField(source="content_item.title", read_only=True)
    content_source = serializers.CharField(source="content_item.source", read_only=True)
    content_body = serializers.CharField(source="content_item.body", read_only=True)
    content_last_updated = serializers.DateTimeField(source="content_item.last_updated", read_only=True)

    class Meta:
        model = Flag
        fields = [
            "id",
            "keyword",
            "keyword_name",
            "content_item",
            "content_title",
            "content_source",
            "content_body",
            "content_last_updated",
            "score",
            "status",
            "suppressed",
            "created_at",
            "updated_at",
        ]


class FlagStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flag
        fields = ["status"]
