from pydantic import BaseModel

from ..constants import MAX_METRO_DISTANT


class McDonaldsBaseModelMetro(BaseModel):
    name: str = ""
    dist: int = MAX_METRO_DISTANT


class McDonaldsBaseModelFeatures(BaseModel):
    name: str = ""


class McDonaldsBaseModelRestaurant(BaseModel):
    name: str = ""
    address: str = ""
    phone: str = ""
    features: list[McDonaldsBaseModelFeatures] = []


class McDonaldsBaseModel(BaseModel):
    metro: list[McDonaldsBaseModelMetro] = []
    restaurant: McDonaldsBaseModelRestaurant = {}
    message: str = ""
