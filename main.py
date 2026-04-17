import webview
import json
import os
import sys
from pathlib import Path

# 데이터 저장 경로
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

DATA_FILE = BASE_DIR / 'budget_data.json'


def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'transactions': [], 'fixed': [], 'settings': {}}


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
        save_data({'transactions': [], 'fixed': [], 'settings': {}})
        return {'ok': True}


if __name__ == '__main__':
    api = Api()
    html_path = BASE_DIR / 'app.html'

    window = webview.create_window(
        title='💰 내 가계부',
        url=str(html_path),
        js_api=api,
        width=1200,
        height=800,
        min_size=(900, 600),
        background_color='#0f0f0f'
    )

    webview.start(debug=False)
