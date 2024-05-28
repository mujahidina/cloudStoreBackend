from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin 
from flask_migrate import Migrate
from sqlalchemy import MetaData
from datetime import datetime

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(100))

    @validates('password')
    def validate_password(self, key, password):
        if len(password) < 8:
            raise ValueError('Password must be more than 8 characters.')
        return password
    
    @validates('email')
    def validate_email(self, key, email):
        if not email.endswith("@gmail.com"):
            raise ValueError("Email is not valid. It should end with @gmail.com")
        return email

class Folder(db.Model, SerializerMixin):
    __tablename__ = 'folders'
    id = db.Column(db.Integer, primary_key=True)
    folder_name = db.Column(db.String(100), nullable=False)
    parent_folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_delete = db.Column(db.Boolean,default = False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('folders', lazy=True))
    files = db.relationship('File', backref='folder', lazy=True, cascade="all, delete-orphan")
    subfolders = db.relationship('Folder', backref=db.backref('parent_folder', remote_side=[id]), cascade="all, delete-orphan")

class File(db.Model, SerializerMixin):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String(255), nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_delete = db.Column(db.Boolean,default = False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('files', lazy=True))

    user = db.relationship('User', foreign_keys=[user_id])


class Share(db.Model, SerializerMixin):
    __tablename__ = 'shares'
    id = db.Column(db.Integer, primary_key=True)
    share_type = db.Column(db.String(50), nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    shared_with_user_email = db.Column(db.String, db.ForeignKey('users.email'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id])
    shared_with_user = db.relationship('User', foreign_keys=[shared_with_user_email])
    file = db.relationship('File', foreign_keys=[file_id])


# class StarredItem(db.Model,SerializerMixin):
#     __tablename__ = 'starred_items'

#     id = db.Column(db.Integer, primary_key=True)
#     file_id = db.Column(db.Integer, db.ForeignKey('files.id'))
#     folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'))
#     item_type = db.Column(db.String(50), nullable=False) 
#     user_id = db.Column(db.Integer, nullable=False)   

class StarredItem(db.Model, SerializerMixin):
    __tablename__ = 'starred_items'

    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    item_type = db.Column(db.String(50), nullable=False) 
    file = db.relationship('File', foreign_keys=[file_id])
    user = db.relationship('User', foreign_keys=[user_id])  

class TrashItem(db.Model,SerializerMixin):
    __tablename__ = 'trash_items'
    
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'))
    folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'))
    item_type = db.Column(db.String(50), nullable=False)  
    user_id = db.Column(db.Integer, nullable=False)  

