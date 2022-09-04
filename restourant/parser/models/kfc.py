from pydantic import BaseModel


class KFCBaseModelGeometry(BaseModel):
    coordinates: list[float, float] = [0.0, 0.0]


class KFCBaseModelEnRuStatement(BaseModel):
    en: str = ""
    ru: str = ""


class KFCBaseModelCoordinatesContacts(BaseModel):
    geometry: KFCBaseModelGeometry


class KFCBaseModelContacts(BaseModel):
    coordinates: KFCBaseModelCoordinatesContacts
    phoneNumber: str = ""
    streetAddress: KFCBaseModelEnRuStatement


class KFCBaseModelStore(BaseModel):
    contacts: KFCBaseModelContacts
    features: list[str] = []
    title: KFCBaseModelEnRuStatement


class KFCBaseModel(BaseModel):
    distanceMeters: int | None
    store: KFCBaseModelStore


class KFCBaseModelSearchResults(BaseModel):
    searchResults: list[KFCBaseModel]
