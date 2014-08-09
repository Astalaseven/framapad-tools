framapad-tools
==============

Inspired by @Framartin framapad-tools repository
https://github.com/Framartin/framapad-tools

Tested on Linux and Windows.

## Windows

In case of `sqlite3.DatabaseError: file is encrypted or is not a database` error, you may need to upgrade your python sqlite version 
from [Sqlite.org](http://www.sqlite.org/download.html): 
[32 bit](http://www.sqlite.org/2014/sqlite-dll-win32-x86-3080500.zip) or [64 bit](http://www.sqlite.org/2014/sqlite-dll-win64-x64-3080500.zip).

The downloaded file must be set in your python DLL's folder, `C:\Python27\DLLs` in my case, and replace the old `sqlite.dll`.
