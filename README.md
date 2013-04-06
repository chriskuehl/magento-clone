magento-clone
=============

magento-clone (`magec`) is a short script for cloning a Magento installation over SSH in one step.

It handles the following automatically:

1. Quickly downloads the remote Magento installation using SSH and tar (minus `var` which contains only temporary files). This is faster than `rsync` or `scp` with lots of small files.
2. Makes a copy of the remote MySQL database using the credentials in the `local.xml` file downloaded. The backup is
made using `mysqldump` and transferred over SSH.
3. Creates a new database on the local MySQL server and copies all the data into it.
4. Adjusts the local `local.xml` to use the local MySQL server and newly-created database.
5. Adjusts the site URL in the local `core_config_data` to point to a local copy of the site.

### Usage
<pre>
usage: magec remote_path

  remote_path: SCP-style path to Magento root directory
		e.g.: chris@example.com:~/www/magento/public/
</pre>

### Example Output
<pre>
$ magec chris@example.com:~/www/example.com/public/
Cloning from Magento repository on chris@example.com at ~/www/example.com/public/...
86.5MB 0:00:27 [3.12MB/s]
Files cloned in 27s.
Detected MySQL settings:
  Host: localhost
	Username: example
	Password: secret
	DB Name: example
Creating new database on localhost...
New MySQL settings:
	Host: localhost
	Username: magec
	Password: magec
	DB Name: magec_example-com-58505
Copying database from server to local...
 682kB 0:00:08 [  79kB/s]
Database copied in 9s.
Adjusting local.xml with new database information...
Recreating var directory...
Updating core_config_data with new site URL...
Magento cloned successfully.
	New URL: http://example.com.dev/
</pre>

### Shortcomings
Right now `magec` is unlikely to work on any computer except my own. It expects your environment to be configured in a
very specific way:

* **MySQL**
    * **Username:** magec
    * **Password:** magec
    * Full access to `magec_*`
* **URLs**
    * All sites are cloned to `${ORIGINAL_DOMAIN}.dev` with no option to specify an alternative URL
* **Installed Software**
    * python3
    * pv (this does *not* come installed on Ubuntu, but can be installed via `apt-get`)
    * pymysql for python3


Additionally, getting this to work on anything besides *nix is going to take a lot of work since it uses `ssh`, `mysql`,
`pv`, and a bunch of pipes. It's only been tested on Linux Mint 14, but it should work on similar systems and
potentially even OS X.

### Contributing
Please feel free to submit pull requests or fork this script.

### License
`magento-clone` is copyright &copy; 2013 Chris Kuehl and is licensed under an MIT license. See `LICENSE`.
