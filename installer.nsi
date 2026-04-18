!define APP_NAME "My Budget"
!define APP_NAME_KR "내 가계부"
!define APP_VERSION "1.1.0"
!define APP_PUBLISHER "kaleam21"
!define OUTPUT_NAME "BudgetApp_Setup_v${APP_VERSION}.exe"

Name "${APP_NAME_KR}"
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

Section "Main" SecMain
  SetOutPath "$INSTDIR"
  File "dist\budget.exe"
  File "dist\updater.exe"
  Rename "$INSTDIR\budget.exe" "$INSTDIR\budget_app.exe"

  WriteRegStr HKLM "Software\${APP_NAME}" "Install_Dir" "$INSTDIR"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME_KR}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoRepair" 1
  WriteUninstaller "$INSTDIR\uninstall.exe"

  CreateShortcut "$DESKTOP\${APP_NAME_KR}.lnk" "$INSTDIR\budget_app.exe"
  CreateDirectory "$SMPROGRAMS\${APP_NAME_KR}"
  CreateShortcut "$SMPROGRAMS\${APP_NAME_KR}\${APP_NAME_KR}.lnk" "$INSTDIR\budget_app.exe"
  CreateShortcut "$SMPROGRAMS\${APP_NAME_KR}\Uninstall.lnk" "$INSTDIR\uninstall.exe"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\budget_app.exe"
  Delete "$INSTDIR\updater.exe"
  Delete "$INSTDIR\uninstall.exe"
  Delete "$INSTDIR\budget_data.json"
  RMDir "$INSTDIR"
  Delete "$DESKTOP\${APP_NAME_KR}.lnk"
  Delete "$SMPROGRAMS\${APP_NAME_KR}\${APP_NAME_KR}.lnk"
  Delete "$SMPROGRAMS\${APP_NAME_KR}\Uninstall.lnk"
  RMDir "$SMPROGRAMS\${APP_NAME_KR}"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
  DeleteRegKey HKLM "Software\${APP_NAME}"
SectionEnd
