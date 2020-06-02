from data.prefstuff import prices, prefdict, qualities, prefix_number
import random
from data.nouns import nouns

class Inventory():
    def __init__(self, engine):
        self.items = {}
        self.engine = engine
    
    @property
    def inventory_price(self):
        return sum([price for price in list(self.items.values())])
    
    def generate_loot(self):
        lootstr = ''
        tier = random.choice(qualities)
        
        for _ in range(prefix_number.get(tier)):
            prefix = random.choice(prefdict.get(tier))
            if prefix in lootstr:
                continue
            lootstr += prefix + ' '
        lootstr += random.choice(nouns).title()
        
        tier_maxprice = prices.get(tier)
        loot = [tier, tier.title() + ' ' + lootstr, random.randint(1, tier_maxprice)]
        
        return loot
    
    def add_to_inventory(self, loot, price):
        self.items.update({loot: price})
    
    def sell_inventory(self):
        self.engine.balance += self.inventory_price
        self.engine.earned += self.inventory_price
        self.items.clear()
    
    @property
    def all_items(self):
        item_list = ''
        for itemprice_pair in self.items.items():
            item_list += f'Item: {itemprice_pair[0]}, price: {itemprice_pair[1]}$\n'
        return item_list