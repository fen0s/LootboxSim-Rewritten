from systems.application import Application
from systems.engine import Engine
from systems.inventory import Inventory

if __name__ == '__main__':
    engine = Engine()
    inventory = Inventory(engine)
    main_application = Application(engine, inventory)
