def header(*allowType):
    def decorator(func):
        def wrapper(*args, **kw):
            for allow in allowType:
                if allow == 'Headers':
                    args[0].set_header("Access-Control-Allow-Headers", "*")
                elif allow == 'Methods':
                    args[0].set_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
                elif allow == 'Origin':
                    args[0].set_header("Access-Control-Allow-Origin", "*")
            return func(*args, **kw)
        return wrapper
    return decorator