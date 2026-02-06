from pydantic import BaseModel


class CategoryCreate(BaseModel):
    """
    Data required to create a new category.
    """
    name: str
    essential: bool = False  # Indicates whether the category is essential (default: False)


class CategoryResponse(BaseModel):
    """
    Data returned by the API when retrieving a category.
    """
    id: int
    name: str
    essential: bool

    class Config:
        orm_mode = True  # Allows returning ORM objects directly
