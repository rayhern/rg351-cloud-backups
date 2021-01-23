#
# Sync all my save games with all my devices, including Google Drive.
# Starting with Diablo.
# By Ray Hernandez
#
#

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# For using listdir() 
import os 
import time
import sys
import shutil
import sys
    
# Credentials for linux handheld / raspberry pi / rg350 / rg351
SSH_IP_ADDRESS = config['connection']['DEVICE_IP']
SSH_USER = config['connection']['DEVICE_USER']
SSH_PASSWORD = config['connection']['DEVICE_PASS']

# Save file paths
REMOTE_PSP_PATH = config['remote']['PSP_SAVE_PATH']
REMOTE_GBA_PATH = config['remote']['GBA_SAVE_PATH']
REMOTE_GBC_PATH = config['remote']['GBC_SAVE_PATH']
REMOTE_GB_PATH = config['remote']['GB_SAVE_PATH']
REMOTE_PSX_PATH= config['remote']['PSX_SAVE_PATH']
REMOTE_DIABLO_PATH = config['remote']['DIABLO_PATH']

LOCAL_DIABLO_PATH = "/Users/ray/Library/Application Support/diasurgical/devilution/"
# Make sure that you install the google drive client on your mac/pc.
LOCAL_GOOGLE_DRIVE_PATH = "/Users/ray/Google Drive File Stream/My Drive/Saved Games"
TEMP_SAVE_PATH = os.getcwd() + "/saves"

def main():
    global RSYNC_DIABLO_PATH,RSYNC_PSX_PATH,RSYNC_GBA_PATH, MAC_DIABLO_PATH, GOOGLE_DRIVE_SAVE_DIR
    global TEMP_SAVE_PATH
    if not os.path.exists(os.getcwd() + "/saves"):
        print('trying to create folder')
        os.mkdir(os.getcwd() + "/saves/")
        os.mkdir(os.getcwd() + "/saves/diablo")
        os.mkdir(os.getcwd() + "/saves/PSP/")
        os.mkdir(os.getcwd() + "/saves/gba/")
        os.mkdir(os.getcwd() + "/saves/psx/")
    os.system('clear')
    print("EmulationStation/RetroArch/RetroPie Save File Sync has started.\n")
    print("System Cloud Save Manager v1.0.0")
    print("By Ray Hernandez")
    print("")
    print("Where are your most recent save files?")
    print("------------------------------------------")
    print("1.) Handheld Game System/RG350/RG351/Raspberry Pi")
    print("2.) Local game/emulation directories on this computer")
    print("3.) Sync save games from Google Drive")
    selection = int(input("Enter your selection: ").strip())
    if selection == "":
        print("You must enter a valid selection.")
        sys.exit(0)
    if (selection == 1 or selection == 2 or selection == 3):
        sync_saves(selection)
    else:
        print("Does not compute.")
    
