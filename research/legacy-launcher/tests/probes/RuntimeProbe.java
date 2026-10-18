import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.nio.file.FileSystem;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.LinkOption;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.security.MessageDigest;
import java.util.Arrays;
import java.util.Collections;
import java.util.Locale;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

/**
 * Original source-only Phase 6A diagnostic fixture. Run only in an approved
 * disposable guest or separately approved Xbox diagnostic package.
 * Does not exercise JNI, natives, graphics, audio, input, or authentication.
 */
public final class RuntimeProbe {
    private static final byte[] PAYLOAD =
        "LegacyForge Phase 6A owned synthetic fixture v1\n".getBytes(StandardCharsets.UTF_8);

    private final int javaMajor = javaMajor();
    private final String architecture = architecture();
    private String outcome = "NOT_EXECUTED";
    private String failure = "NONE";
    private Boolean rootValidated;
    private Boolean childCreated;
    private Boolean threadCompleted;
    private Boolean fileReadWriteHash;
    private Boolean renameReadback;
    private Boolean zipArchiveCreated;
    private Boolean zipfsReadback;
    private String payloadSha256;

    private RuntimeProbe() { }

    public static void main(String[] args) {
        RuntimeProbe result = new RuntimeProbe();
        try {
            result.run(args);
        } catch (Throwable problem) {
            result.outcome = "OBSERVED_FAILURE";
            result.failure = failureCode(problem);
        }
        System.out.println(result.toJson());
    }

    private void run(String[] args) throws Exception {
        if (args.length != 1) {
            rootValidated = Boolean.FALSE;
            outcome = "CONFIGURATION_REJECTED";
            failure = "ONE_EXISTING_APP_LOCAL_ROOT_REQUIRED";
            return;
        }

        Path supplied = Paths.get(args[0]).toAbsolutePath().normalize();
        if (!Files.isDirectory(supplied, LinkOption.NOFOLLOW_LINKS)) {
            rootValidated = Boolean.FALSE;
            outcome = "CONFIGURATION_REJECTED";
            failure = "ROOT_MUST_BE_EXISTING_NON_SYMLINK_DIRECTORY";
            return;
        }
        // The caller must authorize and own this root; Java cannot prove that
        // it is an approved guest/app-local location from a string argument.
        Path root = supplied.toRealPath();
        rootValidated = Boolean.TRUE;
        Path child = Files.createDirectory(root.resolve("runtime-probe-" + UUID.randomUUID()));
        childCreated = Boolean.TRUE;

        final AtomicBoolean completed = new AtomicBoolean(false);
        Thread worker = new Thread(new Runnable() {
            @Override public void run() { completed.set(true); }
        }, "phase6a-synthetic-worker");
        worker.setDaemon(true);
        worker.start();
        worker.join(5000L);
        threadCompleted = Boolean.valueOf(completed.get() && !worker.isAlive());
        if (!threadCompleted.booleanValue()) {
            outcome = "OBSERVED_FAILURE";
            failure = "THREAD_TIMEOUT";
            return;
        }

        Path original = child.resolve("payload-created-once.bin");
        try (OutputStream out = Files.newOutputStream(original,
                StandardOpenOption.CREATE_NEW, StandardOpenOption.WRITE)) {
            out.write(PAYLOAD);
        }
        byte[] expectedDigest = MessageDigest.getInstance("SHA-256").digest(PAYLOAD);
        byte[] reread = readBoundedRegular(original, PAYLOAD.length);
        byte[] actualDigest = MessageDigest.getInstance("SHA-256").digest(reread);
        fileReadWriteHash = Boolean.valueOf(Arrays.equals(PAYLOAD, reread)
            && MessageDigest.isEqual(expectedDigest, actualDigest));
        payloadSha256 = hex(actualDigest);
        if (!fileReadWriteHash.booleanValue()) {
            outcome = "OBSERVED_FAILURE";
            failure = "FILE_READBACK_MISMATCH";
            return;
        }

        Path renamed = child.resolve("payload-renamed-once.bin");
        // No REPLACE_EXISTING and no ATOMIC_MOVE (whose replacement semantics
        // can differ by provider). Existing destinations must cause failure.
        Files.move(original, renamed);
        renameReadback = Boolean.valueOf(!Files.exists(original, LinkOption.NOFOLLOW_LINKS)
            && Arrays.equals(PAYLOAD, readBoundedRegular(renamed, PAYLOAD.length)));
        if (!renameReadback.booleanValue()) {
            outcome = "OBSERVED_FAILURE";
            failure = "RENAME_READBACK_MISMATCH";
            return;
        }

        Path archive = child.resolve("probe-created-once.zip");
        // Create a new ZIP once, then read it with ZIPFS. No existing archive
        // is rewritten, and this fixture makes no delete/cleanup calls.
        try (OutputStream raw = Files.newOutputStream(archive,
                StandardOpenOption.CREATE_NEW, StandardOpenOption.WRITE);
             ZipOutputStream zip = new ZipOutputStream(raw)) {
            ZipEntry entry = new ZipEntry("synthetic-payload.bin");
            entry.setTime(0L);
            zip.putNextEntry(entry);
            zip.write(PAYLOAD);
            zip.closeEntry();
        }
        zipArchiveCreated = Boolean.TRUE;
        URI archiveUri = URI.create("jar:" + archive.toUri().toASCIIString());
        try (FileSystem zipfs = FileSystems.newFileSystem(archiveUri,
                Collections.<String, String>emptyMap())) {
            zipfsReadback = Boolean.valueOf(Arrays.equals(PAYLOAD,
                readBoundedRegular(zipfs.getPath("/synthetic-payload.bin"), PAYLOAD.length)));
        }
        outcome = zipfsReadback.booleanValue() ? "OBSERVED_OK" : "OBSERVED_FAILURE";
        failure = zipfsReadback.booleanValue() ? "NONE" : "ZIPFS_READBACK_MISMATCH";
    }

