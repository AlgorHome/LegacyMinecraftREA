// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 Runtime Diagnostics contributors.
// Original synthetic fixture. No launcher, game, network, file or account code.
package diagnostic;

public final class JniSmoke {
    private JniSmoke() { }

    private static native int nativeFold(int value);

    // Only fixed-width numbers cross the JNI boundary. No raw property is logged.
    public static long[] run() {
        int major = Runtime.version().feature();
        String architecture = System.getProperty("os.arch", "");
        int architectureCode = ("amd64".equals(architecture) || "x86_64".equals(architecture)) ? 1
            : ("aarch64".equals(architecture) || "arm64".equals(architecture)) ? 2
            : ("x86".equals(architecture) || "i386".equals(architecture)) ? 3 : 0;
        int checksum = 0x13579bdf;
        for (int i = 0; i < 4096; i++) {
            checksum = Integer.rotateLeft(checksum ^ (i * 0x045d9f3b), 5) + 0x9e3779b9;
        }
        return new long[] {
            major,
            architectureCode,
            Integer.toUnsignedLong(checksum),
            Integer.toUnsignedLong(nativeFold(0x10203040))
        };
    }

    public static int[] roundTrip(int[] values) {
        int[] output = values.clone();
        for (int i = 0; i < output.length; i++) {
            output[i] ^= 0x5a5a5a5a;
        }
        return output;
    }

    public static void controlledException() {
        throw new IllegalStateException("SYNTHETIC_DIAGNOSTIC");
    }
}
