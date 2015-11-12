#What’s this?

This is a script that can run heedlessly on a Linux machine to notify a user when a course that ran out of spots has an opening in the UF’s ISIS website. The script asks the user for ISIS credentials and a phone number if the user desires to be notified via text message when the course opens up (if it ever does). If the cell phone field is left blank, a notification will be sent to the user’s uf-email account. If the script is left running, the script will continue running for 3 days and then quit. During those three days, it will check the website every three minutes to see if the course became available.

#INSTALL REQUIREMENTS AT YOUR OWN RISK. I CANNOT GUARANTEE IT WILL WORK OR THAT IT WON'T DAMAGE YOUR COMPUTER. FOR ALL I KNOW IT WILL. I GIVE NO WARRANTIES OF ANY KIND.

#Mac requirements

###Note:
Since OS X does not use X server to run GUIs, there’s no way (yet) to run the script headless on OS X (There is an X11 version of firefox available somewhere in the mystical cloud, however it’s downloadable through mac ports and I don’t wanna mess with that. Maybe someone can?)



	brew install caskroom/cask/brew-cask

	#You might need this	
	brew link brew-cask

	brew install Caskroom/cask/firefox

	#If you don’t have pip already	
	easy_install pip

	pip install pyvirtualdisplay selenium




#Linux

###Note: 
I run the script heedlessly on raspberry pi, and the version of firefox for RPI is called iceweasel. I’ll leave installing that to the user. (as easy as: apt-get install iceweasel) 



	
	#as root
	apt-get install firefox

	apt-get install xvfb
	
	#if you don’t have pip already. Why would’t you?
	easy_install pip

	pip install pyvirtualdisplay selenium



#How to use?

The script will ask you for your Gatorlink account, your password, the term you’re trying to register for and the course code (e.g ENC1102), it will also ask you for you cell phone number and your carrier given like (354-543-1234,att). And the supported carries as of now are att, tmobile, verizon, metropcs and sprint (I have only tested att and tmobile). Adding more carriers is not hard, so may someone can?


		
