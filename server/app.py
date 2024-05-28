# from flask import Flask, request, jsonify, make_response
# from flask_migrate import Migrate
# from flask_restful import Resource, Api, reqparse
# from models import db, User, File, Folder,Share,StarredItem,TrashItem
# from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token,unset_jwt_cookies
# from flask_cors import CORS, cross_origin
# from flask_bcrypt import Bcrypt
# from cloudinary.uploader import upload
# from cloudinary.utils import cloudinary_url



# app = Flask(__name__)
# CORS(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cloudstore.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.json.compact = False

# app.secret_key = 'secret key'
# app.config['JWT_SECRET_KEY'] = "b'\x03\xa3\x8c\xb3\n\xf4\x16aFh\xc5'"

# db.init_app(app)

# migrate = Migrate(app, db)
# api = Api(app)
# jwt = JWTManager(app)
# bcrypt = Bcrypt(app)


# class UserRegister(Resource):
#     @cross_origin()
#     def post (self):
#         data = request.get_json()
#         print(data)
#         username = data.get("username")
#         email = data.get("email")
#         password = str(data.get("password"))
#         image_url = data.get("image_url")
        
        
#         print(f"This is {data}")
        
#         #check if the user exists
#         user_exists = User.query.filter(User.username==username) 
        
#         # if user_exists:
#         #     return jsonify({"Error":"User exists"})
        
#         # if password and confirm_password doesn't match
#         # if password != confirm_password:
#         #     return jsonify({"Error":"Password and confirm_password don't match"})
        
#         # creating encrypted passwords
#         hashed_password = bcrypt.generate_password_hash(password)
       
        
#         access_token = create_access_token(identity=username)
#         # User.access_token = access_token
        
#         new_user = User(
#            username = username,
#            email = email,
#            password = hashed_password,
#            image_url = image_url
            
#         )
#         db.session.add(new_user)
#         db.session.commit()
        
#         return jsonify({
#             "id":"new_user.id",
#             "username":"new_user.username",
#             "access_token":access_token
            
#         })
        
# api.add_resource(UserRegister,"/user/register")        


# class UserLogin(Resource):
#     def post(self):
#         data = request.get_json()
#         print(data)
        
#         email = data.get("email")
#         password = str(data.get("password"))

#         user = User.query.filter_by(email=email).first()

#         if user is None:
#             return jsonify({'error': 'Unauthorized'}), 401

#         if not bcrypt.check_password_hash(user.password, password):
#             return jsonify({'error': 'Unauthorized, incorrect password'}), 401
        
#         access_token = create_access_token(identity=email)
#         user.access_token = access_token


#         return jsonify({
#             "id": user.id,
#             "email": user.email,
#             "access_token": user.access_token,
#             "username": user.username,
#             "image_url":user.image_url
        
#         })
        
# api.add_resource(UserLogin,"/user/login")         
    




# class Logout(Resource):
#     @jwt_required()
#     def post(self):
#         unset_jwt_cookies()
#         return{"message":"Successfully logged out"} 
    
# api.add_resource(Logout,"/user/logout")     


# class Users(Resource):
#     def get(self):
#         users = [user.to_dict(only=('id', 'username', 'email',"image_url")) for user in User.query.all()]
#         print("im a user", users)
#         return make_response(jsonify(users),200)
    
# api.add_resource(Users,"/users")     

# class UserByID(Resource):

#     def get(self,id):
#         user = User.query.filter(User.id==id).first()

#         if user:
#             return make_response(jsonify(user.to_dict(only=("id","username","email","image_url"))),200) 

#     def patch(self,id):

#         data = request.get_json()

#         user = User.query.filter(User.id==id).first()

#         for attr in data:
#             setattr(user,attr,data.get(attr)) 

#         db.session.add(user)
#         db.session.commit()

#         return make_response(user.to_dict(only=("id","email","username","files","folders",)),200)

#     def delete(self,id):

#         user = User.query.filter(User.id==id).first()

#         if user:
#             db.session.delete(user)
#             db.session.commit()
#             return make_response("",204)
#         else:
#             return make_response(jsonify({"error":"User not found"}),404) 
        
# api.add_resource(UserByID,"/users/<int:id>")    

