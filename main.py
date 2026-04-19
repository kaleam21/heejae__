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

CURRENT_VERSION = "1.2.0"
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
        req = urllib.request.Request(
            RELEASES_API,
            headers={"User-Agent": "budget-app", "Accept": "application/vnd.github+json"}
        )
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
