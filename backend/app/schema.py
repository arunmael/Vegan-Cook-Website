from pydantic import BaseModel, ConfigDict, Field



class UserBase(BaseModel):
    """Daten, die für einen Benutzer erwartet werden."""

    user_name: str = Field(min_length=1, max_length=255)
    user_email: str = Field(min_length=1, max_length=255)


class UserMailCheck(BaseModel):
    """Daten, die für die E-Mail eines Benutzers erwartet werden."""

    user_email: str = Field(min_length=1, max_length=255)

class UserNameCheck(BaseModel):
    """Daten, die für den Benutzernamen eines Benutzers erwartet werden."""

    user_name: str = Field(min_length=1, max_length=255)


class UserCreate(UserBase):
    """Daten, die beim Erstellen eines Benutzers erwartet werden."""

    user_password: str = Field(min_length=8, max_length=255)


class UserResponse(UserBase):
    """Daten, die FastAPI für einen Benutzer zurückgibt."""

    user_id: int

    model_config = ConfigDict(from_attributes=True)


class UserLoginEmail(BaseModel):
    """Daten, die für die Anmeldung eines Benutzers per E-Mail erwartet werden."""

    user_email: str = Field(min_length=1, max_length=255)
    user_password: str = Field(min_length=8, max_length=255)


class UserLoginName(BaseModel):
    """Daten, die für die Anmeldung eines Benutzers per Benutzername erwartet werden."""

    user_name: str = Field(min_length=1, max_length=255)
    user_password: str = Field(min_length=8, max_length=255)


class Login(BaseModel):
    """Daten, die für den Login eines Benutzers erwartet werden."""
    identifier: str = Field(min_length=1, max_length=255)
    user_password: str = Field(min_length=8, max_length=255)



class IngredientCreate(BaseModel):
    """Daten, die beim Erstellen einer Zutat erwartet werden."""

    ing_name: str = Field(min_length=1, max_length=255)


class IngredientResponse(BaseModel):
    """Daten, die FastAPI für eine Zutat zurückgibt."""

    ingredient_id: int
    ing_name: str

    model_config = ConfigDict(from_attributes=True)
