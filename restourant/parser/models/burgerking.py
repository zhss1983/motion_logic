from pydantic import BaseModel


class BurgerKingBaseModel(BaseModel):
    address: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    phone: str = ""
    name: str = ""
    breakfast: bool = False
    children_party: bool = False
    metro: str | None = ""
    king_drive: bool = False
    parking_delivery: bool = False
    table_delivery: bool = False
    wifi: bool = False


class BurgerKingBaseModelSearchResults(BaseModel):
    items: list[BurgerKingBaseModel]
