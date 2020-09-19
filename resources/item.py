from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT,jwt_required

import sqlite3
from models.item import  ItemModel


class Item(Resource) :


    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Price should not be blank"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Store id  should not be blank"
                        )
    @jwt_required()
    def get(self,name) :

        item = ItemModel.find_by_name(name)
        if item :
            return item.json()
        return {'message' : 'item not found'}, 404



    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message" : "Item deleted"}

    def post(self,name):

        if ItemModel.find_by_name(name):
            return {"message" : "An item with name {} already present".format(name)} , 400
        request_data = Item.parser.parse_args()
        item =  ItemModel(name , **request_data)
        try :
            item.save_to_db()
        except:
            return {"message" , "An error occured while inserting the item"}, 500
        return item.json() , 201

    def put(self,name):


        data = Item.parser.parse_args()
        item  = ItemModel.find_by_name(name)
        if item is None :
            item = ItemModel(name, data['price'], data['store_id'])
        else :
            item.price = data['price']
        item.save_to_db()
        return item.json()




class ItemList(Resource) :
    def get(self):

      #  return { "items" : [item.json() for item in ItemModel.query.all()]  }

        return {"items": list(map(lambda y : y.json() ,ItemModel.query.all()))}