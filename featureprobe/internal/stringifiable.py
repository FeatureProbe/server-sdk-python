def stringifiable(cls):
    """Experimental, unusable yet"""

    def __str__(self):
        attrs = sorted(filter(lambda attr: not callable(attr[1]),
                              self.__dict__.items()))

        return '%s(%s)' % (
            cls.__name__,
            ', '.join(
                '%s=\'%s\'' % item
                if isinstance(item[1], (str, bytes))
                else '%s=%s' % item
                for item in attrs
            )
        )

    cls.__str__ = __str__
    return cls
