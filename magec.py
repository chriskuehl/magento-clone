#!/usr/bin/env python3
# clones a remote Magento installation into the current working directory
import sys, os, time, random
import xml.etree.ElementTree as etree 

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
remote_host = remote_user_host[(remote.find("@") + 1):]
remote_path = remote[(remote.find(":") + 1):]

print("Cloning from Magento repository on {} at {}...".format(remote_user_host, remote_path))

# clone the remote directory into the current directory
start = time.time()
os.system('ssh -C {} "cd {} && tar cf - --exclude=var *" | tar xf -'.format(remote_user_host, remote_path))
end = time.time()

print("Files cloned in {}s.".format(int(end - start)))

# detect MySQL information
conf = etree.parse("app/etc/local.xml")
root = conf.getroot()

nhost = root.find("global/resources/default_setup/connection/host")
nusername = root.find("global/resources/default_setup/connection/username")
npassword = root.find("global/resources/default_setup/connection/password")
ndbname = root.find("global/resources/default_setup/connection/dbname")

thost = nhost.text
tusername = nusername.text
tpassword = npassword.text
tdbname = ndbname.text

print("Detected MySQL settings:")
print("\tHost: {}".format(thost))
print("\tUsername: {}".format(tusername))
print("\tPassword: {}".format(tpassword))
print("\tDB Name: {}".format(tdbname))

# create a new database on localhost
host = "localhost"
username = "magec"
password = "magec"
dbname = "magec_{}-{}".format(remote_host.replace(".", "-"), random.randint(10000, 99999))

print("Creating new database on {}...".format(host))
os.system('echo "CREATE DATABASE \\`{}\\`;" | mysql -u"{}" -p"{}" -h"{}"'.format(dbname, username, password, host))

print("New MySQL settings:")
print("\tHost: {}".format(host))
print("\tUsername: {}".format(username))
print("\tPassword: {}".format(password))
print("\tDB Name: {}".format(dbname))

# copy the data from the old database to the new one
print("Copying database from server to local...")
start = time.time()
os.system('ssh -C {} "mysqldump -u\'{}\' -p\'{}\' -h\'{}\' \'{}\'" | mysql -u"{}" -p"{}" -h"{}" -D"{}"'.format(remote_user_host, tusername, tpassword, thost, tdbname, username, password, host, dbname))
end = time.time()

print("Database copied in {}s.".format(int(end - start)))
