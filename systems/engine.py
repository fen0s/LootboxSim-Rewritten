class Engine():
    def __init__(self, balance=100, price=10):
        self.balance = balance
        self.price = price
        self.spent, self.earned, self.opened,  = 0, 0, 0
    
    @property
    def statistics(self):
        return f"Lootboxes opened: {self.opened}\n Money spent: ${self.spent}\nMoney earned: ${self.earned}"
    
    @property
    def balancestr(self):
        return f'Balance: ${self.balance}'