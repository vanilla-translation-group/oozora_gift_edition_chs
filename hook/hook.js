Interceptor.attach(Module.getExportByName("gdi32.dll", "CreateFontIndirectW"), {
    onEnter(args) {
        let logfontPtr = args[0];
        let lfFaceNamePtr = logfontPtr.add(28);
        let currentFont = lfFaceNamePtr.readUtf16String(32);
        let targetFont = "Microsoft YaHei";
        // console.log(currentFont);
        if (currentFont == "游ゴシック") {
            lfFaceNamePtr.writeUtf16String(targetFont);
        }
    }
});

const menuTranslation = {"終了": "结束", "ウィンドウ": "窗口", "ヘルプ": "帮助"};

const GetMenuItemCount = new NativeFunction(
    Module.getExportByName("user32.dll", "GetMenuItemCount"),
    "int", ["pointer"]
);
const GetMenuStringW = new NativeFunction(
    Module.getExportByName("user32.dll", "GetMenuStringW"),
    "int", ["pointer", "uint32", "pointer", "int", "uint32"]
);
const ModifyMenuW = new NativeFunction(
    Module.getExportByName("user32.dll", "ModifyMenuW"),
    "bool", ["pointer", "uint32", "uint32", "uint32", "pointer"]
);

Interceptor.attach(Module.getExportByName("user32.dll", "LoadMenuW"), {
    onLeave(retval) {
        if (retval.isNull()) {
            return;
        }
        let itemCount = GetMenuItemCount(retval);
        // console.log(itemCount);
        for (let i = 0; i < itemCount; i++) {
            let buffer = Memory.alloc(512);
            let stringLength = GetMenuStringW(retval, i, buffer, 256, 0x00000400);
            // console.log(stringLength);
            if (stringLength > 0) {
                let originalText = Memory.readUtf16String(buffer);
                // console.log(originalText);
                if (originalText in menuTranslation) {
                    let newText = menuTranslation[originalText];
                    let newBuffer = Memory.allocUtf16String(newText);
                    ModifyMenuW(retval, i, 0x00000400, 0, newBuffer);
                }
            }
        }
    }
});
