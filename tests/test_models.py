from app.models import Restaurant, Chef

def test_restaurant_model():
    r = Restaurant(name="Test Pizza", address="Test Street 123")
    assert r.name == "Test Pizza"
    assert r.address == "Test Street 123"

def test_chef_model():
    c = Chef(name="Test Chef", restaurant_id=1)
    assert c.name == "Test Chef"
    assert c.restaurant_id == 1
