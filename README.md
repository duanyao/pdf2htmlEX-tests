Test cases for [pdf2htmlEX](https://github.com/coolwanglu/pdf2htmlEX).  

### Dependencies

- pdf2htmlEX (of course)
- wkhtmltoimage
- python2

### Guidelines for test PDF files

- Make sure you have the proper copyrights.
- Using meaning file names.
- One page only.
- Grayscale only, unless the test case is about colors.
- Minimized, removed unnecessary elements.
- Set proper parameters for cropping in `html2png_args`.
