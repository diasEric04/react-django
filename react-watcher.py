import sys
import os
from pathlib import Path
import json
import time
from threading import Thread, Lock
from shutil import copy, rmtree
import re


ROOT_DIR = Path(__file__).parent.resolve()
JSON_CONFIG_FILENAME = 'rw-config.json'
JSON_CONFIG_PATH = ROOT_DIR / JSON_CONFIG_FILENAME

CONFIG_REACT_KEY = 'react_dir'
CONFIG_DJANGO_KEY = 'django_dir'

CSS_URL_REGEXP = re.compile(
    r'(url\(\/static\/media\/(.+)\))', flags=re.I
)


def build_reactapp(walk_dir, root):
    print(
        ' 🔵 changes detected in react project '
        f'"/{os.path.basename(walk_dir)}", building...'
    )
    system = sys.platform

    cmd = f'cd {root} ; npm run build'

    if system == 'win32':
        cmd = f'cd {root} & npm run build'

    os.system(cmd)
    print(' 🟢 build completed')


def copy_staticfiles(build_dir, django_path):
    print(' 🔵 copying static files...')
    STATIC_FILES_REACT = build_dir / 'static'
    app_name = os.path.basename(django_path)
    STATIC_FILES_DJANGO = django_path / 'static' / app_name
    for root, dirs, files in os.walk(STATIC_FILES_REACT):
        for dir in dirs:
            new_dir = os.path.join(
                root.replace(
                    str(STATIC_FILES_REACT),
                    str(STATIC_FILES_DJANGO)
                ),
                dir
            )
            os.makedirs(new_dir, exist_ok=True)
            print(f' 🟡 copying dir "{dir}/"...')

        for file in files:
            file_path_original = os.path.join(root, file)
            file_path_django = os.path.join(
                root.replace(
                    str(STATIC_FILES_REACT),
                    str(STATIC_FILES_DJANGO)
                ),
                file
            )
            copy(file_path_original, file_path_django)
            print(f' 🟡 copying file "{file}"...')
            _, extesion = os.path.splitext(file)
            extensions = ['.css', '.scss', '.sass']
            if extesion in extensions:
                with open(file_path_django, 'r', encoding='utf8') as stylefile:
                    style_text = stylefile.read()
                    new_style_text = CSS_URL_REGEXP.sub(
                        r'url(/media/react-media/\2)', style_text
                    )
                with open(file_path_django, 'w', encoding='utf8') as stylefile:
                    print(f' 🟡 adjusting url in file "{file}"...')
                    stylefile.write(new_style_text)
    print(' 🔴 removing media dir from static files (django app...)')
    django_static_media_path = os.path.join(STATIC_FILES_DJANGO, 'media')
    if os.path.exists(django_static_media_path):
        rmtree(django_static_media_path)
    print(' 🟢 all static files are copied to django app')


def copy_mediafiles(build_dir, django_path):
    STATIC_FILES_REACT = build_dir / 'static'
    MEDIA_FILES_REACT = STATIC_FILES_REACT / 'media'
    DJANGO_ROOT = Path(os.path.dirname(django_path))
    MEDIA_FILES_DJANGO = DJANGO_ROOT / 'media' / 'react-media'

    os.makedirs(MEDIA_FILES_DJANGO)

    print(' 🔵 copying media files...')
    for root, dirs, files in os.walk(MEDIA_FILES_REACT):
        for dir in dirs:
            new_dir = os.path.join(
                root.replace(
                    str(MEDIA_FILES_REACT),
                    str(MEDIA_FILES_DJANGO)
                ),
                dir
            )
            os.makedirs(new_dir, exist_ok=True)
            print(f' 🟡 copying dir "{dir}/"...')

        for file in files:
            file_path_original = os.path.join(root, file)
            file_path_django = os.path.join(
                root.replace(
                    str(MEDIA_FILES_REACT),
                    str(MEDIA_FILES_DJANGO)
                ),
                file
            )
            copy(file_path_original, file_path_django)
            print(f' 🟡 copying file "{file}"...')
    for item in os.listdir(build_dir):
        if os.path.isfile(item):
            _, extension = os.path.splitext(item)
            if not extension == '.html':
                item_path = os.path.join(build_dir, item)
                new_item_path = os.path.join(MEDIA_FILES_DJANGO, item)
                copy(item_path, new_item_path)
                print(f' 🟡 copying file "{item}"...')
    print(' 🟢 all static files are copied to django app')


