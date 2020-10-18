def diff(base: list, removed: list) -> list: 
    result = list(base).copy()
    for value in removed:
        try:
            result.remove(value)
        except ValueError:
            # do nothing
            continue
    
    return result
