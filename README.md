# iconify

A Python script to batch generate icons from images in a directory.

## Usage

With Python 3.11+ and Git installed, you can run the following:

```sh
pip install git+https://github.com/thegamecracks/iconify
```

Now try `iconify --help` or `python -m iconify --help`:

```sh
usage: iconify.py [-h] [-v] [-s SIZE] [-f] [-m METHOD] [input_dir] [output_dir]

positional arguments:
  input_dir             The directory to read images from (default: .)
  output_dir            The directory to output icons to (default: {input-dir}/{x-size}x{y-size})

options:
  -h, --help            show this help message and exit
  -v, --verbose         Increase logging verbosity
  -s SIZE, --size SIZE  The icon size to output (default: 64x64)
  -f, --force           Overwrite existing icons if necessary
  -m METHOD, --method METHOD
                        Resampling algorithm to use (default: lanczos)
```

When run without any arguments, iconify will generate 64x64 thumbnails
for any images in the current working directory.

## License

This project is written under the MIT license.
