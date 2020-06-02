from systems.application import Application
from systems.engine import Engine
from systems.inventory import Inventory
engine = Engine()
inventory = Inventory(engine)
main_application = Application(engine, inventory)
