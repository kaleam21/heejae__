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

CURRENT_VERSION = "1.2.4"
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

        def bg_update_check():
            import time; time.sleep(5)  # exe 완전 로드 대기
            try:
                latest, notes, url = check_update()
                if latest:
                    safe_notes = (notes or "").replace("'", " ").replace('"', " ")[:100]
                    window.evaluate_js(f"showUpdateNotify('{latest}', '{safe_notes}')")
            except Exception as e:
                print("업데이트 체크 오류:", e)

        t = threading.Thread(target=bg_update_check)
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