# class Folders(Resource):
#      def post(self):
#         data =  request.get_json()
        
       
        
#         try:
#             new_folder = Folder(
#                 folder_name= data.get('folder_name'),
#                 parent_folder_id = data.get('parent_folder_id'),
#                 user_id = data.get('user_id'),
                
#             )  
#             db.session.add(new_folder)
#             db.session.commit() 
            
#         except ValueError:
#             return make_response(jsonify({"error":["validation errors"]}))    
        
#         return make_response(new_folder.to_dict(only=("parent_folder_id","user_id","user.username","folder_name")),201)
# api.add_resource(Folders,"/folders")     

# class FolderByUser(Resource):
#     def get(self, id):
#         folders = [folder.to_dict(only=("id", "folder_name", "user_id", "user.username")) for folder in Folder.query.filter(Folder.user_id == id,Folder.is_delete == 0)]

#         return make_response(folders, 200)
    
    

# api.add_resource(FolderByUser, "/foldersuser/<int:id>")


        
        
    

# class TrashFolders(Resource):
#     def get(self, id):
#         folders = [folder.to_dict(only=("id", "folder_name", "user_id", "user.username")) for folder in Folder.query.filter(Folder.user_id == id,Folder.is_delete == 1)]

#         return make_response(folders, 200)

# api.add_resource(TrashFolders, "/trashfolders/<int:id>")

# class FolderByID(Resource):
    
#     def get(self,id):
#         folder = Folder.query.filter(Folder.id==id).first()

#         if folder:
#             return make_response(jsonify(folder.to_dict(only=("id","folder_name","user_id","user.username"))),200)
#         else:
#             return make_response(jsonify({"error":"Folder not found"}))
        
#     def patch(self,id):

#         data = request.get_json()

#         folder = Folder.query.filter(Folder.id==id).first()

#         for attr in data:
#             setattr(folder,attr,data.get(attr))

#         db.session.add(folder)
#         db.session.commit()

#         return make_response(folder.to_dict(only=("id","folder_name","user_id","user.username")),200) 
    
#     def delete(self,id):
#         folder = Folder.query.filter(Folder.id==id).first()

#         if folder:
#             db.session.delete(folder)
#             db.session.commit()
#             return make_response("",204)
#         else:
#             return make_response(jsonify({"error":"User not found"}),404)
        
        
# api.add_resource(FolderByID,"/folders/<int:id>") 



# # class FolderByID(Resource):
    
    
# #     def get(self,id):
# #         folder = Folder.query.filter(Folder.id==id).first()

# #         if folder:
# #             return make_response(jsonify(folder.to_dict(only=("id","folder_name","user_id","user.username"))),200)
# #         else:
# #             return make_response(jsonify({"error":"Folder not found"}))
    
# #     def patch(self, id):
# #         data = request.get_json()[0]
# #         folder = Folder.query.filter(Folder.id == id).first()

# #         if folder:
# #             # Update folder attributes
# #             for attr in data:
# #                 setattr(folder, attr, data.get(attr))
            
# #             # If 'path' is being updated, ensure it's a Cloudinary URL
# #             if 'path' in data:
# #                 # Validate that the URL is a Cloudinary URL
# #                 if not data['path'].startswith('https://res.cloudinary.com'):
# #                     return make_response(jsonify({"error": "Invalid Cloudinary URL"}), 400)

# #             db.session.commit()
# #             return make_response(folder.to_dict(only=("id", "folder_name", "user_id", "user.username")), 200)
# #         else:
# #             return make_response(jsonify({"error": "Folder not found"}), 404)
    
# #     def delete(self, id):
# #         folder = Folder.query.filter(Folder.id == id).first()

# #         if folder:
# #             # If 'path' represents a Cloudinary URL, additional handling may be needed
# #             if folder.path.startswith('https://res.cloudinary.com'):
# #                 # Extract public ID from Cloudinary URL
# #                 public_id = cloudinary_url(folder.path)[0]
# #                 # Additional handling for Cloudinary URL deletion
# #                 # (e.g., removing associated files from Cloudinary)
# #                 # cloudinary.uploader.destroy(public_id)
            