def copy_htmlfiles(build_dir, django_path):
    app_name = os.path.basename(django_path)
    for item in os.listdir(build_dir):
        item_path = os.path.join(build_dir, item)
        if os.path.isfile(item_path):
            _, extension = os.path.splitext(item)
            if extension == '.html':
                outdir_app_name = input(
                    "which dir name to copy all html files in django app? "
                )
                print(
                    f' 🔵 copying HTMLs to {outdir_app_name}...'
                )
                django_pages_path = os.path.join(
                    django_path, 'templates', app_name,
                    outdir_app_name
                )
                os.makedirs(django_pages_path, exist_ok=True)
                new_html_path = os.path.join(
                    django_pages_path, item
                )
                copy(item_path, new_html_path)
                print(f' 🟡 copying html "{item}"...')
    print(' 🟢 all html files are copied to django app')


class Watcher:
    def __init__(self):
        self.lock = Lock()

    def watch(self, django_app_path, react_project_path):
        PUBLIC_DIR = react_project_path / 'public'
        SRC_DIR_REACT = react_project_path / 'src'
        BUILD_DIR_REACT = react_project_path / 'build'
        while True:
            self.walk_dir(SRC_DIR_REACT, django_app_path, BUILD_DIR_REACT)
            self.walk_dir(PUBLIC_DIR, django_app_path, BUILD_DIR_REACT)

    def walk_dir(self, walk_dir, django_path, build_dir):
        for root, dirs, files in os.walk(walk_dir):
            for file in files:
                seconds_limit = 10

                file_path_original = os.path.join(root, file)
                timestamp_now = time.time()
                timestamp_file = os.path.getmtime(file_path_original)

                seconds_diff = timestamp_now - timestamp_file

                if seconds_diff < seconds_limit:
                    self.lock.acquire()
                    build_reactapp(walk_dir, root)
                    copy_staticfiles(build_dir, django_path)
                    copy_mediafiles(build_dir, django_path)
                    copy_htmlfiles(build_dir, django_path)
                    print(' 🟢 all proccess is completed!')
                    print(' 🔵 github: diasEric04\n\n')
                    self.lock.release()


def watch_react_project(django_app_path, react_project_path):

    print(
        f' 🟢 starting whatching {os.path.basename(react_project_path)} '
        f'to {os.path.basename(django_app_path)}'
    )

    watcher = Watcher()
    t = Thread(
        target=watcher.watch,
        args=(
            django_app_path,
            react_project_path
        ),
        daemon=True
    )
    t.start()

    # trava o progama enquanto nao houver um keyboardinterrupt
    try:
        while t.is_alive():
            pass
    except KeyboardInterrupt:
        pass


def create_config_file():
    with open(JSON_CONFIG_PATH, 'w+', encoding="utf8") as jsonfile:
        react_dir = input('what is the name of REACT dir? ')
        FULL_REACT_PATH = ROOT_DIR / react_dir
        if not os.path.exists(FULL_REACT_PATH):
            print(' 🔴 REACT path dot not exists')
            return

        django_dir = input('what is the name of DJANGO dir? ')
        FULL_DJANGO_DIR = ROOT_DIR / django_dir
        if not os.path.exists(FULL_DJANGO_DIR):
            print(' 🔴 DJANGO path dot not exists')
            return

        obj = {
            CONFIG_REACT_KEY: str(FULL_REACT_PATH),
            CONFIG_DJANGO_KEY: str(FULL_DJANGO_DIR)
        }
        json.dump(obj, jsonfile, ensure_ascii=False, indent=2)
        return True


def app(system_args: list):
    if not JSON_CONFIG_PATH.exists():
        created = create_config_file()
        if not created:
            return

    with open(JSON_CONFIG_PATH, 'r+', encoding='utf8') as jsonfile:
        obj: dict = json.load(jsonfile)

    if CONFIG_REACT_KEY not in obj.keys():
        JSON_CONFIG_PATH.unlink()
        created = create_config_file()
        if not created:
            return

    # tudo ok
    if len(system_args) < 3:
        print(
            ' 🔴 require 2 args, 1st=django app name and '
            '2nd=react project name, example: '
            'python script.py app_name project_name'
        )
        return
    django_app_name = system_args[1]
    react_project_name = system_args[2]

    FULL_REACT_DIR = Path(obj[CONFIG_REACT_KEY])
    FULL_DJANGO_DIR = Path(obj[CONFIG_DJANGO_KEY])

    REACT_PROJECT_PATH = FULL_REACT_DIR / react_project_name
    DJANGO_APP_PATH = FULL_DJANGO_DIR / django_app_name

    if not REACT_PROJECT_PATH.exists():
        print(' 🔴 react project file do not exists')
        return

    if not DJANGO_APP_PATH.exists():
        print(' 🔴 django app file do not exists')
        return

    watch_react_project(DJANGO_APP_PATH, REACT_PROJECT_PATH)


if __name__ == '__main__':
    app(sys.argv)
