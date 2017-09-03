from db_alchemy import db


class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, item_name, item_price, store_id):
        self.name = item_name
        self.price = item_price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price, 'store_id': self.store_id}

    def change_price(self, new_price):
        self.price = new_price

    @classmethod
    def find_by_name(cls, item_name):
        return cls.query.filter_by(name=item_name).first()

    def save_to_database(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_database(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_items(cls):
        return cls.query.all()
