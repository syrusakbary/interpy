try:
    import six
except ImportError:
    from interpy import six

StringIO = six.StringIO
next = six.next
