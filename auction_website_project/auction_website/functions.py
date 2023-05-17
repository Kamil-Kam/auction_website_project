def get_image_path(instance, filename):
    category_name_path = instance.category.category_name
    return f"{category_name_path}/{filename}"


def get_avatars_path(instance, filename):
    return f"avatars/{filename}"
