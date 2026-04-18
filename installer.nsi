!define APP_NAME "내 가계부"
!define APP_VERSION "1.1.0"
!define APP_PUBLISHER "kaleam21"
!define OUTPUT_NAME "BudgetApp_Setup_v${APP_VERSION}.exe"

Name "${APP_NAME}"
OutFile "${OUTPUT_NAME}"
InstallDir "$PROGRAMFILES64\${APP_NAME}"
InstallDirRegKey HKLM "Software\${APP_NAME}" "Install_Dir"
RequestExecutionLevel admin
Unicode True

!include "MUI2.nsh"
!define MUI_ABORTWARNING
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "Korean"

Section "메인 프로그램" SecMain
  SetOutPath "$INSTDIR"
  File "dist\budget.exe"
  File "dist\updater.exe"
  Rename "$INSTDIR\budget.exe" "$INSTDIR\가계부.exe"

  WriteRegStr HKLM "Software\${APP_NAME}" "Install_Dir" "$INSTDIR"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoRepair" 1
  WriteUninstaller "$INSTDIR\uninstall.exe"

  CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\가계부.exe"
  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\가계부.exe"
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\제거.lnk" "$INSTDIR\uninstall.exe"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\가계부.exe"
  Delete "$INSTDIR\updater.exe"
  Delete "$INSTDIR\uninstall.exe"
  Delete "$INSTDIR\budget_data.json"
  RMDir "$INSTDIR"
  Delete "$DESKTOP\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\제거.lnk"
  RMDir "$SMPROGRAMS\${APP_NAME}"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
  DeleteRegKey HKLM "Software\${APP_NAME}"
SectionEnd
