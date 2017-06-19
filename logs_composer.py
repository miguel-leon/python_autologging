import inspect


def for_callable(target, args, keywords):
    spec_args, spec_varargs, spec_keywords, spec_defaults = inspect.getargspec(target)

    owner = None
    try:
        owner = str(target.im_class)
    except AttributeError:
        try:
            if spec_args[0] == 'self':
                owner = target.__module__ + "." + args[0].__class__.__name__
        except IndexError:
            pass

    if owner:
        args = args[1:]
        spec_args = spec_args[1:]
    else:
        owner = target.__module__

    dargs = dict(zip(spec_args[-len(spec_defaults):], list(spec_defaults))) if spec_defaults else {}
    dargs.update(dict(zip(spec_args, list(args))))
    dargs.update(keywords)
    largs = [(k, repr(dargs.pop(k))) for k in spec_args]

    if spec_varargs:
        largs += [(spec_varargs, args[len(spec_args):])]

    if spec_keywords:
        largs += [(spec_keywords, {k: v for k, v in keywords.items() if k not in spec_args})]

    fargs = ", ".join(map("{0}={1}".format, *zip(*largs))) if largs else ""
    fargs = "(" + fargs + ")"

    return owner + ":" + target.__name__ + fargs
