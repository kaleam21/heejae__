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
import urllib.error
import hashlib
import platform
import uuid
import concurrent.futures
from pathlib import Path

CURRENT_VERSION = "1.2.1"
GITHUB_REPO = "kaleam21/heejae__"
RELEASES_API = "https://api.github.com/repos/" + GITHUB_REPO + "/releases/latest"

# ─────────────────────────────────────────────────────────────
# 🔐 라이선스 설정
# ─────────────────────────────────────────────────────────────
GIST_ID = "63f641fed064d6bc7788f0246ed32a1f"
_OBF_TOKEN = "VnVGR2gwMU9yNDFEcVVqYVZOVzVVOWFzempFb2Y2NEEzU2Z4X3BoZw=="
# ─────────────────────────────────────────────────────────────

_HTML_DATA = "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"


def get_html_path():
    html_bytes = gzip.decompress(base64.b64decode(_HTML_DATA))
    tmp = tempfile.NamedTemporaryFile(mode="wb", suffix=".html", delete=False, prefix="budget_")
    tmp.write(html_bytes)
    tmp.close()
    return tmp.name


if getattr(sys, "frozen", False):
    EXE_PATH = Path(sys.executable)
    EXE_DIR = EXE_PATH.parent
    UPDATER_PATH = EXE_DIR / "updater.exe"
    DATA_DIR = Path(os.environ.get("APPDATA", str(Path.home()))) / "MyBudget"
    DATA_DIR.mkdir(parents=True, exist_ok=True)
else:
    EXE_PATH = None
    EXE_DIR = Path(__file__).parent
    UPDATER_PATH = EXE_DIR / "updater.py"
    DATA_DIR = Path(__file__).parent

DATA_FILE = DATA_DIR / "budget_data.json"
LICENSE_FILE = DATA_DIR / "license.json"


# ═══════════════════════════════════════════════
# 🔐 라이선스 모듈
# ═══════════════════════════════════════════════

def _get_token():
    try:
        return base64.b64decode(_OBF_TOKEN.encode()).decode()[::-1]
    except Exception:
        return ""


def get_hwid():
    components = []
    system = platform.system()
    mac = uuid.getnode()
    if mac != 0:
        components.append(f"mac:{mac}")
    if system == "Windows":
        try:
            out = subprocess.check_output("vol C:", shell=True, stderr=subprocess.DEVNULL).decode(errors="ignore")
            serial = "".join(c for c in out if c.isalnum())[-10:]
            components.append(f"vol:{serial}")
        except Exception:
            pass
        try:
            out = subprocess.check_output("wmic cpu get ProcessorId /value", shell=True, stderr=subprocess.DEVNULL).decode(errors="ignore")
            cpu = "".join(c for c in out if c.isalnum())[:16]
            components.append(f"cpu:{cpu}")
        except Exception:
            pass
    elif system == "Darwin":
        # 방법 1: ioreg로 Hardware UUID (앱 샌드박스에서도 동작)
        try:
            out = subprocess.check_output(
                ["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"],
                stderr=subprocess.DEVNULL
            ).decode(errors="ignore")
            for line in out.splitlines():
                if "IOPlatformUUID" in line:
                    val = line.split('"')[-2].strip()
                    if val:
                        components.append(f"ioreg_uuid:{val}")
                        break
        except Exception:
            pass
        # 방법 2: system_profiler fallback
        if not any("ioreg_uuid" in c for c in components):
            try:
                out = subprocess.check_output(
                    ["system_profiler", "SPHardwareDataType"],
                    stderr=subprocess.DEVNULL
                ).decode(errors="ignore")
                for line in out.splitlines():
                    if "Hardware UUID" in line:
                        val = line.split(":")[-1].strip()
                        if val:
                            components.append(f"mac_uuid:{val}")
                            break
                for line in out.splitlines():
                    if "Serial Number" in line:
                        val = line.split(":")[-1].strip()
                        if val:
                            components.append(f"mac_serial:{val}")
                            break
            except Exception:
                pass
    elif system == "Linux":
        try:
            with open("/etc/machine-id") as f:
                components.append(f"mid:{f.read().strip()}")
        except Exception:
            pass
    if not components:
        components.append(f"platform:{platform.node()}:{platform.machine()}")
    raw = "|".join(sorted(components))
    return hashlib.sha256(raw.encode()).hexdigest()[:32].upper()


