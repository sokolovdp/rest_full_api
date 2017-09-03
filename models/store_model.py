from db_alchemy import db
from models.item_model import ItemModel


class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    items = db.relationship('ItemModel', lazy='dynamic')  # relation will be built during getting items from db

    def __init__(self, item_name):
        self.name = item_name

    def json(self):
        return {'name': self.name, 'id': self.id, 'items': [item.json() for item in self.items.all()]}

    def add_item(self, new_item):
        self.items.append(new_item)

    @classmethod
    def find_by_name(cls, item_name):
        return cls.query.filter_by(name=item_name).first()

    def save_to_database(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_database(self):
        # delete all items with store_id
        for item in ItemModel.query.filter_by(store_id=self.id).all():
            item.delete_from_database()
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_stores(cls):
        return cls.query.all()
