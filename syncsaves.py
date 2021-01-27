#
# Sync all my save games with all my devices, including Google Drive.
# Starting with Diablo.
# By Ray Hernandez
#
#
#  Changelog
# ------------------
#  - Added PSP support.
#  - Added GBA/GBC/GB support.
#  - Added playstation and diablo support. Fixed issue with virtual Google Drive.

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

import os 
import time
import sys
import shutil
import sys
    
# Credentials for linux handheld / raspberry pi / rg350 / rg351
SSH_IP_ADDRESS = ""
SSH_USER = ""
SSH_PASSWORD = ""

# Save file paths
REMOTE_PSP_PATH = ""
REMOTE_GBA_PATH = ""
REMOTE_GBC_PATH = ""
REMOTE_GB_PATH = ""
REMOTE_NES_PATH = ""
REMOTE_SNES_PATH = ""
REMOTE_PSX_PATH= ""
REMOTE_DIABLO_PATH = ""
REMOTE_MEGADRIVE_PATH = ""

LOCAL_DIABLO_PATH = config['local']['DIABLO_SAVE_PATH']
LOCAL_PSP_PATH = config['local']['PSP_SAVE_PATH']

# Make sure that you install the google drive client on your mac/pc.
try:
    LOCAL_GOOGLE_DRIVE_PATH = config['local']['GOOGLE_DRIVE_PATH']
except:
    LOCAL_GOOGLE_DRIVE_PATH = ""
    
TEMP_SAVE_PATH = os.getcwd() + "/saves"

def main():
    global RSYNC_DIABLO_PATH,RSYNC_PSX_PATH,RSYNC_GBA_PATH, MAC_DIABLO_PATH, GOOGLE_DRIVE_SAVE_DIR
    global TEMP_SAVE_PATH, REMOTE_PSP_PATH, REMOTE_GBA_PATH, REMOTE_GBC_PATH, REMOTE_GB_PATH
    global REMOTE_NES_PATH, REMOTE_SNES_PATH, REMOTE_PSX_PATH, REMOTE_DIABLO_PATH, REMOTE_MEGADRIVE_PATH
    global SSH_IP_ADDRESS, SSH_USER, SSH_PASSWORD
    os.system('clear')
    print("EmulationStation/RetroArch/RetroPie Save File Sync has started.")
    print("v1.0.0")
    print("------------------------------------------")
    print("1.) Backup save files from remote device (SSH).")
    print("2.) Backup local save files.")
    print("")
    try:
        selection = int(input("Enter your selection: ").strip())
    except:
        selection = ""
    print("")
    if selection == "":
        print("You must enter a valid selection.")
        sys.exit(0)
    if (selection == 1 or selection == 2):
        if os.path.exists(TEMP_SAVE_PATH):
            shutil.rmtree(TEMP_SAVE_PATH)
        os.mkdir(TEMP_SAVE_PATH)
        device_list = config.sections()
        device_list.remove('local')
        device = input("Enter the device to backup saves from %s: " % device_list).strip()
        if device not in device_list:
            print("You must enter a device section from your config.ini.")
            sys.exit(0)
        SSH_IP_ADDRESS = config[device]['DEVICE_IP']
        SSH_USER = config[device]['DEVICE_USER']
        SSH_PASSWORD = config[device]['DEVICE_PASS']
        try:
            REMOTE_PSP_PATH = config[device]['PSP_SAVE_PATH']
        except:
            REMOTE_PSP_PATH = ""
        try:
            REMOTE_GBA_PATH = config[device]['GBA_SAVE_PATH']
        except:
            REMOTE_GBA_PATH = ""
        try:
            REMOTE_GBC_PATH = config[device]['GBC_SAVE_PATH']
        except:
            REMOTE_GBC_PATH = ""
        try:
            REMOTE_GB_PATH = config[device]['GB_SAVE_PATH']
        except:
            REMOTE_GB_PATH = ""
        try:
            REMOTE_NES_PATH = config[device]['NES_SAVE_PATH']
        except:
            REMOTE_NES_PATH = ""
        try:
            REMOTE_SNES_PATH = config[device]['SNES_SAVE_PATH']
        except:
            REMOTE_SNES_PATH = ""
        try:
            REMOTE_PSX_PATH= config[device]['PSX_SAVE_PATH']
        except:
            REMOTE_PSX_PATH = ""
        try:
            REMOTE_DIABLO_PATH = config[device]['DIABLO_SAVE_PATH']
        except:
            REMOTE_DIABLO_PATH = ""
        try:
            REMOTE_MEGADRIVE_PATH = config[device]['MEGADRIVE_SAVE_PATH']
        except:
            REMOTE_MEGADRIVE_PATH = ""
        sync_saves(selection)
    else:
        print("Does not compute.")

