from fastapi import Depends

from .loader import router
from utils.schemas.users import User
from utils.dependencies import JWTBearer
from data.responses import Response, ResponseSchemas


@router.get("/me", name='Информация о пользователе',
            status_code=200,
            response_description="Возвращает информацию о пользователе",
            response_model=ResponseSchemas.UserInfo)
async def me_handler(user: User = Depends(JWTBearer())) -> ResponseSchemas.UserInfo:
    return Response.user_info({
        "uid": user.uid,
        "username": user.username,
        "email": user.email,
        "reg_date": user.reg_date,
        "status": user.status,
        "recent_entries": user.recent_entries,
        "total_files": user.total_files
    })
