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

def MainRun(Destdir="/home/gzhao/git/bcm_auto", Maillist="gzhao", Logdir=""):

    if os.path.isdir(Logdir):
        logpath = Logdir + time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime()) + '/'
    else:
        print "Log dir is invalid"
        return

    os.mkdir(logpath)
    print logpath

    os.chdir(Destdir)
    os.system('make deep_clean')

    if os.path.isfile("bcm963xx/targets/CLX900/bcmCLX900_nand_fs_image_128.w"):
        print "image exist, deep clean failed? Never mind,  deleted it first"
        os.remove("bcm963xx/targets/CLX900/bcmCLX900_nand_fs_image_128.w")
    else:
        res = "image deleted"

    msg = "Build commit:\n\n"
    commitOld = os.popen('git log -1').read()
    os.system('git pull origin zulu')
    commitNew = os.popen('git log -1').read()
    msg += commitNew

    if commitOld == commitNew:
        print "There has no update"
        res = "No need for 900 local build now"
        msg += "\nThere has no update from server side, do not build this time\n"
    else:

        msg += "\n=======================================================================\n"
        msg += "\nLog dir is " + logpath + "\n"
        msg += "\n=======================================================================\n"

        os.system('make >& ' + logpath + 'make.log')
        print msg

        if os.path.isfile("bcm963xx/targets/CLX900/bcmCLX900_nand_fs_image_128.w"):
            res = "900 local build successfully"
        else:
            res = "900 local build failed"
            msg += "\nLast make log:\n"
            msg += os.popen('tail -n 50 ' + logpath + 'make.log').read()

        msg += "\n\nThis is an auto send E-mail, please do not reply."
        print res
        print msg

    facility.Mail2(res, msg, From = "Builder@nanlnx-dragon")


if __name__ == '__main__':
    parser = OptionParser(usage="usage: %prog [options]", version="%prog 0.1")

    parser.add_option("-m", "--mail", dest="MailList", default="",
            help="when script failed, send a mail to inform others")

    parser.add_option("-d", "--destdir", dest="DestDir",
            default="/home/gzhao/git/bcm_auto",
            help="To locate the directory where the git repos is")

    parser.add_option("-l", "--logdir", dest="LogDir", default="",
            help="Use to set the log file directory")

    (options, args) = parser.parse_args()
    os.environ["MAILLIST"] = options.MailList

    MainRun(Destdir = options.DestDir,
           Maillist = options.MailList,
           Logdir = options.LogDir)
