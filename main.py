import webview
import json
import sys
from pathlib import Path

# 실행 환경에 따라 경로 설정
if getattr(sys, 'frozen', False):
    # PyInstaller로 빌드된 exe 실행 시
    BASE_DIR = Path(sys._MEIPASS)
    DATA_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR

DATA_FILE = DATA_DIR / 'budget_data.json'
HTML_FILE = BASE_DIR / 'app.html'


def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'customCats' not in data: data['customCats'] = []
            if 'assetData' not in data: data['assetData'] = {'accounts':[],'debts':[],'investments':[]}
            if 'fixed' not in data: data['fixed'] = []
            if 'includeDebtInNet' not in data: data['includeDebtInNet'] = False
            return data
    return {
        'transactions': [],
        'fixed': [],
        'customCats': [],
        'assetData': {'accounts':[],'debts':[],'investments':[]},
        'includeDebtInNet': False
    }


def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class Api:
    def get_data(self):
        return load_data()

    def save_transactions(self, transactions):
        data = load_data()
        data['transactions'] = transactions
        save_data(data)
        return {'ok': True}

    def save_fixed(self, fixed):
        data = load_data()
        data['fixed'] = fixed
        save_data(data)
        return {'ok': True}

    def save_custom(self, customCats, assetData, includeDebtInNet=False):
        data = load_data()
        data['customCats'] = customCats
        data['assetData'] = assetData
        data['includeDebtInNet'] = includeDebtInNet
        save_data(data)
        return {'ok': True}

    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)
        return {'ok': True}

    def clear_all(self):
        save_data({
            'transactions': [],
            'fixed': [],
            'customCats': [],
            'assetData': {'accounts':[],'debts':[],'investments':[]},
            'includeDebtInNet': False
        })
        return {'ok': True}


if __name__ == '__main__':
    api = Api()

    window = webview.create_window(
        title='내 가계부 v1.1.0',
        url=str(HTML_FILE),
        js_api=api,
        width=1280,
        height=820,
        min_size=(960, 640),
        background_color='#0f0f0f'
    )

    webview.start(debug=False)
