from collections import defaultdict


def group_bookmarks(bookmarks):
    grouped_bookmarks = defaultdict(list)
    for bookmark in bookmarks:
        category = list(bookmark.keys())[0]
        grouped_bookmarks[category].append(bookmark[category])

    return grouped_bookmarks