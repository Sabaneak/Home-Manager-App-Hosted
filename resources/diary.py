from flask_restful import Resource
from flask import request, Response, jsonify
from models.diary import DiaryModel
from schemas.diary import DiarySchema
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity

diary_schema = DiarySchema()
diary_list_schema = DiarySchema(many=True)

class Diary_Entry(Resource):
    """
    Class to add diary entry
    """
    @classmethod
    @jwt_required
    def post(cls):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            diary = diary_schema.load(body)
            diary.added_by = user_id
            diary.save_to_data()
            return {'msg': "Diary entry was added to diary database"}, 200
        
        except Exception as e:
            return {'msg':str(e)}, 500


class Diary(Resource):
    """
    Class to get, edit or delete a diary entry by id
    Params: name of item (Obtaining by diary/all)
    Output: item is displayed/edited/deleted
    """
    @classmethod
    @jwt_required
    def get(cls, _id):
        try:
            diary = DiaryModel.find_by_id(_id)
            if diary:
                return diary_schema.dump(diary), 200
            return {'msg': "No such diary entry exists"}, 404

        except Exception as e:
            return {'msg':str(e)}, 500

    @classmethod
    @jwt_required
    def put(cls, _id):
        try:
            diary = DiaryModel.find_by_id(_id)
            body = request.get_json()
        
            if not diary:
                return {'msg': "No such diary entry exists"}
            
            given_diary = diary_schema.load(body)
            given_diary.id = diary.id
            given_diary.added_by = diary.added_by
            
            diary.delete_from_data()
            given_diary.save_to_data()
            return {'msg': "Diary has been modified"}, 200

        except Exception as e:
            return {'msg':str(e)}, 500

        
class DiaryList(Resource):
    """
    Class to display all diary entries
    """
    @classmethod
    @jwt_required
    def get(cls):
        try:
            return {'Diary Entries': diary_list_schema.dump(DiaryModel.find_all())}, 200
        except Exception as e:
            return {'msg':str(e)}, 500
