from fastapi import FastAPI
from Routes.consulta_kauil import router as fire_router
from fastapi.middleware.cors import CORSMiddleware
from cfn import CONFIG_APP



app = FastAPI(**CONFIG_APP)



app.add_middleware(
    CORSMiddleware,
    allow_origins = "*",
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.include_router(router=fire_router)