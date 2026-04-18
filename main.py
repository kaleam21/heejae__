import webview
import json
import os
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

DATA_FILE = BASE_DIR / 'budget_data.json'


def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'customCats' not in data: data['customCats'] = []
            if 'assetData' not in data: data['assetData'] = {'accounts':[],'debts':[],'investments':[]}
            if 'fixed' not in data: data['fixed'] = []
            return data
    return {'transactions':[], 'fixed':[], 'customCats':[], 'assetData':{'accounts':[],'debts':[],'investments':[]}}


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

    def save_custom(self, customCats, assetData):
        data = load_data()
        data['customCats'] = customCats
        data['assetData'] = assetData
        save_data(data)
        return {'ok': True}

    def add_transaction(self, tx):
        data = load_data()
        data['transactions'].append(tx)
        save_data(data)
        return {'ok': True}

    def update_transaction(self, idx, tx):
        data = load_data()
        if 0 <= idx < len(data['transactions']):
            data['transactions'][idx] = tx
            save_data(data)
        return {'ok': True}

    def delete_transaction(self, idx):
        data = load_data()
        if 0 <= idx < len(data['transactions']):
            data['transactions'].pop(idx)
            save_data(data)
        return {'ok': True}

    def clear_all(self):
        save_data({'transactions':[], 'fixed':[], 'customCats':[], 'assetData':{'accounts':[],'debts':[],'investments':[]}})
        return {'ok': True}


if __name__ == '__main__':
    api = Api()
    html_path = BASE_DIR / 'app.html'

    window = webview.create_window(
        title='내 가계부 v1.1.0',
        url=str(html_path),
        js_api=api,
        width=1280,
        height=820,
        min_size=(960, 640),
        background_color='#0f0f0f'
    )

    webview.start(debug=False)
