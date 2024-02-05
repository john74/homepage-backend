def group_by_category(serialized_data):
    unique_category_ids = set([str(item["category"]) for item in serialized_data])
    grouped_data = {category_id: [] for category_id in unique_category_ids}

    for item in serialized_data:
        category_id = str(item["category"])
        grouped_data[category_id].append(item)

    return grouped_data