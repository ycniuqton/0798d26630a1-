from config import APPConfig
from home.models import SystemCounter
from services.discount import DiscountRepository


class PurchaseEstimator:
    def __init__(self, user, rules=[]):
        self.rules = rules
        self.system_counter = SystemCounter
        self.discount_repo = None
        self.user = user

    def estimate(self, plan, os, duration=1):
        if not plan or not os:
            return 0

        total_fee = plan['price'] * duration
        self.discount_repo = DiscountRepository.get(duration=duration)
        discounted_fee, discount_amount = self.discount_repo.apply(total_fee)
        counter = self.system_counter.get_vps_counter(self.user, plan['id'])

        is_valid = True
        message = ''

        if self.user.balance.amount < discounted_fee and not self.user.is_staff:
            is_valid = False
            message = 'Insufficient balance'

        if (plan['limit_per_user'] and counter >= plan['limit_per_user'] and
              not self.user.is_staff and APPConfig.APP_ROLE != 'admin'):
            is_valid = False
            message = 'Exceeded limit'

        if os.get('distro') == 'windows' and os.get('name', '').find('-2022') > -1 and plan['ram_display'] < 2:
            is_valid = False
            message = 'Requires minimum 2 GB of RAM'

        return is_valid, message, discounted_fee, discount_amount, total_fee
