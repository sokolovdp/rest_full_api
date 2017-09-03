from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.item import Item, ItemList
from resources.user import UserRegister
from resources.store import Store, StoreList
from security import authenticate, identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'sokolov'
api = Api(app)

jwt = JWT(app, authentication_handler=authenticate, identity_handler=identity)  # /auth
api.add_resource(Store, '/stores/<string:store_name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/items/<string:item_name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/signup')

if __name__ == '__main__':
    from db_alchemy import db

    db.init_app(app)
    @app.before_first_request
    def create_tables():
        db.create_all()

    app.run(port=5000, debug=True)
