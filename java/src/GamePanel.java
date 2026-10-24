import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Polygon;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.HashMap;
import java.util.Map;
import javax.imageio.ImageIO;
import javax.swing.JPanel;

// Draws the game screen. The screen is designed for 1000 x 700 and scaled
// to fit the window.
public class GamePanel extends JPanel {

    private static final int W = 1000;
    private static final int H = 700;

    private static final Color BACKGROUND = new Color(255, 248, 225);
    private static final Color HEADER = new Color(70, 110, 200);
    private static final Color FOOTER = new Color(40, 50, 80);
    private static final Color GOOD = new Color(40, 150, 70);
    private static final Color BAD = new Color(225, 120, 20);
    private static final Color GOLD = new Color(250, 200, 40);
    private static final Color[] LETTER_COLORS = {
        new Color(220, 60, 60), new Color(240, 140, 30), new Color(60, 160, 80),
        new Color(60, 120, 220), new Color(150, 80, 200), new Color(220, 70, 150)
    };

    private final Game game;
    private final Map<String, BufferedImage> images = new HashMap<String, BufferedImage>();
    private final File imageFolder;
    private boolean connected = false;

    public GamePanel(Game game) {
        this.game = game;
        setBackground(BACKGROUND);
        if (new File("images").isDirectory()) {
            imageFolder = new File("images");
        } else if (new File("java/images").isDirectory()) {
            imageFolder = new File("java/images");
        } else {
            imageFolder = new File("images");
            System.out.println("Warning: the images folder was not found. "
                    + "Run the game from the java folder.");
        }
    }

    public void setConnected(boolean connected) {
        this.connected = connected;
    }

    @Override
    protected void paintComponent(Graphics g0) {
        super.paintComponent(g0);
        Graphics2D g = (Graphics2D) g0.create();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
        g.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BILINEAR);

        double scale = Math.min(getWidth() / (double) W, getHeight() / (double) H);
        g.translate((getWidth() - W * scale) / 2, (getHeight() - H * scale) / 2);
        g.scale(scale, scale);
        g.setClip(0, 0, W, H);

