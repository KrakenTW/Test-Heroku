from PIL import Image


def resize_photo(image_field, size):
    image_file = Image.open(image_field.file)
    fmt = image_file.format.lower()
    image_file.thumbnail(size)
    image_field.file = type(image_field.file)()
    image_file.save(image_field.file, fmt)
    return image_field
