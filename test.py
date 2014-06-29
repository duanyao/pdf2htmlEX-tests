#!/usr/bin/env python

import sys, os, tempfile, shutil, math, operator
from PIL import Image, ImageChops
from manifest import manifest

pdf2htmlEX_ARGS=' '.join([
    '--data-dir share',
    '--external-hint-tool=ttfautohint',
    '--fit-width 800',
    '-l 1',
])

wkhtmltoimage_ARGS=' '.join([
    '-f png',
    '--height 600',
    '--width 800',
    '--quality 90',
    '--quiet'
])

FILE_PATH = os.path.join(os.getcwd(), 'files')

class Test:
    def process(self, item):
        fn = item['file']
        pdf_fn = fn + '.pdf'
        html_fn = fn + '.html'
        image_fn = fn + '.png'

        pdf2htmlEX_args = pdf2htmlEX_ARGS
        if 'pdf2html_args' in item:
            pdf2html_args += ' ' + item['pdf2htmlEX_args']

        if self.op == 'gen':
            os.system('pdf2htmlEX ' + pdf2htmlEX_args + ' ' + os.path.join(FILE_PATH, pdf_fn) + ' --dest-dir ' + FILE_PATH + ' ' + html_fn)

        wkhtmltoimage_args = wkhtmltoimage_ARGS
        if 'html2png_args' in item:
            wkhtmltoimage_args += ' ' + item['html2png_args']

        if self.op == 'test':
            dest_dir = self.temp_dir
        else:
            dest_dir = FILE_PATH
        os.system('wkhtmltoimage ' + wkhtmltoimage_args + ' ' + os.path.join(FILE_PATH, html_fn) + ' ' + os.path.join(dest_dir, image_fn))

        if self.op == 'test':
            original_img = Image.open(os.path.join(FILE_PATH, image_fn))
            new_img = Image.open(os.path.join(self.temp_dir, image_fn))
            
            ImageChops.difference(original_img, new_img).getbbox() is None

            #h = ImageChops.difference(original_img, new_img).histogram()
            #rms = math.sqrt(reduce(operator.add,
            #    map(lambda h, i: h*(i**2), h, range(256))
            #    ) / (float(original_img.size[0]) * original_img.size[1]))
            #print rms
            

    def run(self, op, fn):
        self.op = op
        if op == 'test':
            self.temp_dir = tempfile.mkdtemp()
        for item in manifest:
            if fn == '' or item['file'] == fn:
                self.process(item)
        if op == 'test':
            shutil.rmtree(self.temp_dir)

if __name__ == '__main__':
    op = sys.argv[1]
    fn = ''
    if len(sys.argv) > 2:
        fn = sys.argv[2]
    Test().run(op, fn)
