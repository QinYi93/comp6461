
def setdefaulttimeout(timeout): # real signature unknown; restored from __doc__
    """
    setdefaulttimeout(timeout)

    Set the default timeout in seconds (float) for new socket objects.
    A value of None indicates that new socket objects have no timeout.
    When the socket module is first imported, the default is None.
    """
    pass


class coding():
    # str is utf8, 1 utf8 character = 3 byte
    def str2bigByte(self, str):
        return str.encode("utf-8")
    # str is utf8, 1 utf8 character = 3 byte
    def bigByte2str(self, byte):
        return byte.decode("utf-8")
    # for sequence #
    def intTo4bigByte(self, seq_num):
        return seq_num.to_bytes(4, byteorder='big')
    # for port
    def intTo2bigByte(self, port):
        return port.to_bytes(2, byteorder='big')
    # for each part of ip
    def intTo1bigByte(self, ip):
        return ip.to_bytes(1, byteorder='big')
class SocketType(object):
    def bind(self, address):  # real signature unknown; restored from __doc__
        """
        bind(address)

        Bind the socket to a local address.  For IP sockets, the address is a
        pair (host, port); the host must refer to the local host. For raw packet
        sockets the address is a tuple (ifname, proto [,pkttype [,hatype]])
        """
        pass

    def close(self):  # real signature unknown; restored from __doc__
        """
        close()

        Close the socket.  It cannot be used after this call.
        """
        pass

    def connect(self, address):  # real signature unknown; restored from __doc__
        """
        connect(address)

        Connect the socket to a remote address.  For IP sockets, the address
        is a pair (host, port).
        """
        pass

    def connect_ex(self, address):  # real signature unknown; restored from __doc__
        """
        connect_ex(address) -> errno

        This is like connect(address), but returns an error code (the errno value)
        instead of raising an exception when an error occurs.
        """
        pass

    def detach(self):  # real signature unknown; restored from __doc__
        """
        detach()

        Close the socket object without closing the underlying file descriptor.
        The object cannot be used after this call, but the file descriptor
        can be reused for other purposes.  The file descriptor is returned.
        """
        pass

    def fileno(self):  # real signature unknown; restored from __doc__
        """
        fileno() -> integer

        Return the integer file descriptor of the socket.
        """
        return 0

    def getpeername(self):  # real signature unknown; restored from __doc__
        """
        getpeername() -> address info

        Return the address of the remote endpoint.  For IP sockets, the address
        info is a pair (hostaddr, port).
        """
        pass

    def getsockname(self):  # real signature unknown; restored from __doc__
        """
        getsockname() -> address info

        Return the address of the local endpoint.  For IP sockets, the address
        info is a pair (hostaddr, port).
        """
        pass

    def getsockopt(self, level, option, buffersize=None):  # real signature unknown; restored from __doc__
        """
        getsockopt(level, option[, buffersize]) -> value

        Get a socket option.  See the Unix manual for level and option.
        If a nonzero buffersize argument is given, the return value is a
        string of that length; otherwise it is an integer.
        """
        pass

    def gettimeout(self):  # real signature unknown; restored from __doc__
        """
        gettimeout() -> timeout

        Returns the timeout in seconds (float) associated with socket
        operations. A timeout of None indicates that timeouts on socket
        operations are disabled.
        """
        return timeout

    def ioctl(self, cmd, option):  # real signature unknown; restored from __doc__
        """
        ioctl(cmd, option) -> long

        Control the socket with WSAIoctl syscall. Currently supported 'cmd' values are
        SIO_RCVALL:  'option' must be one of the socket.RCVALL_* constants.
        SIO_KEEPALIVE_VALS:  'option' is a tuple of (onoff, timeout, interval).
        SIO_LOOPBACK_FAST_PATH: 'option' is a boolean value, and is disabled by default
        """
        return 0

    def listen(self, backlog=None):  # real signature unknown; restored from __doc__
        """
        listen([backlog])

        Enable a server to accept connections.  If backlog is specified, it must be
        at least 0 (if it is lower, it is set to 0); it specifies the number of
        unaccepted connections that the system will allow before refusing new
        connections. If not specified, a default reasonable value is chosen.
        """
        pass

    def recv(self, buffersize, flags=None):  # real signature unknown; restored from __doc__
        """
        recv(buffersize[, flags]) -> data

        Receive up to buffersize bytes from the socket.  For the optional flags
        argument, see the Unix manual.  When no data is available, block until
        at least one byte is available or until the remote end is closed.  When
        the remote end is closed and all data is read, return the empty string.
        """
        pass

    def recvfrom(self, buffersize, flags=None):  # real signature unknown; restored from __doc__
        """
        recvfrom(buffersize[, flags]) -> (data, address info)

        Like recv(buffersize, flags) but also return the sender's address info.
        """
        pass

    def recvfrom_into(self, buffer, nbytes=None, flags=None):  # real signature unknown; restored from __doc__
        """
        recvfrom_into(buffer[, nbytes[, flags]]) -> (nbytes, address info)

        Like recv_into(buffer[, nbytes[, flags]]) but also return the sender's address info.
        """
        pass

    def recv_into(self, buffer, nbytes=None, flags=None):  # real signature unknown; restored from __doc__
        """
        recv_into(buffer, [nbytes[, flags]]) -> nbytes_read

        A version of recv() that stores its data into a buffer rather than creating
        a new string.  Receive up to buffersize bytes from the socket.  If buffersize
        is not specified (or 0), receive up to the size available in the given buffer.

        See recv() for documentation about the flags.
        """
        pass

    def send(self, data, flags=None):  # real signature unknown; restored from __doc__
        """
        send(data[, flags]) -> count

        Send a data string to the socket.  For the optional flags
        argument, see the Unix manual.  Return the number of bytes
        sent; this may be less than len(data) if the network is busy.
        """
        pass

    def sendall(self, data, flags=None):  # real signature unknown; restored from __doc__
        """
        sendall(data[, flags])

        Send a data string to the socket.  For the optional flags
        argument, see the Unix manual.  This calls send() repeatedly
        until all data is sent.  If an error occurs, it's impossible
        to tell how much data has been sent.
        """
        pass

    def sendto(self, data, flags=None, *args,
               **kwargs):  # real signature unknown; NOTE: unreliably restored from __doc__
        """
        sendto(data[, flags], address) -> count

        Like send(data, flags) but allows specifying the destination address.
        For IP sockets, the address is a pair (hostaddr, port).
        """
        pass

    def setblocking(self, flag):  # real signature unknown; restored from __doc__
        """
        setblocking(flag)

        Set the socket to blocking (flag is true) or non-blocking (false).
        setblocking(True) is equivalent to settimeout(None);
        setblocking(False) is equivalent to settimeout(0.0).
        """
        pass

    def setsockopt(self, level, option, value):  # real signature unknown; restored from __doc__
        """
        setsockopt(level, option, value: int)
        setsockopt(level, option, value: buffer)
        setsockopt(level, option, None, optlen: int)

        Set a socket option.  See the Unix manual for level and option.
        The value argument can either be an integer, a string buffer, or
        None, optlen.
        """
        pass

    def settimeout(self, timeout):  # real signature unknown; restored from __doc__
        """
        settimeout(timeout)

        Set a timeout on socket operations.  'timeout' can be a float,
        giving in seconds, or None.  Setting a timeout of None disables
        the timeout feature and is equivalent to setblocking(1).
        Setting a timeout of zero is the same as setblocking(0).
        """
        pass

    def share(self, process_id):  # real signature unknown; restored from __doc__
        """
        share(process_id) -> bytes

        Share the socket with another process.  The target process id
        must be provided and the resulting bytes object passed to the target
        process.  There the shared socket can be instantiated by calling
        socket.fromshare().
        """
        return b""

    def shutdown(self, flag):  # real signature unknown; restored from __doc__
        """
        shutdown(flag)

        Shut down the reading side of the socket (flag == SHUT_RD), the writing side
        of the socket (flag == SHUT_WR), or both ends (flag == SHUT_RDWR).
        """
        pass

    def _accept(self):  # real signature unknown; restored from __doc__
        """
        _accept() -> (integer, address info)

        Wait for an incoming connection.  Return a new socket file descriptor
        representing the connection, and the address of the client.
        For IP sockets, the address info is a pair (hostaddr, port).
        """
        pass

    def __del__(self, *args, **kwargs):  # real signature unknown
        pass

    def __getattribute__(self, *args, **kwargs):  # real signature unknown
        """ Return getattr(self, name). """
        pass

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass

socket = SocketType

class timeout(OSError):
    # no doc
    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    __weakref__ = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """list of weak references to the object (if defined)"""