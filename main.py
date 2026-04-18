import webview
import json
import sys
import gzip
import base64
import tempfile
import os
import threading
import subprocess
import urllib.request
from pathlib import Path

CURRENT_VERSION = "1.1.0"
GITHUB_REPO = "kaleam21/heejae__"
VERSION_URL = "https://raw.githubusercontent.com/" + GITHUB_REPO + "/main/version.json"
DOWNLOAD_URL = "https://github.com/" + GITHUB_REPO + "/releases/latest/download/가계부.exe"

_HTML_DATA = "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"

def get_html_path():
    html_bytes = gzip.decompress(base64.b64decode(_HTML_DATA))
    tmp = tempfile.NamedTemporaryFile(mode="wb", suffix=".html", delete=False, prefix="budget_")
    tmp.write(html_bytes)
    tmp.close()
    return tmp.name

if getattr(sys, "frozen", False):
    DATA_DIR = Path(sys.executable).parent
    EXE_PATH = Path(sys.executable)
    UPDATER_PATH = DATA_DIR / "updater.exe"
else:
    DATA_DIR = Path(__file__).parent
    EXE_PATH = None
    UPDATER_PATH = DATA_DIR / "updater.py"

DATA_FILE = DATA_DIR / "budget_data.json"


def parse_version(v):
    try:
        return tuple(int(x) for x in v.strip().lstrip("v").split("."))
    except:
        return (0, 0, 0)


def check_update():
    try:
        req = urllib.request.Request(VERSION_URL, headers={"User-Agent": "budget-app"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
        latest = data.get("version", "0.0.0")
        notes = data.get("notes", "")
        if parse_version(latest) > parse_version(CURRENT_VERSION):
            return latest, notes
    except Exception as e:
        print("업데이트 확인 실패:", e)
    return None, None


def download_and_update(window, latest_version):
    try:
        window.evaluate_js("showUpdateProgress('다운로드 중...')")
        tmp_dir = tempfile.mkdtemp()
        tmp_exe = os.path.join(tmp_dir, "가계부_new.exe")

        downloaded = [0]
        def reporthook(count, block_size, total_size):
            if total_size > 0:
                pct = min(int(count * block_size * 100 / total_size), 100)
                downloaded[0] = pct
                window.evaluate_js("showUpdateProgress('다운로드 중... " + str(pct) + "%')")

        urllib.request.urlretrieve(DOWNLOAD_URL, tmp_exe, reporthook)
        window.evaluate_js("showUpdateProgress('설치 중...')")

        if EXE_PATH and UPDATER_PATH.exists():
            subprocess.Popen([str(UPDATER_PATH), tmp_exe, str(EXE_PATH)])
            window.evaluate_js("showUpdateProgress('재시작합니다...')")
            import time; time.sleep(1)
            window.destroy()
        else:
            window.evaluate_js("showUpdateProgress('다운로드 완료!')")
    except Exception as e:
        window.evaluate_js("showUpdateProgress('오류: " + str(e) + "')")


def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "customCats" not in data: data["customCats"] = []
            if "assetData" not in data: data["assetData"] = {"accounts":[],"debts":[],"investments":[]}
            if "fixed" not in data: data["fixed"] = []
            if "includeDebtInNet" not in data: data["includeDebtInNet"] = False
            return data
    return {
        "transactions": [], "fixed": [], "customCats": [],
        "assetData": {"accounts":[],"debts":[],"investments":[]},
        "includeDebtInNet": False
    }


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class Api:
    def __init__(self):
        self._window = None

    def set_window(self, window):
        self._window = window

    def get_data(self):
        return load_data()

    def get_version(self):
        return CURRENT_VERSION

    def check_update(self):
        latest, notes = check_update()
        if latest:
            return {"available": True, "version": latest, "notes": notes}
        return {"available": False}

    def do_update(self, version):
        if self._window:
            t = threading.Thread(target=download_and_update, args=(self._window, version))
            t.daemon = True
            t.start()
        return {"ok": True}

    def save_transactions(self, transactions):
        data = load_data(); data["transactions"] = transactions; save_data(data)
        return {"ok": True}

    def save_fixed(self, fixed):
        data = load_data(); data["fixed"] = fixed; save_data(data)
        return {"ok": True}

    def save_custom(self, customCats, assetData, includeDebtInNet=False):
        data = load_data()
        data["customCats"] = customCats
        data["assetData"] = assetData
        data["includeDebtInNet"] = includeDebtInNet
        save_data(data)
        return {"ok": True}

    def open_url(self, url):
        import webbrowser; webbrowser.open(url)
        return {"ok": True}

    def clear_all(self):
        save_data({
            "transactions": [], "fixed": [], "customCats": [],
            "assetData": {"accounts":[],"debts":[],"investments":[]},
            "includeDebtInNet": False
        })
        return {"ok": True}


def on_loaded(window, api):
    api.set_window(window)
    def bg_check():
        import time; time.sleep(2)
        latest, notes = check_update()
        if latest:
            safe_notes = (notes or "").replace("'", " ").replace('"', " ")
            window.evaluate_js("showUpdateNotify('" + latest + "', '" + safe_notes + "')")
    t = threading.Thread(target=bg_check)
    t.daemon = True
    t.start()


if __name__ == "__main__":
    api = Api()
    html_path = get_html_path()
    try:
        window = webview.create_window(
            title="내 가계부 v" + CURRENT_VERSION,
            url=html_path,
            js_api=api,
            width=1280,
            height=820,
            min_size=(960, 640),
            background_color="#0f0f0f"
        )
        webview.start(lambda w: on_loaded(w, api), window, debug=False)
    finally:
        try:
            os.unlink(html_path)
        except:
            pass
