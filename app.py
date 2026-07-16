import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import minecraft_launcher_lib as mll
from PIL import Image
import requests
import subprocess
import os
import sys
import json

DEFAULT_CONFIG = {
    "color_theme": "green",
    "theme": "system",
    "bg_image_path": "default",
    "minecraft_directory": "default",
    "view_available_versions": "true",
    "in_version_list": ["release"],
    "lang": "ru"
}

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS #type: ignore
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = ctk.CTk()
app.geometry("600x500")

if not os.path.exists('config.json'):
    with open('config.json', "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=4)

config_data = DEFAULT_CONFIG

try:
    with open('config.json', "r", encoding="utf-8") as f:
        config_data = json.load(f)
except json.JSONDecodeError:
        config_data = DEFAULT_CONFIG
except Exception as e:
    if e != json.JSONDecodeError:
        warning = CTkMessagebox(app, title='An error occurred while reading settings', message=f'Error: {e}', icon='cancel')
ctk.set_appearance_mode(config_data['theme'])
ctk.set_default_color_theme(config_data['color_theme'])

lang_code = config_data['lang']
with open(resource_path(f'assets/locales/{lang_code}.json')) as f:
    lang_keys = json.load(f)

minecraft_directory = mll.utils.get_minecraft_directory().replace('.minecraft', '.sora2020slauncher')
if not os.path.exists(minecraft_directory):
    os.makedirs(minecraft_directory)
if config_data['minecraft_directory'] != 'default':
    minecraft_directory = config_data['minecraft_directory']

available_versions = []
try:
    if config_data['view_available_versions'] == 'true':
        available_versions = mll.utils.get_available_versions(minecraft_directory)
        selected = [v['id'] for v in available_versions if v['type'] in [ver for ver in config_data['in_version_list']]]
        available_versions = selected
    else:
        available_versions = mll.utils.get_installed_versions(minecraft_directory)
        selected = [v['id'] for v in available_versions]
        if selected == []:
            available_versions = [lang_keys['no_downloaded_versions']]
        else:
            available_versions = selected
except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.HTTPError):
    available_versions = mll.utils.get_installed_versions(minecraft_directory)
    selected = [v['id'] for v in available_versions]
    if selected == []:
        available_versions = [lang_keys['no_downloaded_versions']]
    else:
        available_versions = selected

button_container = ctk.CTkFrame(app, fg_color="transparent")
button_container.pack(anchor='w', side='bottom', padx=15, pady=30)

start = ctk.CTkButton(button_container, width=160, height=30, corner_radius=30, text=lang_keys['launch'])
start.pack(side='left')

folder_icon = ctk.CTkImage(light_image=Image.open(resource_path('assets/images/folder.png')), size=(20, 20))
folder = ctk.CTkButton(button_container, width=30, height=30, corner_radius=3, image=folder_icon, text="", command=lambda: (subprocess.Popen(f'explorer {minecraft_directory}')))
folder.pack(side='left', padx=10, pady=0)

version_box = ctk.CTkComboBox(app, 200, 35, values=available_versions)
version_box.pack(anchor='w', side='bottom', padx=15, pady=0)

username_field = ctk.CTkEntry(app, width=200, height=40, placeholder_text=lang_keys['username'])
username_field.pack(anchor='w', side='bottom', padx=15, pady=15)

bg_img = ctk.CTkImage(light_image=Image.open(resource_path('assets/images/light_theme.png')),
                        dark_image=Image.open(resource_path('assets/images/dark_theme.png')),
                        size=(290, 490))
bg_image = ctk.CTkLabel(app, text='', image=bg_img)
bg_image.place(x=305, y=5)

app.mainloop()