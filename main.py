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

CURRENT_VERSION = "1.2.6"
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
            elif name in ("가계부.exe", "budget.exe"):
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
