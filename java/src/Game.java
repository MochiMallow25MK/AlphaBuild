// The game logic. It does not draw anything and does not know about sockets.
public class Game {

    public static final int LETTER_MODE = 0;   // Letter Learning
    public static final int WORD_MODE = 1;     // Word Building
    public static final int SUMMARY = 2;       // end of the round

    // One example word for every letter A to Z (the context content).
    public static final String[] LETTER_WORDS = {
        "Apple", "Ball", "Cat", "Dog", "Egg", "Fish", "Grapes", "Hat", "Ice cream",
        "Jam", "Kite", "Leaf", "Moon", "Nut", "Orange", "Pig", "Queen", "Rainbow",
        "Sun", "Tree", "Umbrella", "Van", "Watch", "Xylophone", "Yo-yo", "Zipper"
    };

    // Words to build. There is only one plastic copy of each letter,
    // so every word uses each letter only once.
    public static final String[] WORDS = {"CAT", "DOG", "SUN", "PIG", "HAT", "FISH"};

    private int mode = LETTER_MODE;
    private String letters = "";            // letters on the table, left to right
    private char shownLetter = ' ';         // letter shown in Letter Learning mode
    private int wordIndex = 0;
    private int correctCount = 0;
    private int tries = 0;
    private boolean answeredCorrect = false;
    private String feedback = "";
    private boolean feedbackGood = false;
    private long summaryTime = 0;

    // ---------- messages from Python ----------

    public void setLetters(String text) {
        text = text.trim().toUpperCase();
        // The newest letter on the table is the one we show in Letter Learning mode.
        for (int i = 0; i < text.length(); i++) {
            char c = text.charAt(i);
            if (letters.indexOf(c) < 0) {
                shownLetter = c;
            }
        }
        if (text.isEmpty()) {
            shownLetter = ' ';
        } else if (text.indexOf(shownLetter) < 0) {
            shownLetter = text.charAt(text.length() - 1);
        }
        letters = text;
        if (mode == WORD_MODE && !answeredCorrect) {
            feedback = "";                  // remove "Try again" when the child moves letters
        }
    }

    public void handleGesture(String name) {
        if (mode == SUMMARY) {
            // ignore the first two seconds so a repeated gesture does not skip the summary
            if (System.currentTimeMillis() - summaryTime > 2000) {
                restart();
            }
            return;
        }
        if (name.equals("switch")) {
            switchMode();
        } else if (name.equals("submit")) {
            submit();
        } else if (name.equals("next")) {
            next();
        }
    }

    // ---------- actions ----------

    private void switchMode() {
        feedback = "";
        if (mode == LETTER_MODE) {
            mode = WORD_MODE;
        } else {
            mode = LETTER_MODE;
        }
    }

    private void submit() {
        if (mode != WORD_MODE || answeredCorrect) {
            return;
        }
        if (letters.isEmpty()) {
            feedback = "Put the letters on the table first";
            feedbackGood = false;
            return;
        }
        tries++;
        if (letters.equals(getCurrentWord())) {
            correctCount++;
            answeredCorrect = true;
            feedback = "Great job!";
            feedbackGood = true;
        } else {
            feedback = "Try again!";
            feedbackGood = false;
        }
    }

    private void next() {
        if (mode != WORD_MODE) {
            return;
        }
        wordIndex++;
        answeredCorrect = false;
        feedback = "";
        if (wordIndex >= WORDS.length) {
            mode = SUMMARY;
            summaryTime = System.currentTimeMillis();
        }
    }

    private void restart() {
        mode = WORD_MODE;
        wordIndex = 0;
        correctCount = 0;
        tries = 0;
        answeredCorrect = false;
        feedback = "";
    }

    // Used by the keyboard shortcuts as well.
    public void submitKey() { handleGesture("submit"); }
    public void nextKey() { handleGesture("next"); }
    public void switchKey() { handleGesture("switch"); }

    // ---------- information for the screen ----------

    public int getMode() { return mode; }
    public String getLetters() { return letters; }
    public char getShownLetter() { return shownLetter; }
    public String getFeedback() { return feedback; }
    public boolean isFeedbackGood() { return feedbackGood; }
    public boolean isAnsweredCorrect() { return answeredCorrect; }
    public int getCorrectCount() { return correctCount; }
    public int getTries() { return tries; }
    public int getTotalWords() { return WORDS.length; }
    public int getWordNumber() { return Math.min(wordIndex + 1, WORDS.length); }

    public String getCurrentWord() {
        if (wordIndex < WORDS.length) {
            return WORDS[wordIndex];
        }
        return "";
    }

    public static String getExampleWord(char letter) {
        return LETTER_WORDS[letter - 'A'];
    }

    // "Ice cream" -> "icecream" (name of the picture file)
    public static String pictureName(String word) {
        return word.toLowerCase().replaceAll("[^a-z]", "");
    }
}
