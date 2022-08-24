from .register import router
from .auth import router
from .upload_file import router
from .me import router
from .files import router
from .delete_file import router
from .update_file_status import router

__all__ = ['router']
