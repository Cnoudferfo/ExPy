To install `pip` and `tkinter` on the Python embeddable package, follow these steps:

### Installing `pip`

1. **Download the Python embeddable package**:
   - Go to the [Python downloads page](https://www.python.org/downloads/windows/) and download the embeddable zip file for your desired Python version.
   - Extract the contents to a directory, e.g., `C:\python`.

2. **Get `pip`**:
   - Download the `get-pip.py` script from [bootstrap.pypa.io](https://bootstrap.pypa.io/get-pip.py).
   - Save it to the directory where you extracted the Python embeddable package, e.g., `C:\python\get-pip.py`.

3. **Install `pip`**:
   - Open a command prompt and navigate to the directory where you extracted Python.
   - Run the following command:
     ```sh
     C:\python\python.exe get-pip.py
     ```
   - This will install `pip` in the `Scripts` directory within your Python installation.

4. **Configure the path**:
   - Open the `_pth` file in your Python directory (e.g., `C:\python\pythonXX._pth`).
   - Uncomment the line `#import site` by removing the `#` at the beginning of the line.
   - Save the file.

### Installing `tkinter`

1. **Download the `tkinter` package**:
   - The embeddable package does not include `tkinter` by default. You need to download the `tkinter` DLLs and supporting files.
   - You can find these files in a standard Python installation or download them from a trusted source.

2. **Place the `tkinter` files**:
   - Copy the `tkinter` files (e.g., `tcl`, `tk`, and `DLLs` related to `tkinter`) into the appropriate directories within your Python embeddable package. Typically, these go into the `DLLs` and `Lib\tkinter` directories.

3. **Verify the installation**:
   - Open a command prompt and run a simple `tkinter` script to ensure everything is set up correctly:
     ```python
     import tkinter as tk
     root = tk.Tk()
     root.mainloop()
     ```

By following these steps, you should have both `pip` and `tkinter` installed and ready to use with your Python embeddable package¹²³.

If you encounter any issues or need further assistance, feel free to ask!

來源: 與 Copilot 的交談， 2024/9/2
(1) Setting up python's Windows embeddable distribution (properly). https://dev.to/fpim/setting-up-python-s-windows-embeddable-distribution-properly-1081.
(2) Installing Python on Windows using the embedded package (no privileges needed) - B. Nikolic Software and Computing Blog. https://bnikolic.co.uk/blog/python/2022/03/14/python-embedwin.html.
(3) embeddable python 安装pip和tkinter_windows embeddable package tkinter-CSDN博客. https://blog.csdn.net/weixin_43320381/article/details/126487822.
(4) Installing Python ,tkinter and Ttkbootstrap on Windows 10/11 Using PIP for GUI Development : 3 Steps - Instructables. https://www.instructables.com/Installing-Python-tkinter-and-Ttkbootstrap-on-Wind/.
(5) undefined. https://www.python.org/downloads/windows/.
(6) undefined. https://bootstrap.pypa.io/get-pip.py.
(7) undefined. https://www.python.org/downloads/windows/%29.
(8) undefined. https://www.python.org/ftp/python/3.9.10/python-3.9.10-embed-amd64.zip.