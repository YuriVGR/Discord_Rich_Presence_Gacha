# Discord Rich Presence
A Python script that automatically updates your Discord Rich Presence based on the games you're playing. It detects when specific games are running on your computer and updates your Discord status accordingly.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Running at Startup](#running-at-startup)
- [Troubleshooting](#troubleshooting)
- [License](#license)
## Features
- **Automatic Game Detection:** Detects when specified games are running.
- **Discord Rich Presence Updates:** Updates your Discord status with the current game.
- **Time Tracking:** Shows how long you've been playing each game.
- **System Tray Icon:** Provides an easy way to control the script from the system tray.
- **Silent Operation:** Can run at startup without displaying any windows.
## Prerequisites
- **Python 3.6 or higher**
- **Discord Account**
- **Discord Developer Applications:** One for each game you want to track.
## Installation
#### 1. Clone the repo:
 ```
git clone https://github.com/yourusername/discord-game-presence-tracker.git
cd discord-game-presence-tracker
```
#### 2. Setup a VM (Optional)
```
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```
#### 3. Install the packages
```
pip install -r requirements.txt
```
Make sure your `requirements.txt` includes:
```
pypresence
psutil
pystray
Pillow
python-dotenv
```
## Configuration
#### 1. Create Discord Developer Applications
- Go to the Discord Developer Portal.
- Create a new application for each game.
- Note the Client ID for each application.
- Set up Rich Presence assets (images) if desired.

#### 2. Set Up Environment Variables
- Create a .env file in the root directory.
- Add your Discord application Client IDs:

```
NIKKE_CLIENT_ID=your_nikke_client_id
BD_CLIENT_ID=your_bd_client_id
```
  *Replace your_nikke_client_id and your_bd_client_id with your actual Client IDs.*

#### 3. Update the Script

In your script, ensure the games dictionary includes the games you want to track:
```
games = {
    'Brown Dust II': {
        'process_name': 'browndust ii.exe',
        'rpc': rpc_bd,
    },
    'NIKKE': {
        'process_name': 'nikke.exe',
        'rpc': rpc_nikke,
    }
}
```
Update process_name with the exact process name of the game executable.
## Usage

1. Update the `discord_rp.bat` file
```
@echo off
cd /d "F:\dev\discord_rc" # Change the directory to where your python project is. MAYBE I COULD MAKE IT BETTER
python rpc.py
```
Run the script
Either:
```
python your_script.py
```
or open the `vbscript.vbs` file

## Running at Startup
### Method 1: Using the startup folder with VBS Script
Create a shortcut for `vbscript.vbs` inside your startup folder
### Method 2: Task Scheduler
#### 1. Open Task Scheduler
Press Win + S, type "Task Scheduler", and open it
#### 2. Create a New Task
- Click "Create Task" in the Actions pane.
- Under the General tab:
  - Name your task (e.g., "Discord Game Presence Tracker").
  - Select "Run whether user is logged on or not."
  - Check "Run with highest privileges."
#### 3. Set the Trigger

Go to the Triggers tab.
Click "New..." and select "At startup".
Set the Action

Go to the Actions tab.
Click "New..." and select "Start a program."
Program/script: wscript.exe
Add arguments: "C:\path\to\run_script.vbs"
Replace with the path to your VBS script.
Finish Setup

Adjust conditions and settings as needed.
Save the task and enter your password if prompted.

