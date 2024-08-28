# 在这苍穹展翅 GIFT EDITION 汉化补丁

在 Releases 中下载对应版本的安装包，安装完成后打开目录下的 OozoraGEP.exe 即可使用。

## STAFF

scientificworld：初翻、修图~~修了一半跑路了~~、程序？

Misaka13514：校对润色、测试

特别感谢：

- [GARbro](https://github.com/morkt/GARbro) 全体贡献者
- [VN-Patching-Tools](https://github.com/kevlu123/VN-Patching-Tools/tree/master/IMHHW%20Gift%20Edition%20Kotori%20Text%20Patching%20Tools) 开发者 kevlu123
- [SilkyArcTool](https://github.com/TesterTesterov/SilkyArcTool) 开发者 TesterTesterov

## 一些感言

### scientificworld

几年前就想自己参与汉化一部作品，今天这个梦想终于实现了 ~~（虽然只是个小短篇）~~。第一次搞汉化，不足之处还请各位批评指正，也祝各位玩的开心。

感谢 @Misaka13514 能抽出时间帮我校对，也感谢制作了各种解封包工具的前辈们，在你们的帮助下才有了这个补丁。

题外话：本作使用的引擎 `eomaiaゲームシステム` 我以前从来没见过，不知道有没有大佬碰到过其他用这个引擎的游戏？

### Misaka13514

这是我第一次参与汉化，如翻译仍有不妥之处还请大家多多包涵。

感谢 @scientificworld 购入此作品并愿意分享，和 @scientificworld 一起工作也是很开心的事情（才不是因为作品很短工作量很少呢）。

扬羽的泳装真是太可爱啦（偷偷抱走 @scientificworld 的挂画(x)），愿假期中与扬羽贴贴玩耍的愉快时光能永远存在于你我心中。

## 构建流程（备忘）

1. 把原文本封包和汉化文本放在同一个目录下，运行 `python3 patch_text.py script.arc script.chs names.json SC*_*.json`（あげはVer 需要把 SC01\_00 和 SC01\_02 拷贝过来）
2. 将图像从封包里提取出来，把 sys 目录里的两张图覆盖进去，用 SilkyArcTool 重新打包（选择 `Pack archive (no compression)`，如果失败先在原处创建一个空文件）
3. 创建一个 `icon.rc` 文件，在里面写入 `IDI_ICON1 ICON "补丁图标.ico"`，执行 `rc icon.rc` 生成 `icon.res`
4. 从 [Frida Releases](https://github.com/frida/frida/releases) 下载 `frida-core-devkit-windows-x86`，解压后把文件放在和 `OozoraGEP.c` 同目录下，执行 `cl /MT OozoraGEP.c icon.res` 编译出补丁（要显示调试窗口把参数改成 `/MTd`）
5. 修改 installer.nsi 第三行的目标版本，选择 `Kotori` / `Ageha`
6. 把图片封包里的 Event CG 较小版本提取出来，截一个 820 * 1570 的部分另存为 `side.png`，执行 `magick convert -resize 410x785 side.png BMP2:side.bmp`
7. 把所有文件都放在正确的位置后，使用 `makensis /INPUTCHARSET UTF8 installer.nsi` 构建出最终的安装包。（需要安装 [nsJSON](https://nsis.sourceforge.io/NsJSON_plug-in) 和 [Unicode](https://nsis.sourceforge.io/Unicode_plug-in) 插件）

## 版权信息

原始文本、图像等版权归 PULLTOP 所有。

VN-Patching-Tools 相关组件版权归 Kevin Lu 所有。

其余部分以 Unlicense 许可证授权，属于公有领域。
