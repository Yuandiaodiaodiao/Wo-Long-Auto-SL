from pynput.keyboard import Listener
import threading

def get_key_name(key):
    if hasattr(key, 'char'):
        return key.char
    elif hasattr(key, 'name'):
        return key.name
    return None


from concurrent.futures import ThreadPoolExecutor, wait
threadPool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="exec")
import threading
def raise_exception(thread_id):
    import ctypes
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                     ctypes.py_object(SystemExit))
    if res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
        print('Exception raise failure')

def get_thread_id(thread):
    for id, t in threading._active.items():
        if t is thread:
            return id
def stop():
    global threadPool
    for thread in threadPool._threads:
        id = get_thread_id(thread)
        raise_exception(id)

    threadPool.shutdown(wait=False)
    print("已停止当前全部任务")
    threadPool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="exec")
    print("已重新初始化")


class KListener:
    key_callback = {}
    key_callbackasync={}
    key_callbackasyncn={}
    def __init__(self):
        pass

    def bindKey(self, key, callback):
        self.key_callback[key] = callback

    def bindKeyAsync(self, key, callback,name=""):
        self.key_callbackasync[key] = callback
        self.key_callbackasyncn[key] = name

    def presskey(self, key):
        key = get_key_name(key)
        cb = self.key_callback.get(key)
        if callable(cb):
            cb()
        cb = self.key_callbackasync.get(key)
        if callable(cb):
            global threadPool
            print(key+"已启动"+self.key_callbackasyncn.get(key))
            threadPool.submit(cb)
        if key=="f10":
            stop()


    def join(self):
        print("启动 按f10停止")
        for k,v in self.key_callbackasyncn.items():
            if v == "":continue
            print(k+" "+v)
        with Listener(on_press=lambda x: self.presskey(x)) as listener:
            listener.join()
