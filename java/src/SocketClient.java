import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;

// Connects to the Python server and reads one message per line.
// If Python is not running yet (or stops), it keeps trying every second.
public class SocketClient implements Runnable {

    public interface Listener {
        void onMessage(String line);
        void onStatus(boolean connected);
    }

    private final String host;
    private final int port;
    private final Listener listener;

    public SocketClient(String host, int port, Listener listener) {
        this.host = host;
        this.port = port;
        this.listener = listener;
    }

    @Override
    public void run() {
        while (true) {
            try (Socket socket = new Socket(host, port);
                 BufferedReader reader = new BufferedReader(
                         new InputStreamReader(socket.getInputStream(), "UTF-8"))) {
                listener.onStatus(true);
                String line;
                while ((line = reader.readLine()) != null) {
                    listener.onMessage(line);
                }
            } catch (IOException e) {
                // could not connect, or the connection was lost
            }
            listener.onStatus(false);
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                return;
            }
        }
    }
}
