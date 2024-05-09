from models import File,Share,User,Folder,SerializerMixin

class TestModels:
    def test_superclasses(self):
        '''inherits from db.Model and SerializerMixin'''
        
        assert isinstance(File(), SerializerMixin)
        assert isinstance(Share(), SerializerMixin)
        assert isinstance(User(), SerializerMixin)
        assert isinstance(Folder(), SerializerMixin)
            
    def test_table_name_presence(self):
        # Test if each class has a table name defined
        assert hasattr(User, '__tablename__') and User.__tablename__
        assert hasattr(Folder, '__tablename__') and Folder.__tablename__
        assert hasattr(File, '__tablename__') and File.__tablename__
        assert hasattr(Share, '__tablename__') and Share.__tablename__