# #             db.session.delete(folder)
# #             db.session.commit()
# #             return make_response("", 204)
# #         else:
# #             return make_response(jsonify({"error": "Folder not found"}), 404)
# # api.add_resource(FolderByID,"/folders/<int:id>")

# class Files(Resource):
    
    
#     def post(self):
#         data = request.get_json()
        
#         # Handle file upload to Cloudinary
#         uploaded_file = upload(data.get('file'))  # Assuming the file is in the 'file' field of the JSON payload
        
#         try:
#             new_file = File(
#                 filename=data.get('filename'),
#                 file_type=data.get("file_type"),
#                 size=data.get("size"),
#                 path=uploaded_file['url'],  # Use the Cloudinary URL of the uploaded file
#                 folder_id=data.get("folder_id"),
#                 user_id=data.get('user_id')
#             )  
#             db.session.add(new_file)
#             db.session.commit() 
            
#         except ValueError:
#             return make_response(jsonify({"error": ["validation errors"]}))    
        
#         return make_response(new_file.to_dict(only=("filename", "file_type", "user.username", "folder_id", "path", "size", "user_id")), 201)

    
    
    
# api.add_resource(Files,"/files")  




# class FileByFolder(Resource):
#     def get(self,id):
#         files = [files.to_dict(only=("id","filename","file_type","size","path","user.username")) for files in File.query.filter(File.folder_id==id)]
               
        
#         return make_response(files,200)
    
# api.add_resource(FileByFolder,"/filefolder/<int:id>")    

# class FileByUser(Resource):
#     def get(self, id):
#         files = [file.to_dict(only=("id", "filename", "file_type", "size", "path", "user.username")) for file in File.query.filter(File.user_id == id,File.is_delete==0)]

#         return make_response(files, 200)

# api.add_resource(FileByUser, "/fileuser/<int:id>")

# class FileByFileName(Resource):
#     def get(self,name):
#         file = File.query.filter(File.filename==name).first()

#         if file:
#             return make_response(jsonify(file.to_dict(only=("id","filename","file_type","size","path","user.username"))),200)
#         else:
#             return make_response(jsonify({"error":"Folder not found"}))
        
# api.add_resource(FileByFileName,"/filebyfilename/<string:name>")        
    

# class MoveToTrash(Resource):
#     def put(self, id):
#         file = File.query.get(id)
#         if not file:
#             return {"error": "File not found"}, 404

#         file.is_delete = True

#         try:
#             db.session.commit()
#             return {"message": "File moved to trash successfully"}, 200
#         except Exception as e:
#             db.session.rollback()
#             return {"error": str(e)}, 500

# api.add_resource(MoveToTrash, '/move-to-trash/<int:id>')



# class DeleteFile(Resource):
#     def delete(self, id):
#         file = File.query.get(id)
#         if not file:
#             return {"error": "File not found"}, 404

#         db.session.delete(file)
#         db.session.commit()
#         return {"message": "File deleted successfully"}, 200

# api.add_resource(DeleteFile, '/deletefiles/<int:id>')



# class TrashFiles(Resource):
#     def get(self, id):
#         files = [file.to_dict(only=("id", "filename", "file_type", "size", "path", "user.username")) for file in File.query.filter(File.user_id == id,File.is_delete==1)]

#         return make_response(files, 200)

# api.add_resource(TrashFiles, "/trashfiles/<int:id>")   
    
 
# class FileByID(Resource):
    
#     def get(self,id):
#         file = File.query.filter(File.id==id).first()

#         if file:
#             return make_response(jsonify(file.to_dict(only=("id","filename","file_type","size","path","user.username"))),200)
#         else:
#             return make_response(jsonify({"error":"Folder not found"}))
        
#     def patch(self,id):

#         data = request.get_json()

#         file = File.query.filter(File.id==id).first()

#         if file:
#             # Update file attributes
#             for attr in data:
#                 setattr(file, attr, data.get(attr))
            
#             # If 'path' is being updated, ensure it's a Cloudinary URL
#             if 'path' in data:
#                 # Validate that the URL is a Cloudinary URL
#                 if not data['path'].startswith('https://res.cloudinary.com'):
#                     return make_response(jsonify({"error": "Invalid Cloudinary URL"}), 400)

