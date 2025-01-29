import json
from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from Schemas.fire_consult import FireData
from fastapi.encoders import jsonable_encoder
from Models import get_data as gd

router = APIRouter()
tag = "Fire"


@router.post(
    path="/predict_new_fire",
    summary="Consulta de modelo Kauil para el reconocimiento de riesgo de un incendio",
    tags=[tag],
)
async def factura(request: FireData = Body(...)):
    test_data = gd.prepare_test_data(
        longitude=request.longitude,
        latitude=request.latitude,
        fire_date=request.fire_start_date
    )
    prediction = gd.predict_risk(test_data)
    return JSONResponse(content=jsonable_encoder(prediction), status_code=status.HTTP_200_OK)
