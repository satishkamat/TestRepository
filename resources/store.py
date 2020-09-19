from flask_restful import Resource, Api


from models.store import  StoreModel


class Store(Resource) :





    def get(self,name) :

        store = StoreModel.find_by_name(name)
        if store :
            return store.json()
        return {'message' : 'store not found'}, 404



    def delete(self,name):
        item = StoreModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message" : "StoreItem deleted"}

    def post(self,name):

        if StoreModel.find_by_name(name):
            return {"message" : "An store with name {} already present".format(name)} , 400

        store =  StoreModel(name)
        try :
            store.save_to_db()
        except:
            return {"message" , "An error occured while inserting the store"}, 500
        return store.json() , 201


class StoreList(Resource) :
    def get(self):
        return {'stores' :  [store.json() for store in StoreModel.query.all()]}