def sync_saves(answer):

    # Check to see if any previous diablo saves exist.
    mac_diablo_dir = TEMP_SAVE_PATH + '/diablo'
    if os.path.exists(mac_diablo_dir):
        print('Removing old diablo save files from: %s...' % mac_diablo_dir);
        os.system('chmod +rw %s' % mac_diablo_dir)
        shutil.rmtree(mac_diablo_dir)
        os.mkdir(mac_diablo_dir)

    # TODO : Compare sizes and give warnings if smaller than whats getting replaced.
    if answer == 1:
        
        mac_diablo_dir = TEMP_SAVE_PATH + '/diablo'
        print("Copying Diablo save files from remote %s..." % REMOTE_DIABLO_PATH)
        os.system('sshpass -p "%s" rsync -a --include "*/" --include "*.sv" --exclude "*" %s@%s:%s "%s"' % (
            SSH_PASSWORD, SSH_USER, SSH_IP_ADDRESS, REMOTE_DIABLO_PATH, mac_diablo_dir
        ))
        # Copy updated save files to local diablo directory.
        print("Copying save files to local devilution directory...")
        os.system("cp -R '%s' '%s'" % (mac_diablo_dir + '/', LOCAL_DIABLO_PATH))

        # Copying all PSP save files.
        print("Copying PSP save files from device...")
        os.system('sshpass -p "%s" rsync -a %s@%s:%s "%s"' % (
            SSH_PASSWORD, SSH_USER, SSH_IP_ADDRESS, REMOTE_PSP_PATH, TEMP_SAVE_PATH + "/PSP/"
        ))

        # Copying all GBA save files.
        print("Copying GBA save files from device...")
        os.system('sshpass -p "%s" rsync -a --include "*/" --include "*.srm" --exclude "*" %s@%s:%s "%s"' % (
            SSH_PASSWORD, SSH_USER, SSH_IP_ADDRESS, REMOTE_GBA_PATH, TEMP_SAVE_PATH + "/gba/"
        ))

        # Copying all GBC save files.
        print("Copying GBC save files from device...")
        os.system('sshpass -p "%s" rsync -a --include "*/" --include "*.srm" --exclude "*" %s@%s:%s "%s"' % (
            SSH_PASSWORD, SSH_USER, SSH_IP_ADDRESS, REMOTE_GBC_PATH, TEMP_SAVE_PATH + "/gbc/"
        ))

        # Copying all GB save files.
        print("Copying GB save files from device...")
        os.system('sshpass -p "%s" rsync -a --include "*/" --include "*.srm" --exclude "*" %s@%s:%s "%s"' % (
            SSH_PASSWORD, SSH_USER, SSH_IP_ADDRESS, REMOTE_GBC_PATH, TEMP_SAVE_PATH + "/gb/"
        ))

        # Copying all GBA save files.
        print("Copying PSX save files from device...")
        # The -m switch should ignore empty directories.
        os.system('sshpass -p "%s" rsync -am --include "*/" --include "*.srm" --exclude "*" %s@%s:%s "%s"' % (
            SSH_PASSWORD, SSH_USER, SSH_IP_ADDRESS, REMOTE_PSX_PATH, TEMP_SAVE_PATH + "/psx/"
        ))

        if LOCAL_GOOGLE_DRIVE_PATH != "":
            print("Copying all save files to Google Drive...")
            os.system("cp -R '%s' '%s'" % (mac_diablo_dir + '/', LOCAL_GOOGLE_DRIVE_PATH + '/diablo'))
            os.system("cp -R '%s' '%s'" % (TEMP_SAVE_PATH + '/gba', LOCAL_GOOGLE_DRIVE_PATH + '/gba'))
            os.system("cp -R '%s' '%s'" % (TEMP_SAVE_PATH + '/psp', LOCAL_GOOGLE_DRIVE_PATH + '/psp'))
            os.system("cp -R '%s' '%s'" % (TEMP_SAVE_PATH + '/psx', LOCAL_GOOGLE_DRIVE_PATH + '/psx'))

    elif answer == 2:

        print("Removing old Diablo saves from Google Drive..." % LOCAL_GOOGLE_DRIVE_PATH)
        shutil.rmtree(LOCAL_GOOGLE_DRIVE_PATH + '/diablo')

        print("Copying Diablo save files from mac to %s..." % REMOTE_DIABLO_PATH)
        os.system('sshpass -p "%s" rsync -a "%s" %s@%s:%s --include "*/" --include "*.sv" --exclude "*"' % (
            SSH_PASSWORD, LOCAL_DIABLO_PATH, SSH_USER, SSH_IP_ADDRESS, REMOTE_DIABLO_PATH
        ))

        # Copy updated save files to local diablo directory.
        print("Copying save files to local devilution directory...")
        os.system("cp -R '%s' '%s'" % (mac_diablo_dir + '/', LOCAL_DIABLO_PATH))

        # Copy updated save files to Google Drive.
        if LOCAL_GOOGLE_DRIVE_PATH != "":
            print("Copying save files to Google Drive Sync directory...")
            os.system("cp -R '%s' '%s'" % (LOCAL_DIABLO_PATH + '/', LOCAL_GOOGLE_DRIVE_PATH + '/diablo'))

        print("Copying PSP save files from mac to %s..." % REMOTE_PSP_PATH)
        os.system('sshpass -p "%s" rsync -a "%s" %s@%s:%s' % (
            SSH_PASSWORD, TEMP_SAVE_PATH + "/PSP/", SSH_USER, SSH_IP_ADDRESS, REMOTE_PSP_PATH
        ))
    else:
        print("Command not implemented yet.")

if __name__ == "__main__":
    main()
