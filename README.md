Test cases for [pdf2htmlEX](https://github.com/coolwanglu/pdf2htmlEX).  

### Dependencies

- pdf2htmlEX (of course)
- wkhtmltoimage
- python2

### Usage of `test.py`

- `./test.py test` - run all the tests
- `./test.py test fn` - run the test with file `fn`
- `./test.py gen` - generate reference images for all tests
- `./test.py gen fn` - generate reference images for file `fn`

### Guidelines for test PDF files

- Make sure you have the proper copyrights.
- Using meaningful file names.
- One page only, unless the test case is about multiple pages.
- Grayscale only, unless the test case is about colors.
- Try your best to remove unnecessary elements.
- Set proper parameters for cropping in `html2png_args`.
- [Optional] Include the source files.

