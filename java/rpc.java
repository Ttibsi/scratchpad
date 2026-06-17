import java.util.ArrayList;
import java.util.Stack;

// A reverse-polish notation calculation in Java

class RPC {
    private enum TokenType {
        ADD,
        SUB,
        MUL,
        DIV,
        DIGIT;
    }

    private class Token {
        public TokenType type;
        public double value = 0;

        Token(TokenType t) { this.type = t; }
        Token(double val) {
            this.type = TokenType.DIGIT;
            this.value = val;
        }
    }

    private ArrayList<Token> tokens = new ArrayList<>();

    RPC(String inp) {
        for (String c : inp.split(" ")) {
            switch (c) {
                case "+" -> tokens.add(new Token(TokenType.ADD));
                case "-" -> tokens.add(new Token(TokenType.SUB));
                case "*" -> tokens.add(new Token(TokenType.MUL));
                case "/" -> tokens.add(new Token(TokenType.DIV));
                default -> tokens.add(new Token(Double.parseDouble(c)));
            }
        }
    }

    public double calc() {
        Stack<Double> stk = new Stack<>();
        
        for (Token t: this.tokens) {
            if (t.type.equals(TokenType.DIGIT)) {
                stk.push(t.value); 
                continue;
            }

            double second = stk.pop();
            double first = stk.pop();
            switch (t.type) {
                case TokenType.ADD -> stk.push(first + second);
                case TokenType.SUB -> stk.push(first - second);
                case TokenType.MUL -> stk.push(first * second);
                case TokenType.DIV -> stk.push(first / second);
            }
        }

        return stk.pop();
    }
}

class Main {
    public static void main(String... args) {
        RPC rpc = new RPC("2 17 * 35 +");
        System.out.println(String.format("[RESULT]: %.1f", rpc.calc()));
    }
}