#             db.session.commit()
#             return make_response(file.to_dict(only=("id", "filename", "file_type", "size", "path", "user.username")), 200)
#         else:
#             return make_response(jsonify({"error": "File not found"}), 404)
    
#     def delete(self,id):
#         file = File.query.filter(File.id==id).first()

#         if file:
#             # Delete file from Cloudinary if 'path' represents a Cloudinary URL
#             if file.path.startswith('https://res.cloudinary.com'):
#                 # Extract public ID from Cloudinary URL
#                 public_id = cloudinary_url(file.path)[0]
#                 # Delete file from Cloudinary
#                 cloudinary.uploader.destroy(public_id)
            
#             db.session.delete(file)
#             db.session.commit()
#             return make_response("", 204)
#         else:
#             return make_response(jsonify({"error": "File not found"}), 404)
        
        
# api.add_resource(FileByID,"/files/<int:id>")     
        
# class Shares(Resource):
#     def get(self):
#         shares = [share.to_dict(only=("file.size","file_id","share_type","user_id","shared_with_user_email","user.username")) for share in Share.query.all()]
#         return make_response(shares,200)
    
#     def post(self):
#         data =  request.get_json()
        
       
        
#         try:
#             new_share = Share(
#                 share_type= data.get('share_type'),
#                 user_id = data.get('user_id'),
#                 shared_with_user_email= data.get("shared_with_user_email"),
#                 file_id = data.get("file_id")
                
#             )  
#             db.session.add(new_share)
#             db.session.commit() 
            
#         except ValueError:
#             return make_response(jsonify({"error":["validation errors"]}))    
        
#         return make_response(new_share.to_dict(only=("file.size","file.path","file_id","share_type","user_id","shared_with_user_email","user.username")),201)
    
# api.add_resource(Shares,"/shares")

# class ShareByID(Resource):
#     def get(self,id):
#         share = Share.query.filter(Share.id==id).first()

#         if share:
#             return make_response(jsonify(share.to_dict(only=("file.size","file.path","file_id","share_type","user_id","shared_with_user_email","user.username"))),200)
#         else:
#             return make_response(jsonify({"error":"Shares files not found"}))
        
#     def patch(self,id):

#         data = request.get_json()

#         share = Share.query.filter(Share.id==id).first()

#         for attr in data:
#             setattr(share,attr,data.get(attr))

#         db.session.add(share)
#         db.session.commit()

#         return make_response(share.to_dict(only=("file.size","file.path","file_id","share_type","user_id","shared_with_user_email","user.username")),200) 
    
#     def delete(self,id):
#         share = Share.query.filter(Share.id==id).first()

#         if share:
#             db.session.delete(share)
#             db.session.commit()
#             return make_response("",204)
#         else:
#             return make_response(jsonify({"error":"Shared file not found"}),404)
        
        
# api.add_resource(ShareByID,"/shares/<int:id>")     


# class StarredItems(Resource):
#     def get(self):
#         starred_items= [starred.to_dict() for starred in StarredItem.query.all()]
#         return make_response(starred_items,200)
    
#     def post(self):
#         data =  request.get_json()
        
       
        
#         try:
#             starred_item = StarredItem(
#                 file_id = data.get("file_id"),
#                 folder_id = data.get("folder_id"),
#                 item_type = data.get("item_type"),
#                 user_id = data.get("user_id")
                
#             )  
#             db.session.add(starred_item)
#             db.session.commit() 
            
#         except ValueError:
#             return make_response(jsonify({"error":["validation errors"]}))    
        
#         return make_response(starred_item.to_dict(only=("id","file_id","item_type","user_id")),201)
    
# api.add_resource(StarredItems,"/starreditems")   

# class StarredItemByID(Resource):
#    def delete(self,id):
#         starred_item = StarredItem.query.filter(StarredItem.id==id).first()

#         if starred_item:
#             db.session.delete(starred_item)
#             db.session.commit()
#             return make_response("",204)
#         else:
#             return make_response(jsonify({"error":"Item not found"}),404)
        
# api.add_resource(StarredItemByID,"/starreditem/<int:id>")    

# class TrashItems(Resource):
#     def get(self):
#         trash_item = [trash.to_dict() for trash in TrashItem.query.all()]
#         return make_response(trash_item,200)   
    
