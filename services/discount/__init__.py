class DiscountRepository:
    def __init__(self, discount_percent=0):
        self.discount_percent = discount_percent

    @staticmethod
    def get(duration=1, code=None):
        discount_percent = 0
        if duration == 1:
            discount_percent += 0
        elif duration == 3:
            discount_percent += 5
        elif duration == 6:
            discount_percent += 10
        elif duration == 12:
            discount_percent += 15
        elif duration == 24:
            discount_percent += 20

        if discount_percent > 100:
            discount_percent = 100

        return DiscountRepository(discount_percent)

    def apply(self, price):
        discount_amount = price * (self.discount_percent / 100)
        discounted_price = price - discount_amount
        return discounted_price, discount_amount
