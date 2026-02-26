from fastapi import FastAPI, Request, status
import time
from fastapi.responses import JSONResponse
from endpoint.user import user_router
from endpoint.post import post_router
from core.db import get_db, create_tables
from core.models import Users, Post, Comment  # Import models to register them
from datetime import datetime
import logging
from collections import defaultdict
app = FastAPI(title="Project1 API")

# Create tables on startup
create_tables()

app.include_router(user_router)
app.include_router(post_router)



# @app.middleware("http")
# async def blacklist(resquest: Request, call_next):
#     response = await call_next(resquest)
#     IP_BLACKLIST = ['127.0.0.1:8010']
#     host = resquest.headers['host']
    
#     if host in IP_BLACKLIST:
#         logger.warning("xatolik")
#         return JSONResponse(
#             content= "TOOO many request",
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )
#         response.headers["TIME"] = str("erfhubv")
#         return response



