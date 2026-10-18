#pragma once
#include "launcher_common.h"
namespace installedhighlight {
constexpr int kCount = 6;
inline UINT32 Color(int i) {
    static const UINT32 colors[kCount] = {0xF2C14E,0xF5A65B,0x45CBDC,0xAB8BFA,0xEC89BB,0x6CCF91};
    return colors[i >= 0 && i < kCount ? i : 0];
}
inline const wchar_t* Name(int i) {
    static const wchar_t* names[kCount] = {L"Amber",L"Light Orange",L"Cyan",L"Purple",L"Pink",L"Green"};
    return names[i >= 0 && i < kCount ? i : 0];
}
inline std::wstring Path() { return GetLocalStateDir() + L"\\settings\\installed-highlight.txt"; }
inline int& CachedIndex() { static int index = -1; return index; }
inline int CurrentIndex() {
    int& index = CachedIndex();
    if (index >= 0) return index;
    index = 0;
    std::wstring value;
    if (ReadTextFile(Path(), value)) {
        value = TrimWhitespace(StripNewlines(value));
        for (int i = 0; i < kCount; ++i) if (value == Name(i)) { index = i; break; }
    }
    return index;
}
inline UINT32 CurrentColor() { return Color(CurrentIndex()); }
inline bool SetIndex(int index) {
    if (index < 0 || index >= kCount) return false;
    if (!EnsureDirectoryTree(GetLocalStateDir() + L"\\settings") ||
        !WriteTextFile(Path(), std::wstring(Name(index)) + L"\n")) return false;
    CachedIndex() = index;
    return true;
}
}
