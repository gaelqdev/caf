# CAF

Clip and Filtering GeoTIFF datasets

## Getting Started

Clone the repository on your local machine :

```
git clone https://github.com/gaelqdev/caf.git
```

### Prerequisites

Install python3 (the project has been developed with Python 3.7.4), see: https://www.python.org/downloads/

Install [rasterio](https://rasterio.readthedocs.io/en/stable/intro.html)

```
python3 -m pip install --user rasterio
```

Install [scipy](https://www.scipy.org) and [numpy](https://www.numpy.org)

```
python3 -m pip install --user numpy scipy
```

### Running

The program is run with the command:

```
python3 main.py input [-c x y width height] [-o output]
```

#### Options and arguments
* input     : name of the input file
* -c        : coordinates of the clip origin and size of the clip. Ex: -c 400 400 1000 1000
* -h        : print this help message and exit (also --help)
* -o        : name of the output file

#### Examples
Filtering a complete GeoTIFF file:
```
 python3 main.py ilatlon_float.tif
 ```

 Filtering a complete GeoTIFF file and set the output file name:
 ```
  python3 main.py ilatlon_float.tif -o out.tif
  ```

  Filtering a clip inside a GeoTIFF file. The position of the upper left corner of the clip is [200,500], the width of the clip is 1000, the height is 800:
  ```
   python3 main.py ilatlon_float.tif -c 200 500 1000 800 -o out.tif
   ```

### Running the tests

[test_caf.py](https://github.com/gaelqdev/caf/blob/master/test_caf.py) contains Unit Tests

To run the tests:

```
 python3 test_caf.py
 ```
