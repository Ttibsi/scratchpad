import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Arrays;
import java.nio.file.Path;
import java.nio.file.Paths;

public class nob {
    private static ArrayList<String> listFilesForFolder(File folder) {
        ArrayList<String> files = new ArrayList<>();

        for (final File fileEntry : folder.listFiles()) {

            if (fileEntry.getName().equals("nob.java")) { continue; }
            if (fileEntry.getName().endsWith(".class")) { continue; }

            if (fileEntry.isDirectory()) {
                files.addAll(listFilesForFolder(fileEntry));
            } else {
                files.add(fileEntry.getName());
            }
        }

        return files;
    }

    private static void runCmd(ArrayList<String> cmd) throws Exception {
        System.out.println("[INFO] Running cmd: " + cmd);
        ProcessBuilder pb = new ProcessBuilder(cmd);
        pb.inheritIO();
        pb.start();
    }

    private static String getCurrentDir() {
        String userDirectory = Paths.get("")
            .toAbsolutePath()
            .toString();
        String[] parts = userDirectory.split("/");
        return parts[parts.length - 1];
    }

    public static void main(String... argv) throws Exception {
        boolean run = false;
        boolean clean = false;
        for (String flag : argv) {
            if (flag.equals("-run")) { run = true; }
            if (flag.equals("-clean")) { clean = true; }
        }

        if (clean) {
            ArrayList<String> exec = new ArrayList<>();
            exec.add("sh");
            exec.add("-c");
            exec.add("rm *.class");
            runCmd(exec);
            return;
        }

        File folder = new File(".");
        ArrayList<String> files = new ArrayList<>();
        files.add("javac");
        files.addAll(listFilesForFolder(folder));

        runCmd(files);

        if (run) {
            ArrayList<String> exec = new ArrayList<>();
            exec.add("java");
            exec.add("-cp");
            exec.add("..");
            exec.add(getCurrentDir() + ".first");
            runCmd(exec);
        }
    }
}
