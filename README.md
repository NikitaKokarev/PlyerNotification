# PlyerNotification

A simple demo application for Android, in which the Plyer logic for sending notifications has been restored.  
Changed getting activity depending on api_version >= 31.

<br>

## Plyer notification.py changes
versionchanged:: 1.5.0  
Fixed notifications. Changed getting activity depending on api_version >= 31.  
Functon _set_icons has been refactored.  
Added text style property for large message.

## How to use notification.py:
The app works 'as it is' with import from notification.py  
Or you can put this file to the Plyer directory:

    site-packages/plyer/platforms/android/notification.py

before build process (when buildozer downloads and sets up all the prerequisites for python-for-android, including the android SDK and NDK).

## How to use with Buildozer:

#### On Linux

- Use Buildozer [directly](https://github.com/kivy/buildozer#installing-buildozer-with-target-python-3-default) 
  or via [Docker](https://github.com/kivy/buildozer/blob/master/Dockerfile).

#### On Windows 10

- Install [Ubuntu WSL](https://ubuntu.com/wsl) and follow [Linux steps](#On-Linux).

#### Build automatically via GitHub Actions

- Use [ArtemSBulgakov/buildozer-action@v1](https://github.com/ArtemSBulgakov/buildozer-action)
  to build your packages automatically on push or pull request.
- See [full workflow example](https://github.com/ArtemSBulgakov/buildozer-action#full-workflow).


Do not forget to run buildozer android clean or remove .buildozer directory before building if version was updated (Buildozer doesn't update already downloaded packages).

<br>

## Solution based on:
1) https://github.com/nandanhere/kivyTimeTable/blob/main/replaceNotification.py  
2) https://github.com/orgs/kivy/discussions/20  
3) https://github.com/kivy/kivy/wiki/Background-Service-using-P4A-android.service  
4) https://stackoverflow.com/questions/46760144/kivy-and-android-notifications  

I tested this app with api_version >= 31 and api_version < 31. It works for Android 14.