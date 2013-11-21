#!/home/gzhao/mybin/bin/python

print __file__,"is running"
print __file__,"import std modules"
import os
import sys
import time
from optparse import OptionParser
print __file__,"import std modules successfully\n"

print __file__,"import local modules\n"
import facility
print __file__,"import local modules successfully\n"

msg = """
    This is the first release of a very ugly automation script, it is under
/home/gzhao/git/bcm_auto, if the result is failed, you can check make.log
in that directory.
It will need a lot more improvement...
and let's see what we can get as time past!

Thanks
Gary
"""


def MainRun(Destdir="/home/gzhao/git/bcm_auto", maillist="gzhao"):
    os.chdir(Destdir)
    os.system('make deep_clean 2>&1')

    if os.path.isfile("bcm963xx/targets/CLX900/bcmCLX900_nand_fs_image_128.w"):
        print "image exist"
    else:
        res = "image deleted"

    os.system('git pull origin zulu')
    os.system('make >& make.log')

    if os.path.isfile("bcm963xx/targets/CLX900/bcmCLX900_nand_fs_image_128.w"):
        res = "build successfully"
    else:
        res = "build failed"

    facility.Mail2(res, msg)


if __name__ == '__main__':
    parser = OptionParser(usage="usage: %prog [options]", version="%prog 0.1")
    parser.add_option("-m", "--mail", dest="MailList", default="",
            help="when script failed, send a mail to inform others")
    parser.add_option("-d", "--destdir", dest="DestDir",
            default="/home/gzhao/git/bcm_auto",
            help="To locate the directory where the git repos is")

    (options, args) = parser.parse_args()
    os.environ["MAILLIST"] = options.MailList

    MainRun(Destdir = options.DestDir,
           maillist = options.MailList)