    private static byte[] readBoundedRegular(Path file, int maximum) throws IOException {
        if (!Files.isRegularFile(file, LinkOption.NOFOLLOW_LINKS)) {
            throw new IOException();
        }
        try (InputStream in = Files.newInputStream(file);
             ByteArrayOutputStream out = new ByteArrayOutputStream(maximum)) {
            for (int i = 0; i <= maximum; i++) {
                int value = in.read();
                if (value == -1) { return out.toByteArray(); }
                if (i == maximum) { throw new IOException(); }
                out.write(value);
            }
        }
        throw new IOException();
    }

    private static int javaMajor() {
        try {
            String version = System.getProperty("java.specification.version", "");
            String major = version.startsWith("1.") ? version.substring(2) : version;
            int value = Integer.parseInt(major);
            return value >= 1 && value <= 999 ? value : 0;
        } catch (Throwable ignored) { return 0; }
    }

    private static String architecture() {
        try {
            String value = System.getProperty("os.arch", "").toLowerCase(Locale.ROOT);
            if ("amd64".equals(value) || "x86_64".equals(value)) { return "x86_64"; }
            if ("aarch64".equals(value) || "arm64".equals(value)) { return "aarch64"; }
            if ("x86".equals(value) || "i386".equals(value) || "i686".equals(value)) { return "x86"; }
            return "OTHER";
        } catch (Throwable ignored) { return "UNKNOWN"; }
    }

    private static String failureCode(Throwable problem) {
        if (problem instanceof SecurityException) { return "SECURITY_REJECTED"; }
        if (problem instanceof java.nio.file.ProviderNotFoundException) { return "ZIPFS_PROVIDER_UNAVAILABLE"; }
        if (problem instanceof UnsupportedOperationException) { return "UNSUPPORTED_OPERATION"; }
        if (problem instanceof InterruptedException) {
            Thread.currentThread().interrupt();
            return "INTERRUPTED";
        }
        if (problem instanceof IOException) { return "IO_FAILURE"; }
        return "OTHER_FAILURE";
    }

    private static String hex(byte[] bytes) {
        char[] alphabet = "0123456789abcdef".toCharArray();
        StringBuilder out = new StringBuilder(bytes.length * 2);
        for (byte value : bytes) {
            out.append(alphabet[(value >>> 4) & 15]);
            out.append(alphabet[value & 15]);
        }
        return out.toString();
    }

    private String toJson() {
        return "{\"schema\":\"legacyforge-phase6a-synthetic-runtime-v1\","
            + "\"java_major\":" + javaMajor + ",\"architecture\":\"" + architecture + "\","
            + "\"outcome\":\"" + outcome + "\",\"failure_code\":\"" + failure + "\","
            + "\"root_validated\":" + rootValidated + ",\"fresh_child_created\":" + childCreated + ","
            + "\"thread_completed\":" + threadCompleted + ",\"file_read_write_sha256\":" + fileReadWriteHash + ","
            + "\"rename_readback\":" + renameReadback + ",\"zip_created_once\":" + zipArchiveCreated + ","
            + "\"zipfs_readback\":" + zipfsReadback + ",\"payload_sha256\":"
            + (payloadSha256 == null ? "null" : "\"" + payloadSha256 + "\"") + ","
            + "\"cleanup_attempted\":false,\"jni_tested\":false,\"native_loading_tested\":false,"
            + "\"graphics_tested\":false,\"input_tested\":false,\"audio_tested\":false}";
    }
}