def send_rsync(source, destination):
    global SSH_USER, SSH_PASSWORD, SSH_IP_ADDRESS
    os.system('sshpass -p "%s" rsync -a %s@%s:%s "%s"' % (
        SSH_PASSWORD, SSH_USER, SSH_IP_ADDRESS, source, destination
    ))

def send_rsync2(source, destination, extension):
    global SSH_USER, SSH_PASSWORD, SSH_IP_ADDRESS
    os.system('sshpass -p "%s" rsync -a --include "*.%s" --exclude "*" %s@%s:%s "%s"' % (
        SSH_PASSWORD, extension, SSH_USER, SSH_IP_ADDRESS, source, destination
    ))

def send_rsync3(source, destination, extension):
    global SSH_USER, SSH_PASSWORD, SSH_IP_ADDRESS
    os.system('sshpass -p "%s" rsync -a --include "*/" --include "*.%s" --exclude "*" %s@%s:%s "%s"' % (
        SSH_PASSWORD, extension, SSH_USER, SSH_IP_ADDRESS, source, destination
    ))
    
def sync_saves(answer):

    save_file_extensions = ['srm', 'sav']

    # TODO : Compare sizes and give warnings if smaller than whats getting replaced.
    # User has chosen to get all of the save games from the device, and udpate the cloud.
    if answer == 1:
        # Copy all of diablo/devilutionX files. Also save the save files for local play.
        if REMOTE_DIABLO_PATH != "":
            print("Copying Diablo save files from remote %s..." % REMOTE_DIABLO_PATH)
            send_rsync2(REMOTE_DIABLO_PATH, TEMP_SAVE_PATH + "/diablo", 'sv')
            print("Copying save files to local devilution directory...")
            os.system("rsync -a %s %s" % (TEMP_SAVE_PATH + "/diablo/", LOCAL_DIABLO_PATH))

        # Copying all PSP save files.
        if REMOTE_PSP_PATH != "":
            print("Copying PSP save files from device...")
            send_rsync(REMOTE_PSP_PATH, TEMP_SAVE_PATH + "/psp")
            print("Copying PSP saves to local computer...")
            os.system("rsync -a %s %s" % (TEMP_SAVE_PATH + "/psp/SAVEDATA/", LOCAL_PSP_PATH))

        # Copying all GBA save files.
        if REMOTE_GBA_PATH != "":
            print("Copying GBA save files from device...")
            for ext in save_file_extensions:
                send_rsync2(REMOTE_GBA_PATH, TEMP_SAVE_PATH + "/gba/", ext)

        # Copying all GBC save files.
        if REMOTE_GBC_PATH != "":
            print("Copying GBC save files from device...")
            for ext in save_file_extensions:
                send_rsync2(REMOTE_GBC_PATH, TEMP_SAVE_PATH + "/gbc/", ext)

        # Copying all GB save files.
        if REMOTE_GB_PATH != "":
            print("Copying GB save files from device...")
            for ext in save_file_extensions:
                send_rsync2(REMOTE_GB_PATH, TEMP_SAVE_PATH + "/gb/", ext)

        if REMOTE_NES_PATH != "":
            print("Copying NES save files from device...")
            for ext in save_file_extensions:
                send_rsync2(REMOTE_NES_PATH, TEMP_SAVE_PATH + '/nes/', ext)

        if REMOTE_MEGADRIVE_PATH != "":
            print("Copying genesis/megadrive save files from device...")
            for ext in save_file_extensions:
                send_rsync2(REMOTE_MEGADRIVE_PATH, TEMP_SAVE_PATH + '/megadrive/', ext)

        if REMOTE_SNES_PATH != "":
            print("Copying SNES save files from device...")
            for ext in save_file_extensions:
                send_rsync2(REMOTE_SNES_PATH, TEMP_SAVE_PATH + "/snes/", ext)

        # Copying all GBA save files.
        if REMOTE_PSX_PATH != "":
            print("Copying PSX save files from device...")
            # We use send rsync3 here incase discs/saves are in separate folders.
            for ext in save_file_extensions:
                send_rsync3(REMOTE_PSX_PATH, TEMP_SAVE_PATH + "/psx/", ext)

        # If user has set a local google drive path sync all save files.
        if LOCAL_GOOGLE_DRIVE_PATH != "":
            # Tries to make root save game directory every time.
            try:
                os.mkdir(LOCAL_GOOGLE_DRIVE_PATH)
            except:
                pass

            print("Copying all save files to Google Drive...")
            os.system("rsync -a %s %s" % (TEMP_SAVE_PATH + '/diablo/', LOCAL_GOOGLE_DRIVE_PATH + '/diablo'))
            os.system("rsync -a %s %s" % (TEMP_SAVE_PATH + '/gba/', LOCAL_GOOGLE_DRIVE_PATH + '/gba'))
            os.system("rsync -a %s %s" % (TEMP_SAVE_PATH + '/gbc/', LOCAL_GOOGLE_DRIVE_PATH + '/gbc'))
            os.system("rsync -a %s %s" % (TEMP_SAVE_PATH + '/gb/', LOCAL_GOOGLE_DRIVE_PATH + '/gb'))
            os.system("rsync -a %s %s" % (TEMP_SAVE_PATH + '/psp/', LOCAL_GOOGLE_DRIVE_PATH + '/psp'))
            os.system("rsync -a %s %s" % (TEMP_SAVE_PATH + '/psx/', LOCAL_GOOGLE_DRIVE_PATH + '/psx'))

    elif answer == 2:

        print("Retrieving local diablo save files...")
        os.system('rsync -a %s/*.sv %s' % (LOCAL_DIABLO_PATH, TEMP_SAVE_PATH + '/diablo'))

        if os.path.exists(TEMP_SAVE_PATH + "/psp"):
            print("Removing old temporary psp save files from: %s..." % TEMP_SAVE_PATH + "/psp")
            shutil.rmtree(TEMP_SAVE_PATH + "/psp")
            os.mkdir(TEMP_SAVE_PATH + "/psp")

        print("Preparing PSP saves to send...")
        os.system("rsync -a %s %s" % (LOCAL_PSP_PATH, TEMP_SAVE_PATH + "/psp/SAVEDATA/"))

        if LOCAL_GOOGLE_DRIVE_PATH != "":
            # Tries to make root save game directory every time.
            try:
                os.mkdir(LOCAL_GOOGLE_DRIVE_PATH)
            except:
                pass

            print("Copying all save files to Google Drive...")
            os.system("rsync -a %s %s" % (TEMP_SAVE_PATH + '/diablo/', LOCAL_GOOGLE_DRIVE_PATH + "/diablo"))
            os.system("rsync -a %s %s" % (TEMP_SAVE_PATH + '/psp/', LOCAL_GOOGLE_DRIVE_PATH + "/psp"))


if __name__ == "__main__":
    main()
