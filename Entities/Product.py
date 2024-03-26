from datetime import datetime


class Picture:
    def __init__(self, url):
        self.url = url

    def save_to_db(self, pictures_collection):
        picture_data = {'url': self.url}
        result = pictures_collection.insert_one(picture_data)
        return result.inserted_id


class Product:
    def __init__(self, title, description, pictures=None, _id=None, created_at=None):
        self._id = _id
        self.title = title
        self.description = description
        self.pictures = pictures or []
        self.created_at = created_at or datetime.now()

    def save_to_db(self, products_collection):
        product_data = {
            'title': self.title,
            'description': self.description,
            'pictures': self.pictures
        }
        result = products_collection.insert_one(product_data)
        return result.inserted_id
