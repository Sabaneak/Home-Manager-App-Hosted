from flask_restful import Resource
from flask import request, Response, jsonify
from models.models import UserModel, DiaryModel
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity

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
            user = UserModel.objects.get(id=user_id)
            diary = DiaryModel(**body, added_by=user)
            diary.save()
            user.update(push__diary=diary)
            user.save()
            return {'msg': "Diary entry was added to database"}, 200
        
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
            user_id = get_jwt_identity()
            diary = DiaryModel.objects(id=_id, added_by=user_id).exclude('added_by').to_json()
            if not diary:
                return {'msg': 'Diary entry does not exist'}, 400
            return Response(diary, mimetype="application/json", status=200)

        except Exception as e:
            return {'msg':str(e)}, 500

    @classmethod
    @jwt_required
    def put(cls, _id):
        try:
            user_id = get_jwt_identity()
            diary = DiaryModel.objects.get(id=_id, added_by=user_id)
            if not diary:
                return {'msg': 'Diary entry does not exist'}, 400
            
            body = request.get_json()
            DiaryModel.objects.get(id=_id).update(**body)
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
            user_id = get_jwt_identity()
            diary = DiaryModel.objects(added_by=user_id).exclude('added_by').to_json()
            return Response(diary, mimetype="application/json", status=200)
        
        except Exception as e:
            return {'msg':str(e)}, 500
