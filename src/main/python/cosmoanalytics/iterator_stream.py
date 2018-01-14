import logging

LOGGER = logging.getLogger()


class IteratorStream:
    """
    File-like iterating stream, inspired by:
    https://github.com/shazow/urllib3/blob/filepost-stream/urllib3/filepost.py#L23
    """
    def __init__(self, generator):
        self.generator = generator
        self.leftover = b''

    def read(self, size=-1):
        LOGGER.debug("start read({})".format(size))

        buffer = self.leftover
        buffer_size = len(self.leftover)

        try:
            while buffer_size < size or size == -1:
                chunk = self.generator.__next__()
                buffer += chunk
                buffer_size += len(chunk)
        except StopIteration:
            pass

        if buffer_size > size:
            self.leftover = buffer[size:]

        result = buffer[:size]
        LOGGER.debug("done read({}): {}".format(size, result))
        return result
