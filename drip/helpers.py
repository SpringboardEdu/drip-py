def chunks(lst, n):
    '''yield successive n-sized chunks from lst.'''
    for i in xrange(0, len(lst), n):
        yield lst[i:i + n]


def partition(lst, n):
    return list(chunks(lst, n))
