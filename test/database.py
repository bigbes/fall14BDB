import os
import ctypes
import shutil

class DBException(Exception):
    pass

class DBC(ctypes.Structure):
    _fields_ = [
        ('db_size', ctypes.c_size_t),
        ('chunk_size', ctypes.c_size_t),
    ]

class Database(object):
    def __init__(self, name):
        self.dll = ctypes.CDLL(name)
        self.exc = DBException
        self.format_error = (lambda x: "Error")
        self.db = self.dll.dbopen('my.db', ctypes.byref(DBC(16*1024*1024, 4096)))
        if not self.db:
            raise self.exc("Can't create DB")
        self.fput = self.dll.db_put
        self.fget = self.dll.db_get
        self.fget.restype = ctypes.c_void_p
        self.fdel = self.dll.db_del

    def put(self, k, v):
        k_len = len(k)
        k = ctypes.c_char_p(k)
        v_len = len(v)
        v = ctypes.c_char_p(v)
        rc = self.fput(self.db, k, k_len, v, v_len)
        if rc == -1:
            raise self.exc(self.format_error())

    def get(self, k):
        k_len = len(k)
        k = ctypes.c_char_p(k)
        v_len = ctypes.c_int()
        v = ctypes.c_char_p()
        rc = self.fget(self.db, k, k_len, ctypes.byref(v), ctypes.byref(v_len))
        if rc == -1:
            raise self.exc(self.format_error())
        return ctypes.string_at(v, v_len.value)

    def delete(self, k):
        k_len = len(k)
        k = ctypes.c_char_p(k)
        rc = self.fdel(self.db, k, k_len)
        if rc == -1:
            raise self.exc(self.format_error())

    def cleanup(self):
        os.remove('my.db')

    def close(self):
        if self.db:
            self.dll.db_close(self.db)

    def __del__(self):
        self.cleanup()
        self.close()

#############################################
# Child class example for Sophia (Checker)  #
#   Repo: http://github.com/pmwkaa/sophia/  #
# Docs: http://sphia.org/documentation.html #
#############################################
class SophiaException(DBException):
    pass

class Sophia(Database):
    SPDIR     = 0x00

    SPO_RDWR   = 0x02
    SPO_CREAT  = 0x04

    def __init__(self, name=None):
        if name is None:
            name = './libsophia.so'
        self.db   = None
        self.env  = None
        self.exc  = SophiaException
        self.format_error = (lambda x: "Error: " + self.dll.sp_error(self.env))
        self.dll  = ctypes.CDLL('./libsophia.so')
        self.env  = self.dll.sp_env()
        if not self.env:
            raise self.exc('Failed to create ENV')
        rc = self.dll.sp_ctl(self.env, self.SPDIR, self.SPO_CREAT | self.SPO_RDWR, './db')
        if rc == -1:
            raise self.exc(self.format_error())
        self.db   = self.dll.sp_open(self.env)
        if not self.db:
            raise self.exc(self.format_error())
        self.fput = self.dll.sp_set
        self.fget = self.dll.sp_get
        self.fget.restype = ctypes.c_void_p
        self.fdel = self.dll.sp_delete

    def cleanup(self):
        shutil.rmtree('db')

    def close(self):
        if self.db:
            self.dll.sp_destroy(self.db)
        if self.env:
            self.dll.sp_destroy(self.env)

if __name__ == '__main__':
    a = Sophia()
    a.put('1', 'hello, mike')
    assert(a.get('1') == 'hello, mike')
    a.delete('1')
    assert(not a.get('1'))
    a.delete('1')
    a.cleanup()
    a.close()
