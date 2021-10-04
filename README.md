### Hexlet tests and linter status:
[![Actions Status](https://github.com/akocur/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/akocur/python-project-lvl3/actions) [![Linter](https://github.com/akocur/python-project-lvl3/actions/workflows/linter.yml/badge.svg?branch=main)](https://github.com/akocur/python-project-lvl3/actions/workflows/linter.yml)

### CODE CLIMATE:
[![Maintainability](https://api.codeclimate.com/v1/badges/db50853f35014076437e/maintainability)](https://codeclimate.com/github/akocur/python-project-lvl3/maintainability)[![Test Coverage](https://api.codeclimate.com/v1/badges/db50853f35014076437e/test_coverage)](https://codeclimate.com/github/akocur/python-project-lvl3/test_coverage)

###
PageLoader is a command-line utility that downloads pages from the Internet and saves them on your computer. Together with the page, it downloads all resources (images, styles and js), allowing you to open the page without the Internet.

## Usage:

### As CLI tool:
```
> page-loader --help
usage: page-loader [options] <url>

PageLoader is a command-line utility that downloads pages from the Internet and saves them on your computer. Together with the page, it downloads all resources (images, styles and js), allowing you to open the page without the Internet.

positional arguments:
  url

optional arguments:
  -o [dir], --out [dir]
                        output directory where the specified url is saved (default:
                        /home/sense/projects/python-project-lvl3)
  -h, --help            display help for command
```

### Demo:
[![asciicast](https://asciinema.org/a/vq7tAa3St57ZJZXw8J1SVaOvt.svg)](https://asciinema.org/a/vq7tAa3St57ZJZXw8J1SVaOvt)