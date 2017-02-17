# -*- coding: utf-8 -*-
import re
import datetime
import yahoo_finance as yf

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[00m'
    BOLD = '\033[01m'
    UNDERLINE = '\033[04m'

def show_rt_quote(stock_id):

    sk = yf.Share(stock_id)
    #sk.refresh()
    name = re.sub('TWD10', '',sk.get_name().strip())
    price = sk.get_price()
    #convert raw number to comma separated string and cut the tailing 000
    volume = '{:,}'.format(int(sk.get_volume()[:-3]))
    change = sk.get_change()
    percentage = sk.get_percent_change()
    prev = sk.get_prev_close()

    print('{} {} {} {} {} {}'.format(
            name[:NAME_LEN-2] + '..',
            price.rjust(PRICE_LEN),
            volume.rjust(VOLUME_LEN),
            change.rjust(CHANGE_LEN),
            percentage.rjust(PERCENT_LEN),
            prev.rjust(PREV_LEN)
        )
    )

if __name__ == '__main__':

    NAME_LEN = 12
    PRICE_LEN = 8
    VOLUME_LEN = 10
    CHANGE_LEN = 8
    PERCENT_LEN = 8
    PREV_LEN = 8
    bar_len = NAME_LEN+PRICE_LEN+VOLUME_LEN+CHANGE_LEN+PERCENT_LEN+PREV_LEN+5
    #parse stock list
    stock_list = eval(open('rt.conf').read())
    #print titles
    print('{} {} {} {} {} {}'.format(
            'Name'.ljust(NAME_LEN),
            'Price'.rjust(PRICE_LEN),
            'Volume'.rjust(VOLUME_LEN),
            'Change'.rjust(CHANGE_LEN),
            '%'.rjust(PERCENT_LEN),
            'Prev'.rjust(PREV_LEN)
        )
    )
    print('-' * bar_len)
    for id in stock_list:
        show_rt_quote(str(id) + '.TW')
    print('-' * bar_len)
    print('current time: %s' % datetime.datetime.now())
    print('WARNING: information might not be update to date!')