        drawHeader(g);
        if (game.getMode() == Game.LETTER_MODE) {
            drawLetterMode(g);
        } else if (game.getMode() == Game.WORD_MODE) {
            drawWordMode(g);
        } else {
            drawSummary(g);
        }
        drawFooter(g);
        g.dispose();
    }

    // ---------- screens ----------

    private void drawHeader(Graphics2D g) {
        g.setColor(HEADER);
        g.fillRect(0, 0, W, 80);
        g.setColor(Color.WHITE);
        g.setFont(new Font("SansSerif", Font.BOLD, 36));
        g.drawString("AlphaBuild", 30, 54);

        String title = "Letter Learning";
        if (game.getMode() == Game.WORD_MODE) {
            title = "Word Building";
        } else if (game.getMode() == Game.SUMMARY) {
            title = "Round finished";
        }
        g.setFont(new Font("SansSerif", Font.BOLD, 28));
        drawCentered(g, title, 480, 52);

        int total = game.getTotalWords();
        for (int i = 0; i < total; i++) {
            drawStar(g, 760 + i * 38, 40, 16, i < game.getCorrectCount());
        }
    }

    private void drawLetterMode(Graphics2D g) {
        char letter = game.getShownLetter();
        if (letter == ' ') {
            g.setColor(new Color(60, 60, 80));
            g.setFont(new Font("SansSerif", Font.BOLD, 46));
            drawCentered(g, "Put a letter in front of the camera", W / 2, 290);
            g.setFont(new Font("SansSerif", Font.PLAIN, 30));
            g.setColor(new Color(110, 110, 130));
            drawCentered(g, "Each letter shows a picture", W / 2, 360);
            drawCentered(g, "Draw a Z in the air to build words", W / 2, 410);
            return;
        }
        Color color = LETTER_COLORS[(letter - 'A') % LETTER_COLORS.length];
        card(g, 60, 110, 380, 400);
        g.setColor(color);
        g.setFont(new Font("SansSerif", Font.BOLD, 260));
        drawCentered(g, String.valueOf(letter), 250, 390);
        g.setFont(new Font("SansSerif", Font.BOLD, 70));
        drawCentered(g, String.valueOf(letter).toLowerCase(), 250, 480);

        String word = Game.getExampleWord(letter);
        card(g, 500, 110, 440, 400);
        drawPicture(g, word, 720, 310, 340);

        g.setColor(new Color(60, 60, 80));
        g.setFont(new Font("SansSerif", Font.BOLD, 54));
        drawCentered(g, letter + " is for " + word, W / 2, 575);
    }

    private void drawWordMode(Graphics2D g) {
        String target = game.getCurrentWord();
        card(g, 60, 110, 380, 400);
        drawPicture(g, target, 250, 310, 330);
        g.setColor(new Color(60, 60, 80));
        g.setFont(new Font("SansSerif", Font.BOLD, 30));
        drawCentered(g, "Word " + game.getWordNumber() + " of " + game.getTotalWords()
                + ": spell it!", 250, 560);

        String letters = game.getLetters();
        int slots = Math.max(target.length(), letters.length());
        int size = 100;
        int gap = 16;
        int totalWidth = slots * size + (slots - 1) * gap;
        int startX = 700 - totalWidth / 2;
        for (int i = 0; i < slots; i++) {
            int x = startX + i * (size + gap);
            g.setColor(Color.WHITE);
            g.fillRoundRect(x, 200, size, size, 20, 20);
            g.setColor(new Color(120, 140, 190));
            g.setStroke(new java.awt.BasicStroke(4));
            g.drawRoundRect(x, 200, size, size, 20, 20);
            if (i < letters.length()) {
                char c = letters.charAt(i);
                g.setColor(LETTER_COLORS[(c - 'A') % LETTER_COLORS.length]);
                g.setFont(new Font("SansSerif", Font.BOLD, 72));
                drawCentered(g, String.valueOf(c), x + size / 2, 278);
            }
        }

        if (letters.isEmpty()) {
            g.setColor(new Color(110, 110, 130));
            g.setFont(new Font("SansSerif", Font.PLAIN, 28));
            drawCentered(g, "Put the letters on the table", 700, 350);
            drawCentered(g, "from left to right", 700, 390);
        }

        if (!game.getFeedback().isEmpty()) {
            g.setColor(game.isFeedbackGood() ? GOOD : BAD);
            g.setFont(new Font("SansSerif", Font.BOLD, 60));
            drawCentered(g, game.getFeedback(), 700, 470);
        }
        if (game.isAnsweredCorrect()) {
            g.setColor(new Color(110, 110, 130));
            g.setFont(new Font("SansSerif", Font.PLAIN, 28));
            drawCentered(g, "Circle in the air for the next word", 700, 530);
        } else {
            g.setColor(new Color(110, 110, 130));
            g.setFont(new Font("SansSerif", Font.PLAIN, 28));
            drawCentered(g, "Swipe your hand to check the word", 700, 530);
        }
    }

    private void drawSummary(Graphics2D g) {
        g.setColor(new Color(60, 60, 80));
        g.setFont(new Font("SansSerif", Font.BOLD, 84));
        drawCentered(g, "Well done!", W / 2, 210);
        int total = game.getTotalWords();
        int startX = W / 2 - (total * 80) / 2 + 40;
        for (int i = 0; i < total; i++) {
            drawStar(g, startX + i * 80, 300, 34, i < game.getCorrectCount());
        }
        g.setColor(new Color(60, 60, 80));
        g.setFont(new Font("SansSerif", Font.BOLD, 48));
        drawCentered(g, "You got " + game.getCorrectCount() + " of " + total
                + " words right", W / 2, 420);
        g.setFont(new Font("SansSerif", Font.PLAIN, 34));
        g.setColor(new Color(110, 110, 130));
        drawCentered(g, "Total tries: " + game.getTries(), W / 2, 480);
        drawCentered(g, "Make any gesture to play again", W / 2, 560);
    }

    private void drawFooter(Graphics2D g) {
        g.setColor(FOOTER);
        g.fillRect(0, 630, W, 70);
        g.setColor(connected ? new Color(80, 220, 120) : new Color(240, 90, 90));
        g.fillOval(24, 650, 20, 20);
        g.setColor(Color.WHITE);
        g.setFont(new Font("SansSerif", Font.PLAIN, 22));
        g.drawString(connected ? "Connected to Python" : "Waiting for Python...", 54, 667);

        g.setFont(new Font("SansSerif", Font.PLAIN, 22));
        drawRight(g, "Swipe = check    Circle = next    Z = switch mode", 975, 656);
        g.setFont(new Font("SansSerif", Font.PLAIN, 17));
        g.setColor(new Color(190, 200, 225));
        drawRight(g, "Keyboard: Enter = check, N = next, M = switch mode", 975, 682);
    }

    // ---------- helpers ----------

    private void card(Graphics2D g, int x, int y, int w, int h) {
        g.setColor(new Color(0, 0, 0, 30));
        g.fillRoundRect(x + 5, y + 6, w, h, 40, 40);
        g.setColor(Color.WHITE);
        g.fillRoundRect(x, y, w, h, 40, 40);
        g.setColor(new Color(225, 215, 190));
        g.setStroke(new java.awt.BasicStroke(3));
        g.drawRoundRect(x, y, w, h, 40, 40);
    }

    private void drawPicture(Graphics2D g, String word, int cx, int cy, int size) {
        BufferedImage image = loadImage(word);
        if (image != null) {
            g.drawImage(image, cx - size / 2, cy - size / 2, size, size, null);
        } else {
            // no picture file found: show the word on a colored card instead
            g.setColor(new Color(235, 240, 250));
            g.fillRoundRect(cx - size / 2, cy - size / 2, size, size, 30, 30);
            g.setColor(new Color(60, 60, 80));
            g.setFont(new Font("SansSerif", Font.BOLD, 48));
            drawCentered(g, word, cx, cy + 15);
        }
    }

    private BufferedImage loadImage(String word) {
        String name = Game.pictureName(word);
        if (!images.containsKey(name)) {
            BufferedImage image = null;
            try {
                image = ImageIO.read(new File(imageFolder, name + ".png"));
            } catch (Exception e) {
                System.out.println("Picture not found: " + name + ".png");
            }
            images.put(name, image);
        }
        return images.get(name);
    }

    private void drawStar(Graphics2D g, int cx, int cy, int radius, boolean filled) {
        Polygon star = new Polygon();
        for (int i = 0; i < 10; i++) {
            double r = (i % 2 == 0) ? radius : radius * 0.45;
            double angle = -Math.PI / 2 + i * Math.PI / 5;
            star.addPoint((int) Math.round(cx + r * Math.cos(angle)),
                          (int) Math.round(cy + r * Math.sin(angle)));
        }
        if (filled) {
            g.setColor(GOLD);
            g.fillPolygon(star);
        }
        g.setColor(filled ? new Color(200, 150, 20) : new Color(170, 180, 210));
        g.setStroke(new java.awt.BasicStroke(2));
        g.drawPolygon(star);
    }

    private void drawCentered(Graphics2D g, String text, int cx, int baseline) {
        FontMetrics fm = g.getFontMetrics();
        g.drawString(text, cx - fm.stringWidth(text) / 2, baseline);
    }

    private void drawRight(Graphics2D g, String text, int right, int baseline) {
        FontMetrics fm = g.getFontMetrics();
        g.drawString(text, right - fm.stringWidth(text), baseline);
    }
}
