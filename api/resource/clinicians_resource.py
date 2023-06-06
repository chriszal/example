import falcon
import json

import jwt
import datetime
from api.services.clinicians_service import CliniciansService

class CliniaciansResource(object):

    def __init__(self):
        """
        Constructor method to initialize the UserResource class with an instance of UserService.
        """
        self.user_service = CliniciansService()


    def on_get(self, req, resp):
        """
        HTTP GET request method to retrieve a list of all users.
        """
        try:
            resp.status = falcon.HTTP_200
            users = self.user_service.list_users()
            # Convert the list of User objects to a list of dictionary objects
            users_dict = [user.to_dict() for user in users]
            resp.body = json.dumps(users_dict)
        except Exception as e:
            raise falcon.HTTPConflict("User creation conflict", str(e))

    def on_post(self, req, resp):
        """
        HTTP POST request method to create a new user with the given user data.
        """
        try:
            user_data = req.media
            # Create a new user object using the user_service and the provided user data
            user_obj = self.user_service.create_user(**user_data)
            resp.status = falcon.HTTP_201
            resp.body = json.dumps({
                'message': 'User successfully created!',
                'status': 201,
                'data': user_obj.to_dict()
            })
        except Exception as e:
            # If an error occurs while creating the user, return a 409 status code with an error message
            resp.status = falcon.HTTP_409
            resp.body = json.dumps({
                'message': str(e),
                'status': 409,
                'data': {}
            })
            return

   