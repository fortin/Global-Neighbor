from django.utils.text import slugify


def generate_unique_slug(model_class, title, slug_field="slug"):
    """
    Generates a unique slug for a given model class based on the title.
    Ensures no collision with existing slugs in the database.
    """
    base_slug = slugify(title)
    slug = base_slug
    counter = 1

    while model_class.objects.filter(**{slug_field: slug}).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug
