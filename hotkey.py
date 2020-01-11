# _*_ coding: utf-8 _*_
import win32con
import ctypes
import ctypes.wintypes
import threading


class HotKey(threading.Thread):

    def __init__(self):
        """
        super the init of Thread and init the para using later
        hot_key_id_dict: key is the hot key id,
                         value is info about hot key using to register
        hot_func_dict: key is the hot key id, value records the function that be executed when hot key was pressed
        """
        super().__init__()
        self.user32 = ctypes.windll.user32
        self.hot_key_dict = {}
        self.hot_func_dict = {}

    def register_key(self, hwnd=None, flag_id=0, fn_key=0, vk_ey=None, func=None):
        """
        get info that uses to register hot key, record in hot_key_id_dict and set its values False
        if the id have been in hot_key_id_dict, the hot key would be override
        :param hwnd: Handle who response when hot key was pressed
        :param flag_id: hot key id which need to be recorded in hot_key_id_dict.keys()
        :param fn_key: like ctrl and alt
        :param vk_ey: normal key like a ~ z
        :param func: the function executed when hot key pressed
        """
        if vk_ey and func:
            self.hot_key_dict[flag_id] = [hwnd, flag_id, fn_key, vk_ey, False]
            self.hot_func_dict[flag_id] = func

    def run(self):
        """
        specify activity by override run();
        as written in Thread, when start(), run() would be executed
        content: when hot_key pressed, set start signal
        tips: register master in run, maybe hot key only be useful in on thread
        """
        for values in self.hot_key_dict.values():
            rst = self.user32.RegisterHotKey(values[0], values[1], values[2], values[3])
        self.controller()
        try:
            msg = ctypes.wintypes.MSG()
            while 1:
                if self.user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                    if msg.message == win32con.WM_HOTKEY:
                        if msg.wParam in self.hot_key_dict.keys():
                            self.hot_key_dict[msg.wParam][-1] = True
                    self.user32.TranslateMessage(ctypes.byref(msg))
                    self.user32.DispatchMessageA(ctypes.byref(msg))
        finally:
            for i in self.hot_key_dict.keys():
                self.user32.UnregisterHotKey(None, i)

    def controller(self):
        """
        wait signal to start function
        """
        self.thread_it(self.inner)

    def inner(self):
        """
        when  hot_key_id_dict[id] = True, function start
        """
        while 1:
            for key, value in self.hot_func_dict.items():
                if self.hot_key_dict[key][-1]:
                    self.thread_it(value)
                    self.hot_key_dict[key][-1] = False

    def exit_it(self):
        try:
            for i in self.hot_key_dict.keys():
                self.user32.UnregisterHotKey(None, i)
        except Exception:
            pass
        self._stop()

    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()


if __name__ == '__main__':
    pass
