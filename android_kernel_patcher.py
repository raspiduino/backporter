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

# For automatically patching:
# [python3] ./android_kernel_patcher.py [stock_kernel_source_dir_to_patch] [linux_kernel_source_of_the_same_version] [linux_kernel_source_upstream]
#
# Where:
# [stock_kernel_source_dir_to_patch] is the Android kernel from your phone's OEM
# [linux_kernel_source_of_the_same_version] is the Linux kernel in the same version of your Android kernel. For example your phone use 3.18.91 kernel so you should goto https://kernel.org to get the source code of the 3.18 kernel
# [linux_kernel_source_upstream] is the Linux kernel upstream source you want to get patch from
# Eg: python3 ./android_kernel_patcher.py android_kernel_3.18.91/virt/kvm linux_kernel_3.18.91/virt/kvm linux_kernel_4.4.284/virt/kvm
#
# Or:
# Eg: python3 ./android_kernel_patcher.py android_kernel_3.18.91/ linux_kernel_3.18.91/ linux_kernel_4.4.284/ -p virt/kvm
#
# Where -p follow by the directory you want to patch.
#
# For undo the patch:
# [python3] ./android_kernel_patcher.py undo
# And that's all :)

# Thanks for using my script!

import os, sys

helpstring = '''
Usage: [python3] ./android_kernel_patcher.py [stock_kernel_source_dir_to_patch] [linux_kernel_source_of_the_same_version] [linux_kernel_source_upstream] [-p] [path_to_patch_in_tree]

Where:
    [stock_kernel_source_dir_to_patch] is the Android kernel from your phone's OEM
    [linux_kernel_source_of_the_same_version] is the Linux kernel in the same version of your Android kernel.
For example your phone use 3.18.91 kernel so you should goto https://kernel.org to get the source code of the 3.18 kernel
    [linux_kernel_source_upstream] is the Linux kernel upstream source you want to get patch from

Eg: python3 ./android_kernel_patcher.py android_kernel_3.18.91/virt/kvm linux_kernel_3.18.91/virt/kvm linux_kernel_4.4.284/virt/kvm
'''

# Print helpstring
if (len(sys.argv) == 1) or ("-h" in sys.argv) or ("--help" in sys.argv) or ("help" in sys.argv):
    print(helpstring)
    exit(0)

if (sys.argv[1] == "undo"):
    backuplist = [f for f in os.listdir("backup") if os.path.isfile(sys.argv[1] + "/" + f)]

    # Get the previous path
    f = open("backup/path.backporter.txt", "r")
    previous_path = f.read()
    f.close()

    for f in backuplist:
        os.system("cp backup/" + f + " " + previous_path + "/")
    exit(0)

# Add path if -p specified
if len(sys.argv) > 4:
    if sys.argv[4] == "-p":
        for i in range(1,4):
            sys.argv[i] += "/" + sys.argv[5]

# Create a directory named 'diff' if it not exist yet
if not os.path.exists("diff"):
    os.system("mkdir diff")

# Create a directory named 'backup' if not exist yet
if not os.path.exists("backup"):
    os.system("mkdir backup")

# Find the new files added and removed upstream
filelist = [f for f in os.listdir(sys.argv[1]) if os.path.isfile(sys.argv[1] + "/" + f)]
newfilelist = [f for f in os.listdir(sys.argv[3]) if os.path.isfile(sys.argv[3] + "/" + f)]

added = list(sorted(set(newfilelist) - set(filelist)))
removed = list(sorted(set(filelist) - set(newfilelist)))

difflist = []

# Show the added / removed file
if not added == []:
    print("File added upstream: ", end="")
    print(added)

if not removed == []:
    print("File removed upstream: ", end="")
    print(removed)

# Add file path to automatically revert (if needed)
f = open("backup/path.backporter.txt", "w")
f.write(sys.argv[1])
f.close()

# Automatically compare and patch the source
for f in filelist:
    os.system("diff " + sys.argv[2] + "/" + f + " " + sys.argv[1] + "/" + f + " > diff/" + f + ".diff")
    
    cmp = open("diff/" + f + ".diff", "r")
    a = cmp.read()
    cmp.close()
    
    if a == "":
        print("File " + f + " same!")
        print("Patching...")
        
        # Backup
        os.system("cp " + sys.argv[1] + "/" + f + " backup/")

        # Patch
        if not f in removed:
            os.system("cp " + sys.argv[3] + "/" + f + " " + sys.argv[1] + "/" + f)
            os.system("rm diff/" + f + ".diff")
    
    else:
        os.system("diff " + sys.argv[3] + "/" + f + " " + sys.argv[1] + "/" + f + " > diff/" + f + ".diff")
    
        cmp = open("diff/" + f + ".diff", "r")
        a = cmp.read()
        cmp.close()

        if a == "":
            print("File " + f + " already patched! Abort.")
        else:
            difflist.append(f) # Add to diff list for showing later
            print("File " + f + " diff! See diff/" + f + ".diff")

# Add files upstream
for f in added:
    print("Adding " + f)
    os.system("cp " + sys.argv[3] + "/" + f + " " + sys.argv[1] + "/" + f)

# Print diff list
print("Diff list:")
difflist.sort()
print(difflist)
