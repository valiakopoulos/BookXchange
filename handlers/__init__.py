from handlers.main_handler import MainHandler
from handlers.login_handler import LoginHandler
from handlers.logout_handler import LogoutHandler
from handlers.add_book_handler import AddBookHandler
from handlers.search_handler import SearchHandler
from handlers.static_handler import StaticFileHandler
from handlers.search_book_handler import SearchBookHandler
from handlers.user_handler import UserHandler
from handlers.deactivate_book_handler import DeactivateBookHandler
from handlers.change_admin_handler import ChangeAdminHandler
from handlers.ban_user_handler import BanUserHandler

import os
if 'BOOKXCHANGE_PROD' in os.environ:
    from handlers.auth_handler import AuthHandler
    from handlers.attrs_handler import AttrsHandler
    from handlers.metadata_handler import MetadataHandler