def _gist_request(method="GET", data=None):
    url = f"https://api.github.com/gists/{GIST_ID}"
    token = _get_token()
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "budget-app-license",
        "Authorization": f"token {token}"
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    # macOS PyInstaller 앱에서 SSL 인증서 문제 해결
    import ssl
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            return json.loads(r.read().decode())
    except ssl.SSLError:
        # SSL 실패 시 certifi 시도
        try:
            import certifi
            ctx = ssl.create_default_context(cafile=certifi.where())
            with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
                return json.loads(r.read().decode())
        except Exception:
            # 마지막 수단: 인증서 검증 비활성화 (GitHub API라 안전)
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
                return json.loads(r.read().decode())


def _read_db():
    resp = _gist_request("GET")
    content = resp["files"]["keys.json"]["content"]
    return json.loads(content)


def _write_db(db):
    _gist_request("PATCH", {
        "files": {"keys.json": {"content": json.dumps(db, ensure_ascii=False, indent=2)}}
    })


def _local_sig(key, hwid):
    return hashlib.sha256(f"{key}:{hwid}:budget".encode()).hexdigest()


def _load_local_license():
    if LICENSE_FILE.exists():
        try:
            with open(LICENSE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return None


def _save_local_license(key, hwid):
    payload = {"key": key, "hwid": hwid, "sig": _local_sig(key, hwid)}
    with open(LICENSE_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def verify_license():
    hwid = get_hwid()
    local = _load_local_license()
    if local is None:
        return False, "no_license"
    if local.get("sig") != _local_sig(local.get("key", ""), local.get("hwid", "")):
        return False, "tampered"
    if local.get("hwid") != hwid:
        return False, "hwid_mismatch"
    key = local.get("key", "")
    try:
        db = _read_db()
        keys = db.get("keys", {})
        if key not in keys:
            return False, "key_deleted"
        entry = keys[key]
        if entry.get("revoked"):
            return False, "revoked"
        if entry.get("hwid") != hwid:
            return False, "hwid_changed"
        return True, "ok"
    except Exception:
        return True, "ok_offline"


def register_key(key):
    key = key.strip().upper()
    hwid = get_hwid()
    try:
        db = _read_db()
    except Exception as e:
        return "net_error", f"서버 연결 실패: {e}"
    keys = db.get("keys", {})
    if key not in keys:
        return "not_found", "유효하지 않은 키입니다."
    entry = keys[key]
    if entry.get("revoked"):
        return "revoked", "취소된 키입니다. 관리자에게 문의하세요."
    registered_hwid = entry.get("hwid")
    if registered_hwid is None:
        from datetime import datetime
        entry["hwid"] = hwid
        entry["activated_at"] = datetime.now().isoformat()
        try:
            _write_db(db)
        except Exception as e:
            return "net_error", f"등록 실패: {e}"
        _save_local_license(key, hwid)
        return "ok", "등록 완료!"
    elif registered_hwid == hwid:
        _save_local_license(key, hwid)
        return "ok", "인증됨."
    else:
        return "duplicate", "이 키는 다른 PC에 이미 등록되어 있습니다.\nPC를 변경하려면 관리자에게 문의하세요."


# ═══════════════════════════════════════════════
# 라이선스 UI HTML
# ═══════════════════════════════════════════════

LICENSE_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>내 가계부 - 라이선스 등록</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #0f0f0f;
    color: #e0e0e0;
    font-family: 'Malgun Gothic', sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
    user-select: none;
  }
  .card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 16px;
    padding: 48px 56px;
    width: 480px;
    text-align: center;
  }
  .icon { font-size: 52px; margin-bottom: 20px; }
  h1 { font-size: 22px; font-weight: 700; margin-bottom: 8px; color: #fff; }
  .sub { font-size: 13px; color: #888; margin-bottom: 36px; line-height: 1.6; }
  input {
    width: 100%;
    background: #111;
    border: 1.5px solid #333;
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 18px;
    color: #fff;
    text-align: center;
    letter-spacing: 3px;
    font-family: 'Courier New', monospace;
    transition: border-color 0.2s;
    outline: none;
    margin-bottom: 16px;
  }
  input:focus { border-color: #4ade80; }
  input.error { border-color: #f87171; }
  input.success { border-color: #4ade80; }
  button {
    width: 100%;
    background: #4ade80;
    color: #0f0f0f;
    border: none;
    border-radius: 10px;
    padding: 14px;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.2s;
  }
  button:hover { background: #22c55e; }
  button:disabled { background: #333; color: #666; cursor: not-allowed; }
  .msg { margin-top: 16px; font-size: 13px; min-height: 20px; line-height: 1.5; }
  .msg.err { color: #f87171; }
  .msg.ok { color: #4ade80; }
  .msg.info { color: #60a5fa; }
  .hint { font-size: 11px; color: #555; margin-top: 28px; }
</style>
</head>
<body>
<div class="card">
  <div class="icon">🔐</div>
  <h1>내 가계부 라이선스 등록</h1>
  <p class="sub">이 앱을 사용하려면 라이선스 키가 필요합니다.<br>관리자로부터 받은 키를 입력하세요.</p>
  <input type="text" id="key" placeholder="XXXX-XXXX-XXXX-XXXX"
    maxlength="19" autocomplete="off" spellcheck="false" />
  <button id="btn" onclick="submitKey()">키 등록하기</button>
  <div class="msg" id="msg"></div>
  <p class="hint">v""" + CURRENT_VERSION + """ | 1 PC에만 등록 가능합니다</p>
</div>
<script>
  const input = document.getElementById('key');
  const btn = document.getElementById('btn');
  const msg = document.getElementById('msg');

  input.addEventListener('input', function() {
    let v = this.value.replace(/[^A-Za-z0-9]/g, '').toUpperCase().slice(0, 16);
    let parts = v.match(/.{1,4}/g) || [];
    this.value = parts.join('-');
    input.className = '';
    msg.textContent = '';
    msg.className = 'msg';
  });

  input.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') submitKey();
  });

  function setMsg(text, type) {
    msg.textContent = text;
    msg.className = 'msg ' + type;
  }

  function submitKey() {
    const k = input.value.trim();
    if (k.length < 19) {
      setMsg('키를 올바르게 입력하세요 (XXXX-XXXX-XXXX-XXXX)', 'err');
      input.className = 'error';
      return;
    }
    btn.disabled = true;
    btn.textContent = '확인 중...';
    setMsg('서버에 연결 중입니다...', 'info');
    pywebview.api.submit_license_key(k);
  }

  function onLicenseResult(ok, message) {
    if (ok) {
      setMsg('✅ ' + message, 'ok');
      input.className = 'success';
      btn.textContent = '등록 완료!';
      setTimeout(function() { pywebview.api.license_accepted(); }, 1200);
    } else {
      setMsg('❌ ' + message, 'err');
      input.className = 'error';
      btn.disabled = false;
      btn.textContent = '키 등록하기';
    }
  }
</script>
</body>
</html>"""


# ═══════════════════════════════════════════════
# 기존 유틸 함수들
# ═══════════════════════════════════════════════

def parse_version(v):
    try:
        return tuple(int(x) for x in v.strip().lstrip("v").split("."))
    except:
        return (0, 0, 0)


def check_update():
    try:
        token = _get_token()
        headers = {"User-Agent": "budget-app", "Accept": "application/vnd.github+json"}
        if token:
            headers["Authorization"] = f"token {token}"
        req = urllib.request.Request(RELEASES_API, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
        latest = data.get("tag_name", "0.0.0").lstrip("v")
        notes = data.get("body", "")
        download_url = ""
        installer_url = ""
        for asset in data.get("assets", []):
            name = asset.get("name", "")
            if name == "updater.exe":
                continue
            if "installer" in name.lower() or "setup" in name.lower():
                installer_url = asset.get("browser_download_url", "")
            elif name == "가계부.exe":
                download_url = asset.get("browser_download_url", "")
        if parse_version(latest) > parse_version(CURRENT_VERSION):
            return latest, notes, download_url or installer_url
    except Exception as e:
        print("업데이트 확인 실패:", e)
    return None, None, None


def download_and_update(window, latest_version, download_url):
    try:
        if not download_url:
            window.evaluate_js("showUpdateProgress('다운로드 URL을 찾을 수 없어요.')")
            return
        window.evaluate_js("showUpdateProgress('다운로드 중...')")
        tmp_dir = tempfile.mkdtemp()
        is_installer = "installer" in download_url.lower() or "setup" in download_url.lower()
        tmp_exe = os.path.join(tmp_dir, "update.exe")

        def reporthook(count, block_size, total_size):
            if total_size > 0:
                pct = min(int(count * block_size * 100 / total_size), 100)
                window.evaluate_js(f"showUpdateProgress('다운로드 중... {pct}%')")

        urllib.request.urlretrieve(download_url, tmp_exe, reporthook)
        window.evaluate_js("showUpdateProgress('설치 중...')")
        if is_installer:
            subprocess.Popen([tmp_exe])
            window.evaluate_js("showUpdateProgress('설치 파일을 실행했어요. 설치 후 재시작하세요.')")
            import time; time.sleep(2)
            window.destroy()
        elif EXE_PATH and UPDATER_PATH.exists():
            subprocess.Popen([str(UPDATER_PATH), tmp_exe, str(EXE_PATH)])
            window.evaluate_js("showUpdateProgress('재시작합니다...')")
            import time; time.sleep(1)
            window.destroy()
        else:
            window.evaluate_js("showUpdateProgress('다운로드 완료! 수동으로 교체해주세요.')")
    except Exception as e:
        window.evaluate_js("showUpdateProgress('오류가 발생했어요.')")
        print("업데이트 오류:", e)


def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "customCats" not in data: data["customCats"] = []
            if "assetData" not in data: data["assetData"] = {"accounts": [], "debts": [], "investments": []}
            if "fixed" not in data: data["fixed"] = []
            if "includeDebtInNet" not in data: data["includeDebtInNet"] = False
            if "dutchPayList" not in data: data["dutchPayList"] = []
            return data
    return {
        "transactions": [], "fixed": [], "customCats": [],
        "assetData": {"accounts": [], "debts": [], "investments": [], "manualAssets": []},
        "includeDebtInNet": False,
        "dutchPayList": []
    }


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════
# API 클래스
# ═══════════════════════════════════════════════

class LicenseApi:
    def __init__(self, on_accept):
        self._on_accept = on_accept
        self._window = None

    def set_window(self, w):
        self._window = w

    def submit_license_key(self, key):
        """백그라운드 스레드에서 검증 후 JS 콜백으로 결과 전달"""
        def _do_verify():
            try:
                result, msg = register_key(key)
            except Exception as e:
                result, msg = "net_error", str(e)
            if self._window:
                ok = "true" if result == "ok" else "false"
                safe_msg = msg.replace("'", " ").replace('"', " ").replace("\n", " ")
                self._window.evaluate_js(
                    f"onLicenseResult({ok}, '{safe_msg}')"
                )
        t = threading.Thread(target=_do_verify, daemon=True)
        t.start()
        return {"ok": True, "started": True}

    def license_accepted(self):
        if self._window:
            self._window.destroy()
        self._on_accept()


class Api:
    def __init__(self):
        self._window = None
        self._update_url = None

    def set_window(self, window):
        self._window = window

    def get_data(self):
        return load_data()

    def get_version(self):
        return CURRENT_VERSION

    def check_update(self):
        latest, notes, url = check_update()
        if latest:
            self._update_url = url
            return {"available": True, "version": latest, "notes": notes}
        return {"available": False}

    def do_update(self, version):
        if self._window and self._update_url:
            t = threading.Thread(target=download_and_update, args=(self._window, version, self._update_url))
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

    def save_dutch(self, dutchPayList):
        data = load_data()
        data["dutchPayList"] = dutchPayList
        save_data(data)
        return {"ok": True}

    def open_url(self, url):
        import webbrowser; webbrowser.open(url)
        return {"ok": True}

    def clear_all(self):
        save_data({
            "transactions": [], "fixed": [], "customCats": [],
            "assetData": {"accounts": [], "debts": [], "investments": []},
            "includeDebtInNet": False
        })
        return {"ok": True}


# ═══════════════════════════════════════════════
# 실행
# ═══════════════════════════════════════════════

def run_main_app():
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

        def on_loaded(w):
            api.set_window(w)
            def bg_check():
                import time; time.sleep(2)
                latest, notes, url = check_update()
                if latest:
                    safe_notes = (notes or "").replace("'", " ").replace('"', " ")[:100]
                    w.evaluate_js(f"showUpdateNotify('{latest}', '{safe_notes}')")
            t = threading.Thread(target=bg_check)
            t.daemon = True
            t.start()

        webview.start(on_loaded, window, debug=False)
    finally:
        try:
            os.unlink(html_path)
        except:
            pass


def run_license_window():
    accepted = threading.Event()

    def on_accept():
        accepted.set()

    lic_api = LicenseApi(on_accept=on_accept)
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, prefix="license_", encoding="utf-8")
    tmp.write(LICENSE_HTML)
    tmp.close()

    try:
        win = webview.create_window(
            title="내 가계부 - 라이선스 등록",
            url=tmp.name,
            js_api=lic_api,
            width=540,
            height=440,
            resizable=False,
            background_color="#0f0f0f"
        )
        webview.start(lambda w: lic_api.set_window(w), win, debug=False)
    finally:
        try:
            os.unlink(tmp.name)
        except:
            pass

    if accepted.is_set():
        run_main_app()


if __name__ == "__main__":
    valid, status = verify_license()
    if valid:
        run_main_app()
    else:
        reason_map = {
            "no_license":    "라이선스 없음",
            "tampered":      "license.json 변조 감지",
            "hwid_mismatch": "HWID 불일치",
            "key_deleted":   "키 삭제됨",
            "revoked":       "키 취소됨",
            "hwid_changed":  "HWID 변경됨",
        }
        print(reason_map.get(status, f"인증 실패: {status}"))
        run_license_window()
