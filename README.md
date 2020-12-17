# PyLSASS

## Preamble

### Disclaimer
PyLSASS is for educational purposes only, intended to show security flaws that are coming with Windows. This tool comes without any warranty.

**You may not use this software for illegal or unethical purposes. This includes activities which give rise to criminal or civil liability.**

**Under no event shall the licensor be responsible for any activities, or misdeeds, by the licensee.**

## Content
1. [Usage](#1-usage)
2. [See also](#2-see-also)

## 1. Usage

### UAC bypassing
WinPwnage is being used as a implementation of various [UAC bypass techniques](https://github.com/rootm0s/WinPwnage#uac-bypass-techniques). They can be passed to PyLSASS as an attribute:
```python
PyLSASS(bypass_function = uacMethod4)
```

The following list gives an overview on working and non-working techniques (tested on Windows 10).

#### Working
- **silentcleanup scheduled task (Method 4)**
- **cmstp.exe (Method 13)**

#### Non-working
- **runas (Method 1):** only working if UAC is set to never notify
- **fodhelper.exe (Method 2):** blocked by Windows Defender
- **slui.exe (Method 3):** blocked by Windows Defender
- **sdclt.exe (isolatedcommand) (Method 5):** blocked by Windows Defender
- **sdclt.exe (App Paths) (Method 6)**
- **perfmon.exe (Method 7):** runtime error
- **eventvwr.exe (Method 8):** blocked by Windows Defender
- **compmgmtlauncher.exe (Method 9):** blocked by Windows Defender
- **computerdefaults.exe (Method 10):** blocked by Windows Defender
- **token manipulation (Method 11):** runtime error
- **sdclt.exe (Folder) (Method 12):** blocked by Windows Defender
- **wsreset.exe (Method 14):** blocked by Windows Defender
- **slui.exe and changepk.exe (Method 15):** blocked by Windows Defender

## 2. See also
- **[WinPwnage](https://github.com/rootm0s/WinPwnage) by [@rootm0s](https://github.com/rootm0s)**
