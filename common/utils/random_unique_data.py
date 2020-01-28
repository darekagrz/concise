
import random
from utils.helpers import get_date_serial


class RandomUniqueData(object):
    def __init__(self, seed=''):
        self.unique_number = '{0}{1}'.format(get_date_serial(), seed)
        self.full_name = 'FN{0} LN{0}'.format(self.unique_number)
        self.first_name = self.full_name.split()[0]
        self.last_name = self.full_name.split()[1]
        self.email = '{0}@email.com'.format(self.unique_number)
        self.home_email = 'home{0}'.format(self.email)
        self.private_email = 'private{0}'.format(self.email)
        self.title = 'Title{0}'.format(self.unique_number)
        self.company_name = 'Company{0}'.format(self.unique_number)
        self.description = 'Description{0}'.format(self.unique_number)
        self.phone_number = '({0}{1}{2}) {3}{4}{5}-{6}{7}{8}{9}'.\
            format(*list(str(random.randrange(1000000000, 9999999999))))
        self.phone_number_digits = ''.join(num for num in self.phone_number if num.isdigit())
        self.mobile_number = '({0}{1}{2}) {3}{4}{5}-{6}{7}{8}{9}'.\
            format(*list(str(random.randrange(1000000000, 9999999999))))
        self.mobile_number_digits = ''.join(num for num in self.mobile_number if num.isdigit())
        self.home_number = '({0}{1}{2}) {3}{4}{5}-{6}{7}{8}{9}'.\
            format(*list(str(random.randrange(1000000000, 9999999999))))
        self.home_number_digits = ''.join(num for num in self.home_number if num.isdigit())
        self.address1 = 'Address1{0}'.format(self.unique_number)
        self.address2 = 'Address2{0}'.format(self.unique_number)
        self.city = 'City{0}'.format(self.unique_number)
        self.zip = '{0}'.format(str(self.unique_number)[:5])
