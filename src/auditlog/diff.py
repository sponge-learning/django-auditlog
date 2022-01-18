from django.db.models import Model


def to_unicode(value):
    if isinstance(value, str):
        value = value.decode('utf-8')
    return unicode(value)

def model_instance_diff(old, new):
    """
    Calculate the differences between two model instances. One of the instances may be None (i.e., a newly
    created model or deleted model). This will cause all fields with a value to have changed (from None).
    """
    if not(old is None or isinstance(old, Model)):
        raise TypeError('The supplied old instance is not a valid model instance.')
    if not(new is None or isinstance(new, Model)):
        raise TypeError('The supplied new instance is not a valid model instance.')

    diff = {}

    if old is not None and new is not None:
        fields = set(old._meta.fields + new._meta.fields)
    elif old is not None:
        fields = set(old._meta.fields)
    elif new is not None:
        fields = set(new._meta.fields)
    else:
        fields = set()

    for field in fields:
        old_value = to_unicode(getattr(old, field.name, None))
        new_value = to_unicode(getattr(new, field.name, None))

        if old_value != new_value:
            diff[field.name] = (old_value, new_value)

    if len(diff) == 0:
        diff = None

    return diff
