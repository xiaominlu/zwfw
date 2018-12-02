# -*- coding: UTF-8 -*-
import wx
from multiprocessing.pool import ThreadPool
from check_required_field import HttpManager
import threading
import logging
import os
if not os.path.exists(u'logs'):
    os.mkdir(u'logs')
if not os.path.exists(u'results'):
    os.mkdir(u'results')
EVT_RESULT_ID = wx.NewId()

class ThreadOne(threading.Thread):
    def __init__(self, notify_window, path):
        threading.Thread.__init__(self)
        self.path = path
        self.notify_window = notify_window
        self.start()

    def run(self):
        thread_pool = ThreadPool(15)
        with open(self.path) as fd:
            lines = fd.readlines()
        for line in lines:
            line = line.strip()
            username, password = line.split(u',')
            thread_pool.apply_async(self.check, (username, password,))
        thread_pool.close()
        thread_pool.join()
        wx.PostEvent(self.notify_window, ResultEvent(u'运行结束'))


    def check(self, username, password):
        threading.currentThread().setName(username)
        print username
        logger = logging.getLogger(threading.currentThread().getName())
        file_handler = logging.FileHandler(u'logs/%s.log' % threading.currentThread().getName())
        formatter = logging.Formatter(u'%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
        http_manager = HttpManager(u'221.226.253.51', u'5065')
        check_result = http_manager.check(username, password, 2)
        if check_result == 2:
            wx.PostEvent(self.notify_window, ResultEvent(u'帐号%s密码不正确\r\n' % username))
        elif check_result == 1:
            wx.PostEvent(self.notify_window, ResultEvent(u'帐号%s中有数据没有必填\r\n' % username))
        else:
            wx.PostEvent(self.notify_window, ResultEvent(u'帐号%s检查数据正确\r\n' % username))

class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, message):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.message = message


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, u'统计错误信息',
                          size=(600, 300), style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.Centre()
        self.path = None
        open_button = wx.Button(self, label=u'打开')
        open_button.Bind(wx.EVT_BUTTON, self.__open_file)
        self.execute_button = wx.Button(self, label=u'运行')
        self.execute_button.Bind(wx.EVT_BUTTON, self.__execute)
        box = wx.BoxSizer()
        box.Add(open_button, wx.SizerFlags().Border(wx.ALL, 3))
        box.Add(self.execute_button, wx.SizerFlags().Border(wx.ALL, 3))
        self.content_text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        label = wx.StaticText(self, -1, u'运行结果:')
        v_box = wx.BoxSizer(wx.VERTICAL)  # wx.VERTICAL参数表示实例化一个垂直尺寸器
        self.file_path = wx.StaticText(self, -1, u'文件路径:')
        v_box.Add(box)
        v_box.Add(self.file_path)
        v_box.Add(label)
        v_box.Add(self.content_text, wx.SizerFlags(5).Expand().Border(wx.ALL, 3))
        self.SetSizer(v_box)
        self.Connect(-1, -1, EVT_RESULT_ID, self.__on_result)


    def __open_file(self, event):
        filesFilter = "txt (*.txt)|*.txt||"
        fileDialog = wx.FileDialog(self, message=u'选择文件', defaultDir=os.getcwd(), wildcard=filesFilter, style=wx.FD_OPEN)
        dialogResult = fileDialog.ShowModal()
        if dialogResult != wx.ID_OK:
            return
        self.path = fileDialog.GetPath()
        self.file_path.SetLabelText(u'文件路径:%s' % self.path)

    def __execute(self, event):
        if self.path is None or not os.path.exists(self.path):
            self.content_text.AppendText(u'输入的文件路径不正确, 请重新输入!\r\n')
            # self.content_text.flush()
            return
        ThreadOne(self, self.path)
        self.execute_button.Disable()

    def __on_result(self, event):
        """Show Result status."""
        if event.message is not None:
            self.content_text.AppendText(event.message)
            if event.message == u'运行结束':
                self.execute_button.Enable()





if __name__ == u'__main__':
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()

