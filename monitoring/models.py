from django.db import models

class Keyword(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class ContentItem(models.Model):
    title = models.CharField(max_length=500)
    source = models.CharField(max_length=100)
    body = models.TextField()
    external_id = models.CharField(max_length=255, unique=True)
    last_updated = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Flag(models.Model):
    STATUS_PENDING = "pending"
    STATUS_RELEVANT = "relevant"
    STATUS_IRRELEVANT = "irrelevant"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_RELEVANT, "Relevant"),
        (STATUS_IRRELEVANT, "Irrelevant"),
    ]

    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name="flags")
    content_item = models.ForeignKey(ContentItem, on_delete=models.CASCADE, related_name="flags")
    score = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    suppressed = models.BooleanField(default=False)
    suppressed_at = models.DateTimeField(null=True, blank=True)
    content_last_updated_at_review = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["keyword", "content_item"], name="unique_keyword_content_flag")
        ]



# Create your models here.
