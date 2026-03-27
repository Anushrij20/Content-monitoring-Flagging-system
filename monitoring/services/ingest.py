import json
from pathlib import Path
from django.utils.dateparse import parse_datetime
from monitoring.models import ContentItem

def load_mock_content():
    path = Path("mock_data/content.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def upsert_content_items(records):
    items = []
    for record in records:
        item, _ = ContentItem.objects.update_or_create(
            external_id=record["external_id"],
            defaults={
                "title": record["title"],
                "body": record["body"],
                "source": record["source"],
                "last_updated": parse_datetime(record["last_updated"]),
            },
        )
        items.append(item)
    return items
