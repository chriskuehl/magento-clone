#!/usr/bin/env python3
# clones a remote Magento installation into the current working directory
import sys

if len(sys.argv) != 2:
	print("usage: magec remote_path")
	print("")
	print("\tremote_path: SCP-style path to Magento root directory")
	print("\t\te.g.: chris@example.com:~/www/magento/public/")
	sys.exit(1)

remote = sys.argv[1]

if not remote.endswith("/"):
	remote += "/"

print(remote)
