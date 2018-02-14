from django.utils.text import slugify

def slug_generator(text, model, *args, **kwargs):

    slug = slugify(text)
    if slug.startswith("_") or slug.startswith("-"):
        slug = slug[1:]

    if slug.endswith("_") or slug.endswith("-"):
        slug = slug[:-1]

    tmp_slug = slug
    i = 1
    while model.objects.filter(slug=tmp_slug).exists():
        tmp_slug = slug + "-" + str(i)
        i += 1
    slug = tmp_slug
    return slug
