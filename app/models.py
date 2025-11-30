from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Restaurant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    address: str

    chef: Optional["Chef"] = Relationship(back_populates="restaurant")
    pizzas: List["Pizza"] = Relationship(back_populates="restaurant")
    reviews: List["Review"] = Relationship(back_populates="restaurant")


class Chef(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    restaurant_id: int = Field(foreign_key="restaurant.id")

    restaurant: Optional[Restaurant] = Relationship(back_populates="chef")


class PizzaIngredientLink(SQLModel, table=True):
    pizza_id: Optional[int] = Field(default=None, foreign_key="pizza.id", primary_key=True)
    ingredient_id: Optional[int] = Field(default=None, foreign_key="ingredient.id", primary_key=True)


class Pizza(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    cheese: str
    dough: str
    secret: str
    restaurant_id: int = Field(foreign_key="restaurant.id")

    restaurant: Optional[Restaurant] = Relationship(back_populates="pizzas")
    ingredients: List["Ingredient"] = Relationship(back_populates="pizzas", link_model=PizzaIngredientLink)


class Ingredient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    pizzas: List[Pizza] = Relationship(back_populates="ingredients", link_model=PizzaIngredientLink)


class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rating: int
    text: str
    restaurant_id: int = Field(foreign_key="restaurant.id")

    restaurant: Optional[Restaurant] = Relationship(back_populates="reviews")