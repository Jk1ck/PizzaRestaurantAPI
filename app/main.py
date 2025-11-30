from fastapi import FastAPI
from sqlmodel import Session, select, SQLModel
from app.database import engine
from app.models import Restaurant, Chef, Pizza, Ingredient, Review, PizzaIngredientLink

app = FastAPI(title="Pizza API")


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def seed_data():
    with Session(engine) as session:
        if not session.exec(select(Restaurant)).first():
            r1 = Restaurant(name="LoLoPizza", address="Байтурсынова 80")
            r2 = Restaurant(name="PizzaHubovich", address="Сейфуллина 500")
            session.add_all([r1, r2])
            session.commit()

            c1 = Chef(name="Марио Братишкин", restaurant_id=r1.id)
            c2 = Chef(name="Гордон Рамзаев", restaurant_id=r2.id)
            session.add_all([c1, c2])
            session.commit()


@app.post("/restaurants/", response_model=Restaurant)
def create_restaurant(restaurant: Restaurant):
    with Session(engine) as session:
        session.add(restaurant)
        session.commit()
        session.refresh(restaurant)
        return restaurant


@app.get("/restaurants/", response_model=list[Restaurant])
def get_restaurants():
    with Session(engine) as session:
        restaurants = session.exec(select(Restaurant)).all()
        return restaurants


@app.get("/pizzas/", response_model=list[Pizza])
def get_pizzas():
    with Session(engine) as session:
        return session.exec(select(Pizza)).all()

@app.post("/pizzas/", response_model=Pizza)
def create_pizza(pizza: Pizza):
    with Session(engine) as session:
        session.add(pizza)
        session.commit()
        session.refresh(pizza)
        return pizza

@app.put("/pizzas/{pizza_id}", response_model=Pizza)
def update_pizza(pizza_id: int, pizza_data: Pizza):
    with Session(engine) as session:
        pizza = session.get(Pizza, pizza_id)
        if not pizza:
            return {"error": "Pizza not found"}
        pizza.name = pizza_data.name
        pizza.cheese = pizza_data.cheese
        pizza.dough = pizza_data.dough
        pizza.secret = pizza_data.secret
        pizza.restaurant_id = pizza_data.restaurant_id
        session.add(pizza)
        session.commit()
        session.refresh(pizza)
        return pizza

@app.delete("/pizzas/{pizza_id}")
def delete_pizza(pizza_id: int):
    with Session(engine) as session:
        pizza = session.get(Pizza, pizza_id)
        if not pizza:
            return {"error": "Pizza not found"}
        session.delete(pizza)
        session.commit()
        return {"ok": True}

@app.get("/chefs/", response_model=list[Chef])
def get_chefs():
    with Session(engine) as session:
        return session.exec(select(Chef)).all()

@app.post("/chefs/", response_model=Chef)
def create_chef(chef: Chef):
    with Session(engine) as session:
        session.add(chef)
        session.commit()
        session.refresh(chef)
        return chef

@app.get("/ingredients/", response_model=list[Ingredient])
def get_ingredients():
    with Session(engine) as session:
        return session.exec(select(Ingredient)).all()

@app.post("/ingredients/", response_model=Ingredient)
def create_ingredient(ingredient: Ingredient):
    with Session(engine) as session:
        session.add(ingredient)
        session.commit()
        session.refresh(ingredient)
        return ingredient
    
@app.get("/reviews/", response_model=list[Review])
def get_reviews():
    with Session(engine) as session:
        return session.exec(select(Review)).all()

@app.post("/reviews/", response_model=Review)
def create_review(review: Review):
    with Session(engine) as session:
        session.add(review)
        session.commit()
        session.refresh(review)
        return review

@app.get("/restaurants/{restaurant_id}/menu/", response_model=list[Pizza])
def get_menu(restaurant_id: int):
    with Session(engine) as session:
        pizzas = session.exec(select(Pizza).where(Pizza.restaurant_id == restaurant_id)).all()
        return pizzas

@app.get("/reviews-with-restaurants/")
def reviews_with_restaurants():
    with Session(engine) as session:
        reviews = session.exec(select(Review)).all()
        result = []
        for review in reviews:
            restaurant = session.get(Restaurant, review.restaurant_id)
            result.append({
                "review_id": review.id,
                "rating": review.rating,
                "text": review.text,
                "restaurant_name": restaurant.name if restaurant else None
            })
        return result
