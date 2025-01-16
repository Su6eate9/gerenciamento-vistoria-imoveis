def paginate(data, params):
    page = int(params.get('page', 1))
    limit = int(params.get('limit', 10))
    total_items = len(data)
    total_pages = (total_items + limit - 1) // limit
    start = (page - 1) * limit
    end = start + limit
    return {
        "page": page,
        "total_pages": total_pages,
        "total_items": total_items,
        "items": data[start:end],
    }
