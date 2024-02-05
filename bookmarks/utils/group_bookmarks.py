from collections import defaultdict


def group_bookmarks(serialized_bookmarks):
    unique_category_ids = set([str(bookmark["category"]) for bookmark in serialized_bookmarks])
    grouped_bookmarks = {category_id: [] for category_id in unique_category_ids}

    for bookmark in serialized_bookmarks:
        category_id = str(bookmark["category"])
        grouped_bookmarks[category_id].append(bookmark)

    return grouped_bookmarks