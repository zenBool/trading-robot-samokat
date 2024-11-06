from pydantic import BaseModel, ConfigDict


class UserCreateSchema(BaseModel):
    username: str
    foo: int
    bar: int


class UserResponseSchema(UserCreateSchema):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: int
