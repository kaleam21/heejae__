# 💰 내 가계부 - 빌드 가이드

## 파일 구성
- `main.py` — 메인 파이썬 백엔드
- `app.html` — UI (HTML/CSS/JS)
- `budget.spec` — PyInstaller 빌드 설정
- `budget_data.json` — 데이터 저장 파일 (자동 생성)

---

## 개발 환경 실행

```bash
pip install pywebview
python main.py
```

---

## Windows exe 빌드

```bash
pip install pyinstaller pywebview
pyinstaller budget.spec
```

빌드 완료 후 `dist/가계부.exe` 생성

---

## Mac app 빌드

```bash
pip install pyinstaller pywebview
pyinstaller budget.spec
```

빌드 완료 후 `dist/가계부.app` 생성

---

## 기능
- 뱅크샐러드 엑셀 업로드 (중복 자동 제거)
- 거래내역 직접 추가/수정/삭제
- 고정지출 관리
- 대시보드 (카테고리 도넛차트, Top5)
- 소비 달력 (날짜 클릭 상세보기)
- 월별 수입/지출 막대 그래프
- 데이터 자동 저장 (budget_data.json)
