#!/usr/bin/env python

import sys, os, math, operator
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
    def process(self, item):
        fn = item['file']
        base_path = os.path.join(INPUT_FILE_PATH, fn)
        pdf_path = base_path + '.pdf'
        html_fn = fn + '.new.html'
        html_path = os.path.join(INPUT_FILE_PATH, html_fn)
        original_image_path = base_path + '.png'
        new_image_path = base_path + '.new.png'
        diff_image_path = base_path + '.diff.png'

        path_removed = [html_path, new_image_path, diff_image_path]
        passed = True

        pdf2htmlEX_args = pdf2htmlEX_ARGS
        if 'pdf2html_args' in item:
            pdf2html_args += ' ' + item['pdf2htmlEX_args']

        os.system('pdf2htmlEX ' + pdf2htmlEX_args + ' ' + pdf_path + ' --dest-dir ' + INPUT_FILE_PATH + ' ' + html_fn)

        wkhtmltoimage_args = wkhtmltoimage_ARGS
        if 'html2png_args' in item:
            wkhtmltoimage_args += ' ' + item['html2png_args']

        if self.op == 'test':
            image_path = new_image_path
        else:
            image_path = original_image_path
        os.system('wkhtmltoimage ' + wkhtmltoimage_args + ' ' + html_path + ' ' + image_path)

        if self.op == 'test':
            original_img = Image.open(original_image_path)
            new_img = Image.open(new_image_path)

            diff_img = ImageChops.difference(original_img, new_img);
            passed = diff_img.getbbox() is None
            if not passed:
                # http://stackoverflow.com/questions/15721484/saving-in-png-using-pil-library-after-taking-imagechops-difference-of-two-png
                diff_img.convert('RGB').save(diff_image_path)
                path_removed = []

        for path in path_removed:
            if os.path.exists(path):
                os.remove(path)
        return passed

    def summary(self, failed):
        if len(failed) == 0:
            print 'All tests passed.'
            return

        print len(failed), 'tests' if len(failed) > 1 else 'test', 'failed:'
        for fn in failed:
            print fn

    def run(self, op, fn):
        self.op = op

        failed = []
        for item in manifest:
            if fn == '' or item['file'] == fn:
                if not self.process(item):
                    failed.append(item['file'])

        if self.op == 'test':
            self.summary(failed);


if __name__ == '__main__':
    op = sys.argv[1]
    fn = ''
    if len(sys.argv) > 2:
        fn = sys.argv[2]
    Test().run(op, fn)
