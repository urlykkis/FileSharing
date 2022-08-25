from .me import router
from .files import router

from .auth import router
from .update_file_status import router

from .register import router
from .upload_file import router

from .delete_file import router

__all__ = ['router']
