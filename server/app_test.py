from app import UserRegister, UserLogin, Logout, Users, UserByID,Resource,Folders,FolderByID,Files,FileByID,Shares,ShareByID

class TestRoutesResources:
    
        
    def test_user_register_inheritance(self):
        # Test if UserRegister inherits from Resource '
        assert(isinstance(UserRegister(), Resource))
        # Perform additional checks as needed
        
    def test_user_login_inheritance(self):
        # Test if UserLogin inherits from Resource '
        assert(isinstance(UserLogin(), Resource))
        # Perform additional checks as needed
        
    def test_logout_inheritance(self):
        # Test if Logout inherits from Resource '
        assert(isinstance(Logout(), Resource))
        # Perform additional checks as needed
        
    def test_users_inheritance(self):
        # Test if Users inherits from Resource 
        assert(isinstance(Users(), Resource))
        # Perform additional checks as needed
        
    def test_user_by_id_inheritance(self):
        # Test if UserByID inherits from Resource 
        assert(isinstance(UserByID(), Resource))
        # Perform additional checks as needed
        
    def test_folders_inheritance(self):
        # Test if Folders inherits from Resource
        assert(isinstance(Folders(),Resource))
        
    def test_folder_by_id_inheritance(self):
        # Test if FolderByID inherits from Resource
        assert(isinstance(FolderByID(),Resource))
        
    def test_files_inheritance(self):
        # Test if Files inherits from resource
        assert(isinstance(Files(),Resource))
        
    def test_file_by_id_inheritance(self):
        # Test if FileByID iinherits from resource
        assert(isinstance(FileByID(),Resource))
        
    def test_shares_inheritance(self):
        # Test if File
        assert(isinstance(Shares(),Resource))
        
    def test_share_by_id_inheritance(self):
        assert(isinstance(ShareByID(),Resource))
        
                           

