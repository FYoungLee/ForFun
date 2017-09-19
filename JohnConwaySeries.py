def jc_series(howmany):
    if not isinstance(howmany, int):
        raise Exception('An integer required! ')
    result = '1'
    ret = [result, ]
    for n in range(howmany):
        strn = '{}'.format(result)
        result = ''
        counter = 1
        number = None
        for each in strn:
            if not number:
                number = each
                continue
            if number == each:
                counter += 1
            else:
                result = '{}{}{}'.format(result, counter, number)
                number = each
                counter = 1
        result = '{}{}{}'.format(result, counter, number)
        ret.append(result)
    return ret

if __name__ == '__main__':
    hm = input('Input the size of John Conway Series that you want >> ')
    for each in jc_series(int(hm)):
        print(each)
