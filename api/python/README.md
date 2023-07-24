## Running the Python examples

To run the Python examples you will need to:

1. Install the `vna` Python package
2. Copy the necessary platform-specific libraries from the PicoVNA 5 SDK into a directory where Python can locate them.

### Installing the vna Python package

The `vna` Python package can be installed in the usual way via PyPI. Use:

```
pip install vna
```


### Platform-specific libraries

You will need to copy the following files from the downloadable SDK to somewhere Python can find them. In the simplest case (if your Python script will be in the working directory), copy all of the files into the same directory as your Python script.

Windows: `_vna_python.pyd`, `vna.lib`, `vna_python.lib`, `vna.dll`, `ftd2xx.dll`

Linux: `_vna_python.so`, `libvna.so` and `libftd2xx.so`

macOS: `_vna_python.dylib`, `libvna.dylib` and `libftd2xx.dylib`



### Diagnosing import errors

If you see an error similar to `ImportError: ... No such file or directory` then `_vna_python.so` (or `_vna_python.pyd` on Windows, or `_vna_python.dylib` on macOS) is not being found. On Windows, make sure `_vna_python.pyd` is in a suitable location (for example, the directory that the Python interpreter is being invoked from). On Linux, the easiest workaround is to set the `LD_LIBRARY_PATH` environment variable to the directory it is found in:

`LD_LIBRARY_PATH=example python3 example.py`

On macOS, the equivalent command would be:

`DYLD_LIBRARY_PATH=example python3 example.py`


### Diagnosing ModuleNotFound errors

If you see the error `ModuleNotFoundError: No module named 'vna'`, then the `vna` package has not been correctly installed from PyPI.


### Notes for Windows users

On Windows, make sure to copy the correct libraries from the SDK for your version of Python.

For Python version 3.X, copy files from vna5_sdk/python/windows/python3X (where X may be 8, 9, 10 or 11).

If you do not know what version of Python you are using, the following Python code will tell you:

```
import sys
print(f"{sys.version}")
```

(or alternatively type `python3 --version` at the command prompt)



