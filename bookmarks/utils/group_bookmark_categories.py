from settings.models import Setting


def group_bookmark_categories(categories):
    setting = Setting.objects.first()
    group_size = setting.bookmark_category_group_size if setting else None

    if not group_size:
        return [categories]

    groups = []
    for i in range(0, len(categories), group_size):
        group = categories[i:i + group_size]
        groups.append(group)
    return groups


