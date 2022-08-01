# Counts lines of code developed by Purism for the Librem 5
#
# Author: Amos Batto <amosbatto@yahoo.com>
# License: GPL 3.0+ 
# Requires Python 3.6 or later. Need the "cloc" package. In Debian family: sudo apt install cloc

import shutil
import os
import os.path
from urllib.request import urlretrieve
from urllib.parse import urlparse
import subprocess
import tempfile
import re
import pprint


projectUrls = {
	"libhandy"   : "https://gitlab.gnome.org/GNOME/libhandy/-/archive/master/libhandy-master.tar.bz2",
	"libadwaita" : "https://gitlab.gnome.org/GNOME/libadwaita/-/archive/main/libadwaita-main.tar.bz2",
	"calls"      : "https://gitlab.gnome.org/GNOME/calls/-/archive/master/calls-master.tar.bz2",
	"chatty"     : "https://source.puri.sm/Librem5/chatty/-/archive/master/chatty-master.tar.bz2",
	"squeekboard": "https://gitlab.gnome.org/World/Phosh/squeekboard/-/archive/master/squeekboard-master.tar.bz2",
	"libcall-ui" : "https://gitlab.gnome.org/World/Phosh/libcall-ui/-/archive/main/libcall-ui-main.tar.bz2",
	"proc"       : "https://gitlab.gnome.org/World/Phosh/phoc/-/archive/master/phoc-master.tar.bz2",
	"phosh"      : "https://gitlab.gnome.org/World/Phosh/phosh/-/archive/main/phosh-main.tar.bz2",
	"feedbackd"  : "https://source.puri.sm/Librem5/feedbackd/-/archive/master/feedbackd-master.tar.bz2",
	"feedbackd-device-themes": "https://source.puri.sm/Librem5/feedbackd-device-themes/-/archive/master/feedbackd-device-themes-master.tar.bz2",
	"gtherm"     : "https://source.puri.sm/Librem5/gtherm/-/archive/master/gtherm-master.tar.bz2",
	"haegtesse"  : "https://source.puri.sm/Librem5/haegtesse/-/archive/master/haegtesse-master.tar.bz2",
	"wys"        : "https://source.puri.sm/Librem5/wys/-/archive/master/wys-master.tar.bz2" 
}

def main():
	print("Purism's code projects for the Librem 5:")
	
	totalLoc = 0; #running total of lines of code
	
	for projName, projUrl in projectUrls.items():
		
		tmpDir = tempfile.mkdtemp(prefix="loc-")
		
		a = urlparse(projUrl) 
		compressedFilename = os.path.basename(a.path)
		pathToFileName = os.path.join(tmpDir, compressedFilename)  
		fileName, headers = urlretrieve(projUrl, filename = pathToFileName)
		print(projName)
		
		os.system("cloc --exclude-lang='PO File,Markdown' " + fileName); 
		print('');
		
		#Get the sum
		output = subprocess.check_output(["cloc", "--exclude-lang=Markdown,PO File", fileName])
		print(output.decode('utf-8'))
		
		found = re.search( r'^SUM:.*?\s+(\d+)$', output.decode('utf-8'), re.M)
		
		if found:
			totalLoc += int(found.group(1))
			print(found.group(1))
		else:
			print(f"Error: no SUM of the lines of code in {projName}.")
		
		shutil.rmtree(tmpDir) 
	
	print("Total Lines of code: " + str(totalLoc));
 
 
if __name__ == "__main__":
	main()
