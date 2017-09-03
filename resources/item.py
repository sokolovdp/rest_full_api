from flask_restful import Resource, reqparse  # return data in JSON format
from flask_jwt import jwt_required
from models.item_model import ItemModel
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import exc


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Price field must float and be present")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Item needs store id")

    @jwt_required()
    def get(self, item_name):
        item = ItemModel.find_by_name(item_name)
        if item:
            return item.json(), 200
        else:
            return {"item": None}, 404

    @jwt_required()
    def post(self, item_name):
        item = ItemModel.find_by_name(item_name)
        data = Item.parser.parse_args()
        if not item:
            item = ItemModel(item_name, data['price'], data['store_id'])   # **data
            try:
                item.save_to_database()
            except sqlalchemy.exc.DatabaseError:
                return {"message": "error - internal database error"}, 500
            else:
                return item.json(), 201  # created
        else:
            return {"message": "error - duplicated item name"}, 400  # bad request

    @jwt_required()
    def delete(self, item_name):
        item = ItemModel.find_by_name(item_name)
        if item:
            try:
                item.delete_from_database()
            except sqlalchemy.exc.DatabaseError:
                return {"message": "error - internal database error"}, 500
        return {"item": "deleted"}, 200

    @jwt_required()
    def put(self, item_name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(item_name)
        if not item:
            item = ItemModel(item_name, data['price'], data['store_id'])   # **data
        else:
            item.change_price(data['price'])
        try:
            item.save_to_database()
        except sqlalchemy.exc.DatabaseError:
            return {"message": "error - internal database error"}, 500
        else:
            return item.json(), 201


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': [item.json() for item in ItemModel.get_all_items()]}
