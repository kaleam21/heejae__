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

CURRENT_VERSION = "1.2.3"
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
