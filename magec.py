#!/usr/bin/env python3
# clones a remote Magento installation into the current working directory
import sys, os, time

if len(sys.argv) != 2:
	print("usage: magec remote_path")
	print("")
	print("\tremote_path: SCP-style path to Magento root directory")
	print("\t\te.g.: chris@example.com:~/www/magento/public/")
	sys.exit(1)

remote = sys.argv[1]

if not remote.endswith("/"):
	remote += "/"

remote_user_host = remote[:remote.find(":")]
remote_path = remote[(remote.find(":") + 1):]
print(remote_path)

print("Cloning from Magento repository on {} at {}...".format(remote_user_host, remote_path))

# clone the remote directory into the current directory
start = time.time()
os.system('ssh -C {} "cd {} && tar cv - --exclude=var *" | tar xvf -'.format(remote_user_host, remote_path))
end = time.time()

print("Files cloned in {}s.".format(int(end - start)))
