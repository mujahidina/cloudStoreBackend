from models import User, Folder, File
from app import app, db

def seed_data():
   with app.app_context():

    print('deleting existing data...')
    db.session.query(File).delete()
    db.session.query(Folder).delete()
    db.session.query(User).delete()
    db.session.commit() 

    print('creating users....')
    user1 = User(username='user1', email='user1@gmail.com', password='password1', image_url="https://i.scdn.co/image/ab6761610000e5ebebfd16a3bca87c31c1e20576")
    user2 = User(username='user2', email='user2@gmail.com', password='password2', image_url = "https://www.essence.com/wp-content/uploads/2022/12/GettyImages-1428769836-scaled.jpg")
#     db.session.add(user1)
#     db.session.add(user2)
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    print('creating folders....')
    folder1 = Folder(folder_name='Folder 1', user_id=user1.id)
    folder2 = Folder(folder_name='Folder 2', user_id=user1.id)
    folder3 = Folder(folder_name='Folder 3', user_id=user2.id)
    db.session.add(folder1)
    db.session.add(folder2)
    db.session.add(folder3)
    db.session.commit()

    print('creating files....')
    file1 = File(filename='file1.txt', file_type='text', size=1024, path='/path/to/file1.txt', folder_id=folder1.id, user_id=user1.id)
    file2 = File(filename='file2.txt', file_type='text', size=2048, path='/path/to/file2.txt', folder_id=folder2.id, user_id=user1.id)
    file3 = File(filename='file3.txt', file_type='text', size=4096, path='/path/to/file3.txt', folder_id=folder3.id, user_id=user2.id)
    db.session.add(file1)
    db.session.add(file2)
    db.session.add(file3)
    db.session.commit()
       

if __name__ == '__main__':
    seed_data()



# from models import  User, Folder, File
# from app import app, db

# def seed_data():
#    with app.app_context():
    
#      # Delete existing data
#     print('deleting existing data...')
#     db.session.query(File).delete()
#     db.session.query(Folder).delete()
#     db.session.query(User).delete()
#     db.session.commit() 
         
#     print('creating users....')
#     user1 = User(username='user1', email='user1@gmail.com', password='password1',image_url="https://i.scdn.co/image/ab6761610000e5ebebfd16a3bca87c31c1e20576")
#     user2 = User(username='moringa', email='user2@gmail.com', password='password2',image_url = "https://www.essence.com/wp-content/uploads/2022/12/GettyImages-1428769836-scaled.jpg")
#     db.session.add(user1)
#     db.session.add(user2)
#     db.session.commit()
#     with app.app_context():
#         # Delete existing data
#         print('deleting existing data...')
#         db.session.query(File).delete()
#         db.session.query(Folder).delete()
#         db.session.query(User).delete()
#         db.session.commit()

#         # Create new data
#         print('creating users...')
#         user1 = User(username='user1', email='user1@gmail.com', password='password1')
#         user2 = User(username='user2', email='user2@gmail.com', password='password2')
#         db.session.add(user1)
#         db.session.add(user2)
#         db.session.commit()

#         print('creating folders...')
#         folder1 = Folder(folder_name='Folder 1', user_id=user1.id)
#         folder2 = Folder(folder_name='Folder 2', user_id=user1.id)
#         folder3 = Folder(folder_name='Folder 3', user_id=user2.id)
#         db.session.add(folder1)
#         db.session.add(folder2)
#         db.session.add(folder3)
#         db.session.commit()

#         print('creating files...')
#         file1 = File(filename='file1.txt', file_type='text', size=1024, path='/path/to/file1.txt', folder_id=folder1.id, user_id=user1.id)
#         file2 = File(filename='file2.txt', file_type='text', size=2048, path='/path/to/file2.txt', folder_id=folder2.id, user_id=user1.id)
#         file3 = File(filename='file3.txt', file_type='text', size=4096, path='/path/to/file3.txt', folder_id=folder3.id, user_id=user2.id)
#         db.session.add(file1)
#         db.session.add(file2)
#         db.session.add(file3)
#         db.session.commit()

# if __name__ == '__main__':
#     seed_data()


