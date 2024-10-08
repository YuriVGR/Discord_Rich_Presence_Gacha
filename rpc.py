from pypresence import Presence
import psutil
import time
from dotenv import load_dotenv
import os
from threading import Thread
from pystray import Icon, Menu, MenuItem
from PIL import Image
import logging

script_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_dir, 'script.log')

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info('Script Started')
logging.info('##############################################')
load_dotenv()


nikke_client_id = os.getenv('NIKKE_CLIENT_ID')
bd_client_id = os.getenv('BD_CLIENT_ID')

logging.info("BrownDust Client ID:", bd_client_id)
logging.info("Nikke Client ID:", nikke_client_id)

if not nikke_client_id or not bd_client_id:
    raise ValueError("One or both Client IDs are not set. Please check your .env file.")

rpc_bd = Presence(bd_client_id)
rpc_nikke = Presence(nikke_client_id)

try:
    rpc_bd.connect()
    rpc_nikke.connect()
    print("Successfully connected to both RPCs")
except Exception as e:
    print(f"Failed to connect to Discord RPC: {e}")
    exit(1)

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

def game_running(name):
    for proc in psutil.process_iter(attrs=['name', 'exe']):
        try:
            if proc.info['name'].lower() == name.lower() and proc.info['exe'] and name.lower() in proc.info['exe'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return False

start_time = {}
running = False

def start_tracking():
    global running, start_time
    running = True
    while running:
        for game, info in games.items():
            if game_running(info['process_name']):
                if game not in start_time:
                    start_time[game] = time.time()
                    logging.info(f"{game} detected! Tracking Started.")
                try:
                    info['rpc'].update(start=start_time[game])
                    logging.info(f'Updated Discord Presence for {game}')
                except Exception as e:
                    logging.info(f'Failed to update Discord Presence for {game}: {e}')
            else:
                if game in start_time:
                    logging.info(f"{game} was closed. Clearing Discord Presence")
                    try:
                        info['rpc'].clear()
                    except Exception as e:
                        logging.info(f'Failed to clear Discord Presence for {game}: {e}')
                    del start_time[game]
        time.sleep(10)

def stop_tracking():
    global running
    running = False
    for game, info in games.items():
        info['rpc'].clear()
    logging.info("Tracking stopped.")

def run_tracking():
    tracking_thread = Thread(target=start_tracking)
    tracking_thread.daemon = True
    tracking_thread.start()

def setup_tray_icon():
    image = Image.open("icon.png")
    menu = Menu(
        MenuItem('Start Tracking', lambda: run_tracking(), enabled=lambda item: not globals().get('running', False)),
        MenuItem('Stop Tracking', lambda: stop_tracking(), enabled=lambda item: globals().get('running', False)),
        MenuItem('Quit', lambda: icon.stop())
    )
    icon = Icon("Discord RPC", image, menu=menu, title="Discord RPC Controller")
    icon.run()

if __name__ == '__main__':
    run_tracking()
    setup_tray_icon()