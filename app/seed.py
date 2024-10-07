from app import create_app, db
from app.models import Hero, Power

app = create_app()

with app.app_context():
    db.create_all()

    hero1 = Hero(name="Kamala Khan", super_name="Ms. Marvel")
    hero2 = Hero(name="Doreen Green", super_name="Squirrel Girl")

    power1 = Power(
        name="super strength", description="gives the wielder super-human strengths"
    )
    power2 = Power(
        name="flight",
        description="gives the wielder the ability to fly through the skies at supersonic speed",
    )

    db.session.add_all([hero1, hero2, power1, power2])
    db.session.commit()
