!include "MUI2.nsh"

!define TARGET_EDITION ""

Name "在这苍穹展翅 Gift Edition ${TARGET_EDITION} 汉化补丁"
OutFile "${TARGET_EDITION}_patch_installer.exe"
Unicode True
RequestExecutionLevel admin
InstallDir "$PROGRAMFILES32\PULLTOP\この大空に、翼をひろげて Gift Edition ${TARGET_EDITION}"
# SetCompress off
SetCompressor lzma
SetFont "Microsoft YaHei" 8
ShowInstDetails show

!define MUI_FINISHPAGE_NOAUTOCLOSE
!define MUI_ICON "hat.ico"
!define MUI_WELCOMEFINISHPAGE_BITMAP "${TARGET_EDITION}_side.bmp"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "license.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "SimpChinese"

Section "安装汉化补丁" SEC01
	DetailPrint "正在修补 JSON..."
	unicode::FileUnicode2Ansi "$INSTDIR\systeminfo.json" "$INSTDIR\systeminfo_tmp.json" "UTF-8"
	nsJSON::Set /file "$INSTDIR\systeminfo_tmp.json"
	nsJSON::Get `System` `UniqueGameID` /end
	Pop $R0
	StrCmp $R0 "__OOZORA_GIFT_${TARGET_EDITION}__" +3
	MessageBox MB_OK|MB_ICONSTOP "错误的游戏 ID，请检查安装目录是否正确。安装程序将现在终止。"
	Quit
	nsJSON::Set `System` `GameTitle` /value `"在这苍穹展翅 Gift Edition ${TARGET_EDITION}"`
	nsJSON::Set `GameFile` `script` `Archive` /value `"script.chs"`
	nsJSON::Set `GameFile` `image` `Archive` /value `"image.chs"`
	nsJSON::Serialize /format /file "$INSTDIR\systeminfo_tmp.json"
	unicode::FileAnsi2Unicode "$INSTDIR\systeminfo_tmp.json" "$INSTDIR\systeminfo.json" "UTF-8"
	SetDetailsPrint none
	Delete "$INSTDIR\systeminfo_tmp.json"
	SetOutPath "$INSTDIR"
	SetDetailsPrint both
	DetailPrint "正在释放文件..."
	SetOverwrite on
	File "${TARGET_EDITION}\script.chs"
	File "${TARGET_EDITION}\image.chs"
	File OozoraGEP.exe
SectionEnd
