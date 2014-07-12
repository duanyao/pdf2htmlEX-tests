#!/usr/bin/env python

import sys, os, tempfile, shutil, math, operator
from PIL import Image, ImageChops
from manifest import manifest

pdf2htmlEX_ARGS=' '.join([
    '--data-dir share',
    '--external-hint-tool=ttfautohint',
    '--fit-width 800',
    '-l 1',
    '--correct-text-visibility 1',
])

wkhtmltoimage_ARGS=' '.join([
    '-f png',
    '--height 600',
    '--width 800',
    '--quality 0',
    '--quiet'
])

INPUT_FILE_PATH = os.path.join(os.getcwd(), 'files')

class Test:
    def convert_file(self, item):
        fn = item['file']
        pdf_fn = fn + '.pdf'
        html_fn = fn + '.html'
        image_fn = fn + '.png'

        pdf2htmlEX_args = pdf2htmlEX_ARGS
        if 'pdf2html_args' in item:
            pdf2html_args += ' ' + item['pdf2htmlEX_args']

        os.system('pdf2htmlEX ' + pdf2htmlEX_args 
            + ' ' + os.path.join(INPUT_FILE_PATH, pdf_fn) 
            + ' --dest-dir ' + self.temp_dir + ' ' + html_fn)

        wkhtmltoimage_args = wkhtmltoimage_ARGS
        if 'html2png_args' in item:
            wkhtmltoimage_args += ' ' + item['html2png_args']

        os.system('wkhtmltoimage ' + wkhtmltoimage_args 
            + ' ' + os.path.join(self.temp_dir, html_fn) 
            + ' ' + os.path.join(
                (self.temp_dir if self.op == 'test' else INPUT_FILE_PATH),
                image_fn))

    def process(self, item):
        self.convert_file(item)
        if self.op == 'test':
            image_fn = item['file'] + '.png'
            original_img = Image.open(os.path.join(INPUT_FILE_PATH, image_fn))
            new_img = Image.open(os.path.join(self.temp_dir, image_fn))
            
            return ImageChops.difference(original_img, new_img).getbbox() is None

    def summary(self, failed):
        if len(failed) == 0:
            print 'All tests passed.'
            return

        print len(failed), 'tests' if len(failed) > 1 else 'test', 'failed:'
        for fn in failed:
            print fn

    def run(self, op, fn):
        self.op = op
        self.temp_dir = tempfile.mkdtemp()

        failed = []
        for item in manifest:
            if fn == '' or item['file'] == fn:
                if not self.process(item):
                    failed.append(item['file'])

        if self.op == 'test':
            self.summary(failed);

        shutil.rmtree(self.temp_dir)

if __name__ == '__main__':
    op = sys.argv[1]
    fn = ''
    if len(sys.argv) > 2:
        fn = sys.argv[2]
    Test().run(op, fn)
