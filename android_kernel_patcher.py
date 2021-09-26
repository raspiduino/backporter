# android_kernel_patcher.py - Simple script for patching upstream the Linux kernel for Android.

# MIT License
#
# Copyright (c) 2021 Giang Vinh Loc
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Usage: [python3] ./android_kernel_patcher.py [stock_kernel_source_dir_to_patch] [linux_kernel_source_of_the_same_version] [linux_kernel_source_upstream]
# Where:
# [stock_kernel_source_dir_to_patch] is the Android kernel from your phone's OEM
# [linux_kernel_source_of_the_same_version] is the Linux kernel in the same version of your Android kernel. For example your phone use 3.18.91 kernel so you should goto https://kernel.org to get the source code of the 3.18 kernel
# [linux_kernel_source_upstream] is the Linux kernel upstream source you want to get patch from
# Eg: python3 ./android_kernel_patcher.py android_kernel_3.18.91/virt/kvm linux_kernel_3.18.91/virt/kvm linux_kernel_4.4.284/virt/kvm

import os, sys

helpstring = '''
Usage: [python3] ./android_kernel_patcher.py [stock_kernel_source_dir_to_patch] [linux_kernel_source_of_the_same_version] [linux_kernel_source_upstream]

Where:
    [stock_kernel_source_dir_to_patch] is the Android kernel from your phone's OEM
    [linux_kernel_source_of_the_same_version] is the Linux kernel in the same version of your Android kernel.
For example your phone use 3.18.91 kernel so you should goto https://kernel.org to get the source code of the 3.18 kernel
    [linux_kernel_source_upstream] is the Linux kernel upstream source you want to get patch from

Eg: python3 ./android_kernel_patcher.py android_kernel_3.18.91/virt/kvm linux_kernel_3.18.91/virt/kvm linux_kernel_4.4.284/virt/kvm
'''

if (sys.argv[1] == "") or ("-h" in sys.argv) or ("--help" in sys.argv) or ("help" in sys.argv):
    print(helpstring)

# Create a directory named 'diff' if it not exist yet

if not os.path.exists("diff"):
    os.system("mkdir diff")

# Find the new files added and removed upstream

filelist = [f for f in os.listdir(sys.argv[1]) if os.path.isfile(sys.argv[1] + "/" + f)]
newfilelist = [f for f in os.listdir(sys.argv[3]) if os.path.isfile(sys.argv[3] + "/" + f)]

added = list(sorted(set(newfilelist) - set(filelist)))
removed = list(sorted(set(filelist) - set(newfilelist)))

# Show the added / removed file

if not added == []:
    print("File added upstream: ", end="")
    print(added)

if not removed == []:
    print("File removed upstream: ", end="")
    print(removed)

# Automatically compare and patch the source

for f in filelist:
    os.system("diff " + sys.argv[2] + "/" + f + " " + sys.argv[1] + "/" + f + " > diff/" + f + ".diff")
    
    cmp = open("diff/" + f + ".diff", "r")
    a = cmp.read()
    
    if a == "":
        print("File " + f + " same!")
        print("Patching...")
        if not f in removed:
            os.system("cp " + sys.argv[3] + "/" + f + " " + sys.argv[1] + "/" + f)
            os.system("rm diff/" + f + ".diff")
    
    else:
        print("File " + f + " diff! See diff/" + f + ".diff")

# Add files upstream

for f in added:
    print("Adding " + f)
    os.system("cp " + sys.argv[3] + "/" + f + " " + sys.argv[1] + "/" + f)
