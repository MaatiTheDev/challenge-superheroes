import ipdb
from models import Hero, Power, HeroPower
from app import app

if __name__ == '__main__':
    with app.app_context():
        ipdb.set_trace()