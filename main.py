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
@app.middleware("http")
async def process_time(request: Request, call_next):
    # 1. So'rov keldi — vaqtni boshlaymiz
    start = time.time()

    # 2. So'rovni endpoint ga yuboramiz
    response = await call_next(request)

    # 3. Javob qaytdi — vaqtni hisoblaymiz
    duration = time.time() - start
    response.headers["X-Process-Time"] = str(duration)

    # 4. Javobni klientga qaytaramiz
    return response


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = datetime.now()
    logger.info(f"→ {request.method} {request.url.path} | IP: {request.client.host}")
    response = await call_next(request)
    duration = (datetime.now() - start).total_seconds()
    logger.info(f"← {response.status_code} | {duration:.3f}s")
    if duration > 1:
        logger.warning(f"Slow request: {request.method} {request.url.path} took {duration:.3f}s")
    return response
@app.get("/")
def read_root():
 
    return {"message": "API is running"}
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


request_log = defaultdict(list)
