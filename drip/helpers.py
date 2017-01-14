def chunks(lst, n):
    """
    Yields successive n-sized chunks from list
    Args:
        lst: Python List
        n (int): Size of chunks

    Returns:
        Yields successive n-sized chunks
    """
    for i in xrange(0, len(lst), n):
        yield lst[i:i + n]


def partition(lst, n):
    return list(chunks(lst, n))
