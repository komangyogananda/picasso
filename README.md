# Picasso
A collection of tools for painting super-resolution images

## Requirements
### Python 3.* (tested with 3.5)  
I suggest installing it with [Anaconda](https://www.continuum.io/downloads) which comes bundled with many useful third-party packages and a package manager which removes the pain of building some packages by yourself.

### Python packages
Various Python packages need to be installed. Find out which by looking at either the source code or error messages when running Picasso programs.

## Installation
The described procedure is intended for Windows. The equivalent steps for Linux or OSX are not documented.
Replace any <...> notations according to your situation.
1. Open the console, `cd` to the directory where you want to install and run  
`git clone https://gitlab.com/jungmannlab/picasso.git`  
Alternatively, [download](https://gitlab.com/jungmannlab/picasso) the zip file and unzip it.  
For both options you need approved access on Gitlab.
3. Add `<picasso directory>\scripts` to your PATH environment variable.  
This will make the scripts in this folder accessible in the
console, independent of the current directory.
4. Run this command to register the picasso package in the Python installation.
    - `ECHO <picasso directory> >> <python installation directory>\Lib\site-packages\picasso.pth`
5. Make shortcuts of `gui\*.pyw` files. Open shortcut properties. Prepend shortcut command with `pythonw `. Set the icon to the respective file in the `gui` folder. Move the shortcut to the picasso top level directory. This shortcut can now be double-clicked, pinned to task bar or copied to Desktop.

### Optional steps for your Python environment
* Add `.PY;.PYW` to your `PATHEXT` environment variable.  
The result is that Windows considers these files to be executable, so you don't have to type `.py` or `.pyw` when calling a Python script.
* Depending on your Python installation, Windows might now know that it should call the Python interpreter when running a Python script just by its file name.
If not, run these commands to tell Windows what to do if a `.py` or `.pyw` file is being called:
  - `assoc .py=Python.File`
  - `assoc .pyw=Python.NoConFile`
  - `ftype Python.File=<python installation directory>\python.exe %1 %*`
  - `ftype Python.NoConFile=<python installation directory>\pythonw.exe %1 %*`  

## Contributions & Copyright
Contributors: Joerg Schnitzbauer
Copyright (c) 2015 Jungmann Lab, Max Planck Institute of Biochemistry

## Credits
- Localize icon based on "Mountains by MONTANA RUCOBO from the Noun Project"
- ToRaw icon based on "Lion by Sathish Selladurai from the Noun Project"
- Filter icon based on "Funnel by José Campos from the Noun Project"
- Render icon based on "Paint Palette by Vectors Market from the Noun Project"