#     def post(self):
#         data =  request.get_json()
        
       
        
#         try:
#             trash_item = TrashItem(
#                 file_id = data.get("file_id"),
#                 folder_id = data.get("folder_id"),
#                 item_type = data.get("item_type"),
#                 user_id = data.get("user_id")
                
#             )  
#             db.session.add(trash_item)
#             db.session.commit() 
            
#         except ValueError:
#             return make_response(jsonify({"error":["validation errors"]}))    
        
#         return make_response(trash_item.to_dict(only=("id","file_id","item_type","user_id")),201)

# api.add_resource(TrashItems,"/trashitems")               
        
        
# class TrashItemByID(Resource):
#     def delete(self,id):
#         trash_item = TrashItem.query.filter(TrashItem.id==id).first()

#         if trash_item:
#             db.session.delete(trash_item)
#             db.session.commit()
#             return make_response("",204)
#         else:
#             return make_response(jsonify({"error":"Item not found"}),404)
        
# api.add_resource(TrashItemByID,"/trashitem/<int:id>")
            
        
        
                
        
        

# if __name__ == "__main__":
#     app.run(port=5555,debug=True)        

from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Resource, Api, reqparse
from models import db, User, File, Folder,Share,StarredItem,TrashItem
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token,unset_jwt_cookies
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
# from cloudinary.uploader import upload
# from cloudinary.utils import cloudinary_url



app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cloudstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.json.compact = False

app.secret_key = 'secret key'
app.config['JWT_SECRET_KEY'] = "b'\x03\xa3\x8c\xb3\n\xf4\x16aFh\xc5'"

db.init_app(app)

migrate = Migrate(app, db)
api = Api(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)


class UserRegister(Resource):
    @cross_origin()
    def post (self):
        data = request.get_json()
        print(data)
        username = data.get("username")
        email = data.get("email")
        password = str(data.get("password"))
        image_url = data.get("image_url")
        
        
        print(f"This is {data}")
        
        #check if the user exists
        user_exists = User.query.filter(User.username==username) 
        
        # if user_exists:
        #     return jsonify({"Error":"User exists"})
        
        # if password and confirm_password doesn't match
        # if password != confirm_password:
        #     return jsonify({"Error":"Password and confirm_password don't match"})
        
        # creating encrypted passwords
        hashed_password = bcrypt.generate_password_hash(password)
       
        
        access_token = create_access_token(identity=username)
        # User.access_token = access_token
        
        new_user = User(
           username = username,
           email = email,
           password = hashed_password,
           image_url = image_url
            
        )
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "id":"new_user.id",
            "username":"new_user.username",
            "access_token":access_token,
            "token":access_token
            
        })
        
api.add_resource(UserRegister,"/user/register")        


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        
        email = data.get("email")
        password = str(data.get("password"))

        user = User.query.filter_by(email=email).first()

        if user is None:
            return jsonify({'error': 'Unauthorized'}), 401

        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({'error': 'Unauthorized, incorrect password'}), 401
        
        access_token = create_access_token(identity=email)
        user.access_token = access_token


        return jsonify({
            "id": user.id,
            "email": user.email,
            "access_token": user.access_token,
            "username": user.username,
            "image_url":user.image_url
        
        })
        
api.add_resource(UserLogin,"/user/login")         
    




class Logout(Resource):
    @jwt_required()
    def post(self):
        unset_jwt_cookies()
        return{"message":"Successfully logged out"} 
    
api.add_resource(Logout,"/user/logout")     


class Users(Resource):
    def get(self):
        users = [user.to_dict(only=('id', 'username', 'email',"image_url")) for user in User.query.all()]
        print("im a user", users)
        return make_response(jsonify(users),200)
    
api.add_resource(Users,"/users")     

class UserByID(Resource):

    def get(self,id):
        user = User.query.filter(User.id==id).first()

        if user:
            return make_response(jsonify(user.to_dict(only=("id","username","email","image_url"))),200) 

    def patch(self,id):

        data = request.get_json()

        user = User.query.filter(User.id==id).first()

        for attr in data:
            setattr(user,attr,data.get(attr)) 

        db.session.add(user)
        db.session.commit()

        return make_response(user.to_dict(only=("id","email","username","files","folders",)),200)

    def delete(self,id):

        user = User.query.filter(User.id==id).first()

        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response("",204)
        else:
            return make_response(jsonify({"error":"User not found"}),404) 
        
