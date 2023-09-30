import uuid

def to_string(obj):
    def __str__(self):
        attributes = ', '.join(f"{key}={value}" for key, value in vars(self).items())
        return f"{self.__class__.__name__}({attributes})"
    obj.__str__ = __str__
    return obj

def generate_id(prefix = ""):
    id = uuid.uuid4()
    return f'{"" if prefix == "" else (prefix + "-")}{id}'
