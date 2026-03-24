from fastapi import APIRouter

router = APIRouter()


@router.get("/business-types")
async def list_business_types() -> list[dict[str, str]]:
    return [
        {"value": "virtual-store", "label": "Sucursales"},
        {"value": "nearby-event", "label": "Eventos"},
        {"value": "recycling-point", "label": "Puntos de reciclaje"},
        {"value": "academy", "label": "Academias"},
        {"value": "technical-service", "label": "Servicios técnicos"},
    ]