api.add_resource(UserByID,"/users/<int:id>")    

class Folders(Resource):
     def post(self):
        data =  request.get_json()
        
       
        
        try:
            new_folder = Folder(
                folder_name= data.get('folder_name'),
                parent_folder_id = data.get('parent_folder_id'),
                user_id = data.get('user_id'),
                
            )  
            db.session.add(new_folder)
            db.session.commit() 
            
        except ValueError:
            return make_response(jsonify({"error":["validation errors"]}))    
        
        return make_response(new_folder.to_dict(only=("parent_folder_id","user_id","user.username","folder_name")),201)
api.add_resource(Folders,"/folders")     

class FolderByUser(Resource):
    def get(self, id):
        folders = [folder.to_dict(only=("id", "folder_name", "user_id", "user.username")) for folder in Folder.query.filter(Folder.user_id == id,Folder.is_delete == 0)]

        return make_response(folders, 200)
    
api.add_resource(FolderByUser, "/foldersuser/<int:id>")    
    
class FolderByFolderName(Resource):
   def get(self,name):
        folder = Folder.query.filter(Folder.folder_name==name).first()

        if folder:
            return make_response(jsonify(folder.to_dict(only=("id","folder_name","user_id","user.username"))),200)
        else:
            return make_response(jsonify({"error":"Folder not found"}))    
        
api.add_resource(FolderByFolderName,"/folderbyfoldername/<string:name>")          
    
    



class TrashFolders(Resource):
    def get(self, id):
        folders = [folder.to_dict(only=("id", "folder_name", "user_id", "user.username")) for folder in Folder.query.filter(Folder.user_id == id,Folder.is_delete == 1)]

        return make_response(folders, 200)

api.add_resource(TrashFolders, "/trashfolders/<int:id>")

class FolderByID(Resource):
    
    def get(self,id):
        folder = Folder.query.filter(Folder.id==id).first()

        if folder:
            return make_response(jsonify(folder.to_dict(only=("id","folder_name","user_id","user.username"))),200)
        else:
            return make_response(jsonify({"error":"Folder not found"}))
        
    def patch(self,id):

        data = request.get_json()

        folder = Folder.query.filter(Folder.id==id).first()

        for attr in data:
            setattr(folder,attr,data.get(attr))

        db.session.add(folder)
        db.session.commit()

        return make_response(folder.to_dict(only=("id","folder_name","user_id","user.username")),200) 
    
    def delete(self,id):
        folder = Folder.query.filter(Folder.id==id).first()

        if folder:
            db.session.delete(folder)
            db.session.commit()
            return make_response("",204)
        else:
            return make_response(jsonify({"error":"User not found"}),404)
        
        
api.add_resource(FolderByID,"/folders/<int:id>") 



# class FolderByID(Resource):
    
    
#     def get(self,id):
#         folder = Folder.query.filter(Folder.id==id).first()

#         if folder:
#             return make_response(jsonify(folder.to_dict(only=("id","folder_name","user_id","user.username"))),200)
#         else:
#             return make_response(jsonify({"error":"Folder not found"}))
    
#     def patch(self, id):
#         data = request.get_json()[0]
#         folder = Folder.query.filter(Folder.id == id).first()

#         if folder:
#             # Update folder attributes
#             for attr in data:
#                 setattr(folder, attr, data.get(attr))
            
#             # If 'path' is being updated, ensure it's a Cloudinary URL
#             if 'path' in data:
#                 # Validate that the URL is a Cloudinary URL
#                 if not data['path'].startswith('https://res.cloudinary.com'):
#                     return make_response(jsonify({"error": "Invalid Cloudinary URL"}), 400)

#             db.session.commit()
#             return make_response(folder.to_dict(only=("id", "folder_name", "user_id", "user.username")), 200)
#         else:
#             return make_response(jsonify({"error": "Folder not found"}), 404)
    
#     def delete(self, id):
#         folder = Folder.query.filter(Folder.id == id).first()

