from datetime import datetime


def get_date_serial():

    return datetime.now().strftime('%m%d%y%H%M%S')


def get_date_serial_reverse():

    h = 23 - int(datetime.now().strftime('%H'))
    m = 59 - int(datetime.now().strftime('%M'))
    s = 59 - int(datetime.now().strftime('%S'))

    return datetime.now().strftime('%m%d%y{0}{1}{2}'.format(h, m, s))