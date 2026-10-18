// Original verification helper. Uses public certificate material and read-only
// Windows verification APIs. No certificate store writes or signing functions.
using System;
using System.ComponentModel;
using System.Runtime.InteropServices;

public static class ReadOnlySignatureChecks {
    [StructLayout(LayoutKind.Sequential)] struct Blob { public uint Size; public IntPtr Data; }
    [StructLayout(LayoutKind.Sequential)] struct Algorithm { public IntPtr Oid; public Blob Parameters; }
    [StructLayout(LayoutKind.Sequential)] struct Attribute { public IntPtr Oid; public Blob Value; }
    [StructLayout(LayoutKind.Sequential)] struct IndirectData { public Attribute Data; public Algorithm Algorithm; public Blob Digest; }
    [StructLayout(LayoutKind.Sequential)] struct Subject {
        public uint Size; public IntPtr Guid; public IntPtr File;
        public IntPtr FileName, DisplayName; public uint Reserved1, Version;
        public IntPtr Provider; public Algorithm Algorithm;
        public uint Flags, Encoding, Reserved2, CapiSettings, SecuritySettings, Index, Choice;
        public IntPtr Additional, Client;
    }
    [StructLayout(LayoutKind.Sequential)] struct FileInfo {
        public uint Size; public IntPtr Name, File, Subject;
    }
    [StructLayout(LayoutKind.Sequential)] struct TrustData {
        public uint Size; public IntPtr Policy, SipClient; public uint Ui, Revocation, Choice;
        public IntPtr File; public uint Action; public IntPtr State, Url;
        public uint Flags, UiContext; public IntPtr SignatureSettings;
    }
    [DllImport("crypt32.dll", CharSet=CharSet.Unicode, SetLastError=true)]
    static extern bool CryptSIPRetrieveSubjectGuid(string file, IntPtr handle, out Guid guid);
    [DllImport("crypt32.dll", CharSet=CharSet.Ansi, SetLastError=true)]
    static extern bool CryptDecodeObjectEx(uint encoding, string type, byte[] encoded, uint length,
        uint flags, IntPtr allocation, IntPtr decoded, ref uint size);
    [DllImport("crypt32.dll", SetLastError=true)]
    static extern bool CryptSIPVerifyIndirectData(ref Subject subject, IntPtr indirect);
    [DllImport("wintrust.dll", ExactSpelling=true, SetLastError=false)]
    static extern int WinVerifyTrust(IntPtr window, ref Guid action, ref TrustData data);

    public sealed class IntegrityResult {
        public string SubjectGuid, DigestAlgorithm, DigestHex;
        public bool FileDigestMatches, MutatedExpectedDigestRejected;
        public string FileDigestError, MutatedDigestError;
    }
    static string Hex(int error) { return "0x" + unchecked((uint)error).ToString("X8"); }
    static void Require(bool result, string operation) {
        if (!result) throw new Win32Exception(Marshal.GetLastWin32Error(), operation);
    }
    public static IntegrityResult VerifyPackageDigest(string path, byte[] signedIndirectContent) {
        Guid guid;
        Require(CryptSIPRetrieveSubjectGuid(path, IntPtr.Zero, out guid), "CryptSIPRetrieveSubjectGuid");
        uint size=0;
        Require(CryptDecodeObjectEx(0x10001, "1.3.6.1.4.1.311.2.1.4", signedIndirectContent,
            (uint)signedIndirectContent.Length, 0, IntPtr.Zero, IntPtr.Zero, ref size), "CryptDecodeObjectEx size");
        IntPtr buffer=Marshal.AllocHGlobal((int)size), guidPtr=Marshal.AllocHGlobal(Marshal.SizeOf<Guid>());
        IntPtr name=Marshal.StringToHGlobalUni(path);
        try {
            Require(CryptDecodeObjectEx(0x10001, "1.3.6.1.4.1.311.2.1.4", signedIndirectContent,
                (uint)signedIndirectContent.Length, 0, IntPtr.Zero, buffer, ref size), "CryptDecodeObjectEx data");
            Marshal.StructureToPtr(guid, guidPtr, false);
            var indirect=Marshal.PtrToStructure<IndirectData>(buffer);
            var subject=new Subject { Size=(uint)Marshal.SizeOf<Subject>(), Guid=guidPtr,
                File=new IntPtr(-1), FileName=name, Algorithm=indirect.Algorithm, Encoding=0x10001 };
            byte[] digest=new byte[indirect.Digest.Size];
            Marshal.Copy(indirect.Digest.Data, digest, 0, digest.Length);
            var result=new IntegrityResult { SubjectGuid=guid.ToString(),
                DigestAlgorithm=Marshal.PtrToStringAnsi(indirect.Algorithm.Oid),
                DigestHex=Convert.ToHexString(digest) };
            result.FileDigestMatches=CryptSIPVerifyIndirectData(ref subject, buffer);
            result.FileDigestError=result.FileDigestMatches ? null : Hex(Marshal.GetLastWin32Error());
            // Negative control changes only this allocated expected digest buffer.
            // The APPX and its embedded signature are never opened for writing.
            if (result.FileDigestMatches && digest.Length>0) {
                // APPX digest blob starts with APPX + AXPC identifiers. Change
                // a hash byte after those 8 bytes, preserving format headers.
                if (digest.Length<=8) throw new InvalidOperationException("Short APPX digest");
                byte original=Marshal.ReadByte(indirect.Digest.Data, 8);
                Marshal.WriteByte(indirect.Digest.Data, 8, (byte)(original ^ 1));
                bool badAccepted=CryptSIPVerifyIndirectData(ref subject, buffer);
                result.MutatedDigestError=badAccepted ? null : Hex(Marshal.GetLastWin32Error());
                result.MutatedExpectedDigestRejected=!badAccepted;
                Marshal.WriteByte(indirect.Digest.Data, 8, original);
            }
            return result;
        } finally { Marshal.FreeHGlobal(name); Marshal.FreeHGlobal(guidPtr); Marshal.FreeHGlobal(buffer); }
    }
    public static string VerifyNormalTrustCacheOnly(string path) {
        IntPtr name=Marshal.StringToHGlobalUni(path);
        IntPtr file=Marshal.AllocHGlobal(Marshal.SizeOf<FileInfo>());
        Guid action=new Guid("00AAC56B-CD44-11D0-8CC2-00C04FC295EE");
        var data=new TrustData { Size=(uint)Marshal.SizeOf<TrustData>(), Ui=2, Choice=1,
            File=file, Action=1, Flags=0x1000 | 0x10 };
        try {
            Marshal.StructureToPtr(new FileInfo { Size=(uint)Marshal.SizeOf<FileInfo>(), Name=name }, file, false);
            return Hex(WinVerifyTrust(new IntPtr(-1), ref action, ref data));
        } finally {
            data.Action=2; WinVerifyTrust(new IntPtr(-1), ref action, ref data);
            Marshal.FreeHGlobal(file); Marshal.FreeHGlobal(name);
        }
    }
}