#         if folder:
#             # If 'path' represents a Cloudinary URL, additional handling may be needed
#             if folder.path.startswith('https://res.cloudinary.com'):
#                 # Extract public ID from Cloudinary URL
#                 public_id = cloudinary_url(folder.path)[0]
#                 # Additional handling for Cloudinary URL deletion
#                 # (e.g., removing associated files from Cloudinary)
#                 # cloudinary.uploader.destroy(public_id)
            
#             db.session.delete(folder)
#             db.session.commit()
#             return make_response("", 204)
#         else:
#             return make_response(jsonify({"error": "Folder not found"}), 404)
# api.add_resource(FolderByID,"/folders/<int:id>")

class Files(Resource):
    
    
    def post(self):
        data = request.get_json()
        
        # Handle file upload to Cloudin  # Assuming the file is in the 'file' field of the JSON payload
        
        try:
            new_file = File(
                filename=data.get('filename'),
                file_type=data.get("file_type"),
                size=data.get("size"),
                path=data.get('path'),  # Use the Cloudinary URL of the uploaded file
                folder_id=data.get("folder_id"),
                user_id=data.get('user_id')
            )  
            db.session.add(new_file)
            db.session.commit() 
            
        except ValueError:
            return make_response(jsonify({"error": ["validation errors"]}))    
        
        return make_response(new_file.to_dict(only=("filename", "file_type", "user.username", "folder_id", "path", "size", "user_id", "created_at")), 201)

    
    
    
api.add_resource(Files,"/files")  

class FileByFolder(Resource):
    def get(self,id):
        files = [files.to_dict(only=("id","filename","file_type","size","path","user.username", "is_delete", "created_at")) for files in File.query.filter(File.folder_id==id)]
               
        
        return make_response(files,200)
    
api.add_resource(FileByFolder,"/filefolder/<int:id>")    

class FileByUser(Resource):
    def get(self, id):
        files = [file.to_dict(only=("id", "filename", "file_type", "size", "path", "user.username", "is_delete", "created_at")) for file in File.query.filter(File.user_id == id,File.is_delete==0)]

        return make_response(files, 200)

api.add_resource(FileByUser, "/fileuser/<int:id>")

class TrashFiles(Resource):
    def get(self, id):
        files = [file.to_dict(only=("id", "filename", "file_type", "size", "path", "user.username")) for file in File.query.filter(File.user_id == id,File.is_delete==1)]

        return make_response(files, 200)

api.add_resource(TrashFiles, "/trashfiles/<int:id>")   
    
 
class FileByID(Resource):
    
    def get(self,id):
        file = File.query.filter(File.id==id).first()

        if file:
            return make_response(jsonify(file.to_dict(only=("id","filename","file_type","size","path","user.username"))),200)
        else:
            return make_response(jsonify({"error":"Folder not found"}))
        

        
    
    # def delete(self,id):
    #     file = File.query.filter(File.id==id).first()

    #     if file:
    #         # Delete file from Cloudinary if 'path' represents a Cloudinary URL
    #         if file.path.startswith('https://res.cloudinary.com'):
    #             # Extract public ID from Cloudinary URL
    #             public_id = cloudinary_url(file.path)[0]
    #             # Delete file from Cloudinary
    #             cloudinary.uploader.destroy(public_id)
            
    #         db.session.delete(file)
    #         db.session.commit()
    #         return make_response("", 204)
    #     else:
    #         return make_response(jsonify({"error": "File not found"}), 404)
        
        
api.add_resource(FileByID,"/files/<int:id>") 

class FileByFilename(Resource):
    
    def get(self, filename):
        
        file = File.query.filter(File.filename.ilike(f'%{filename}%')).first()

        if file:
            return make_response(jsonify(file.to_dict(only=("id", "filename", "file_type", "size", "path", "user.username"))), 200)
        else:
            return make_response(jsonify({"error": "File not found"}), 404)
        
api.add_resource(FileByFilename, '/filebyfilename/<string:filename>')

