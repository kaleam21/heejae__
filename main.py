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

CURRENT_VERSION = "1.2.2"
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
