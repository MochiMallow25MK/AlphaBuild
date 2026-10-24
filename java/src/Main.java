import java.awt.KeyboardFocusManager;
import java.awt.event.KeyEvent;
import javax.swing.JFrame;
import javax.swing.SwingUtilities;

// AlphaBuild - Java side. Start the Python program first, then run this.
public class Main {

    private static final String HOST = "localhost";
    private static final int PORT = 5000;

    public static void main(String[] args) {
        SwingUtilities.invokeLater(Main::start);
    }

    private static void start() {
        final Game game = new Game();
        final GamePanel panel = new GamePanel(game);

        JFrame frame = new JFrame("AlphaBuild - Interactive Alphabet Word Builder");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(panel);
        frame.setSize(1000, 740);
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);

        // Keyboard shortcuts (a backup for the hand gestures).
        KeyboardFocusManager.getCurrentKeyboardFocusManager().addKeyEventDispatcher(e -> {
            if (e.getID() == KeyEvent.KEY_PRESSED) {
                if (e.getKeyCode() == KeyEvent.VK_ENTER) {
                    game.submitKey();
                } else if (e.getKeyCode() == KeyEvent.VK_N) {
                    game.nextKey();
                } else if (e.getKeyCode() == KeyEvent.VK_M) {
                    game.switchKey();
                }
                panel.repaint();
            }
            return false;
        });

        // Receive letters and gestures from Python.
        SocketClient client = new SocketClient(HOST, PORT, new SocketClient.Listener() {
            @Override
            public void onMessage(final String line) {
                SwingUtilities.invokeLater(() -> {
                    handleMessage(line, game);
                    panel.repaint();
                });
            }

            @Override
            public void onStatus(final boolean connected) {
                SwingUtilities.invokeLater(() -> {
                    panel.setConnected(connected);
                    if (!connected) {
                        game.setLetters("");
                    }
                    panel.repaint();
                });
            }
        });
        Thread thread = new Thread(client);
        thread.setDaemon(true);
        thread.start();
    }

    // Messages look like:  LETTERS CAT    or    GESTURE submit
    private static void handleMessage(String line, Game game) {
        String[] parts = line.split(" ", 2);
        String type = parts[0];
        String value = "";
        if (parts.length > 1) {
            value = parts[1].trim();
        }
        if (type.equals("LETTERS")) {
            game.setLetters(value);
        } else if (type.equals("GESTURE")) {
            game.handleGesture(value);
        }
    }
}