class MoveToTrash(Resource):
    def put(self, id):
        file = File.query.get(id)
        if not file:
            return {"error": "File not found"}, 404

        file.is_delete = True

        try:
            db.session.commit()
            return {"message": "File moved to trash successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

api.add_resource(MoveToTrash, '/move-to-trash/<int:id>')

class DeleteFile(Resource):
    def delete(self, id):
        file = File.query.get(id)
        if not file:
            return {"error": "File not found"}, 404

        db.session.delete(file)
        db.session.commit()
        return {"message": "File deleted successfully"}, 200

api.add_resource(DeleteFile, '/deletefiles/<int:id>')

        
class Shares(Resource):
    def get(self, shared_with_user_email):
        shares = [
            {
                'file_id': share.file_id,
                'share_type': share.share_type,
                'shared_with_user_email': share.shared_with_user_email,
                'user_id': share.user_id,
                'user': {
                    'email': share.user.email,
                    'username': share.user.username
                },
                'file': {
                    'size': share.file.size,
                    'path': share.file.path,
                    'filename': share.file.filename
                }
            }
            for share in Share.query.filter(Share.shared_with_user_email==shared_with_user_email).all()
        ]
        return make_response(jsonify(shares), 200)

api.add_resource(Shares, "/shares/<string:shared_with_user_email>")

class SharesPost(Resource):
        def post(self):
            data =  request.get_json()

            try:
                new_share = Share(
                    share_type= data.get('share_type'),
                    user_id = data.get('user_id'),
                    shared_with_user_email = data.get("shared_with_user_email"),
                    file_id = data.get("file_id")

                )
                db.session.add(new_share)
                db.session.commit() 

            except ValueError:
                return make_response(jsonify({"error":["validation errors"]}))

            return make_response(new_share.to_dict(only=("file.size","file.path","file_id","share_type","user_id","shared_with_user_email","user.username")),201)

api.add_resource(SharesPost, "/shares")     


class StarredItems(Resource):
    def get(self):
        starred_items= [starred.to_dict() for starred in StarredItem.query.all()]
        return make_response(starred_items,200)
    

    
api.add_resource(StarredItems,"/starreditems/<int:user_id>")   

class StarredItemsPost(Resource):
      def post(self):
        data =  request.get_json()

        try:
            starred_item = StarredItem(
                file_id = data.get("file_id"),
                user_id = data.get("user_id"),
                item_type = data.get("item_type"),
            )
            db.session.add(starred_item)
            db.session.commit() 

        except ValueError:
            return make_response(jsonify({"error" :["validation errors"]}))

        return make_response(starred_item.to_dict(only=("id","file_id","item_type","user_id")),201)
api.add_resource(StarredItemsPost,"/starreditems")   
      

class StarredItemByFileID(Resource):
   def delete(self, file_id):
        starred_item = StarredItem.query.filter(StarredItem.file_id == file_id).first()

        if starred_item:
            db.session.delete(starred_item)
            db.session.commit()
            return make_response("", 204)
        else:
            return make_response(jsonify({"error": "Item not found"}), 404)
    
api.add_resource(StarredItemByFileID, "/starreditem/<int:file_id>")
class TrashItems(Resource):
    def get(self):
        trash_item = [trash.to_dict() for trash in TrashItem.query.all()]
        return make_response(trash_item,200)   
    
    def post(self):
        data =  request.get_json()
        
       
        
        try:
            trash_item = TrashItem(
                file_id = data.get("file_id"),
                folder_id = data.get("folder_id"),
                item_type = data.get("item_type"),
                user_id = data.get("user_id")
                
            )  
            db.session.add(trash_item)
            db.session.commit() 
            
        except ValueError:
            return make_response(jsonify({"error":["validation errors"]}))    
        
        return make_response(trash_item.to_dict(only=("id","file_id","item_type","user_id")),201)

api.add_resource(TrashItems,"/trashitems")               
        
        
class TrashItemByID(Resource):
    def delete(self,id):
        trash_item = TrashItem.query.filter(TrashItem.id==id).first()

        if trash_item:
            db.session.delete(trash_item)
            db.session.commit()
            return make_response("",204)
        else:
            return make_response(jsonify({"error":"Item not found"}),404)
        
api.add_resource(TrashItemByID,"/trashitem/<int:id>")
            
        
        
                
        
        

if __name__ == "__main__":
    app.run(port=5555,debug=True) 