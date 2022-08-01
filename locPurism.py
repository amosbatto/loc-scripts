# locPurism.py counts lines of code developed by Purism for the Librem 5
# Shows more info from cloc with the "-d" option: python3 locPurism.py -d
#
# Author: Amos Batto <amosbatto@yahoo.com>
# License: public domain 
# Requires Python 3.6 or later. Needs the "cloc" package installed. In Debian family: sudo apt install cloc

import shutil, subprocess, tempfile, re, os, os.path, sys
from urllib.request import urlretrieve
from urllib.parse import urlparse


projectUrls = {
	"libhandy"   : "https://gitlab.gnome.org/GNOME/libhandy/-/archive/main/libhandy-main.tar.bz2",
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
	print("Lines of code in Purism's projects for the Librem 5:")
	
	totalLoc = 0; #running total of lines of code
	
	for projName, projUrl in projectUrls.items():
		
		tmpDir = tempfile.mkdtemp(prefix="loc-")
		
		a = urlparse(projUrl) 
		compressedFilename = os.path.basename(a.path)
		pathToFileName = os.path.join(tmpDir, compressedFilename)  
		fileName, headers = urlretrieve(projUrl, filename = pathToFileName)
		
		#Get the LOC sum:
		output = subprocess.check_output(["cloc", "--exclude-lang=Markdown,PO File", fileName])
		found = re.search( r'^SUM:.*?\s+(\d+)$', output.decode('utf-8'), re.M)
		
		if found:
			loc = int(found.group(1))
			totalLoc += loc
		else:
			print(f"Error: no SUM of the lines of code in {projName}.")
			sys.exit();
		
		if "-d" in sys.argv[1:] :
			print(projName)
			os.system("cloc --exclude-lang='PO File,Markdown' " + fileName); 
			print('');
		else:
			print(f"\t{projName}: {loc}")
		
		shutil.rmtree(tmpDir) 
	
	print("Total lines of code: " + str(totalLoc));
 
 
if __name__ == "__main__":
	main()
