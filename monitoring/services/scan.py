from django.utils import timezone
from monitoring.models import Keyword, Flag
from .ingest import load_mock_content, upsert_content_items
from .matching import compute_match_score

def run_scan():
    records = load_mock_content()
    content_items = upsert_content_items(records)
    keywords = Keyword.objects.all()

    stats = {
        "content_items_processed": len(content_items),
        "flags_created": 0,
        "flags_updated": 0,
        "flags_resurfaced": 0,
        "flags_suppressed": 0,
    }

    for item in content_items:
        for keyword in keywords:
            score = compute_match_score(keyword.name, item.title, item.body)

            if score == 0:
                continue

            flag, created = Flag.objects.get_or_create(
                keyword=keyword,
                content_item=item,
                defaults={
                    "score": score,
                    "status": Flag.STATUS_PENDING,
                    "suppressed": False,
                },
            )

            if created:
                stats["flags_created"] += 1
                continue

            if flag.status == Flag.STATUS_IRRELEVANT and flag.suppressed:
                reviewed_last_updated = flag.content_last_updated_at_review
                if reviewed_last_updated and item.last_updated <= reviewed_last_updated:
                    stats["flags_suppressed"] += 1
                    continue
                else:
                    flag.status = Flag.STATUS_PENDING
                    flag.suppressed = False
                    flag.suppressed_at = None
                    flag.score = score
                    flag.save()
                    stats["flags_resurfaced"] += 1
                    continue

            flag.score = score
            flag.save()
            stats["flags_updated"] += 1

    return stats
