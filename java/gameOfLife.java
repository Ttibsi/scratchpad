package gameOfLife;

import java.util.ArrayList;

class gameOfLife {
    private static final int board_sz = 50;
    private static Cell[] gliderGun = {
        new Cell(1, 5), new Cell(1, 6), new Cell(2, 5), new Cell(2, 6), 
        new Cell(11, 5), new Cell(11, 6), new Cell(11, 7), new Cell(12, 4), 
        new Cell(12, 8), new Cell(13, 3), new Cell(13, 9), new Cell(14, 3), 
        new Cell(14, 9), new Cell(15, 6), new Cell(16, 4), new Cell(16, 8), 
        new Cell(17, 5), new Cell(17, 6), new Cell(17, 7), new Cell(18, 6), 
        new Cell(21, 3), new Cell(21, 4), new Cell(21, 5), new Cell(22, 3), 
        new Cell(22, 4), new Cell(22, 5), new Cell(23, 2), new Cell(23, 6), 
        new Cell(25, 1), new Cell(25, 2), new Cell(25, 6), new Cell(25, 7), 
        new Cell(35, 3), new Cell(35, 4), new Cell(36, 3), new Cell(36, 4)
    };
    private static Cell[] relatives = {
        new Cell(-1, -1), new Cell(-1, 0), new Cell(-1, 1),
        new Cell(0, -1),                   new Cell(0, 1),
        new Cell(1, -1), new Cell(1, 0), new Cell(1, 1),
    };

    private static class Cell {
        int x;
        int y;
        boolean alive;

        Cell(int x, int y) {
            this.x = x;
            this.y = y;
            this.alive = false;
        }

        Cell(int x, int y, boolean b) {
            this.x = x;
            this.y = y;
            this.alive = b;
        }

        public void toggle() { this.alive = !this.alive; }
        public boolean isAlive() { return this.alive; }
    }

    private static int find(int x, int y) {
        return x * board_sz + y;
    }

    private static boolean verifyOutput(ArrayList<Cell> grid) {
        final Cell[] expected = {
            new Cell(1, 5), new Cell(1, 6), new Cell(2, 5), new Cell(2, 6), new Cell(7, 5), new Cell(7, 6),
            new Cell(7, 7), new Cell(8, 5), new Cell(8, 6), new Cell(8, 7), new Cell(9, 4), new Cell(9, 8), 
            new Cell(11, 3), new Cell(11, 4), new Cell(11, 8), new Cell(11, 9), new Cell(16, 3), new Cell(16, 4),
            new Cell(16, 5), new Cell(17, 7), new Cell(17, 8), new Cell(18, 7), new Cell(18, 8), new Cell(19, 8), 
            new Cell(19, 9), new Cell(20, 6), new Cell(20, 8), new Cell(21, 6), new Cell(21, 7), new Cell(24, 1),
            new Cell(24, 2), new Cell(24, 6), new Cell(24, 7), new Cell(25, 1), new Cell(25, 2), new Cell(25, 6), 
            new Cell(25, 7), new Cell(26, 13), new Cell(27, 3), new Cell(27, 4), new Cell(27, 5), new Cell(27, 14),
            new Cell(27, 15), new Cell(28, 3), new Cell(28, 4), new Cell(28, 5), new Cell(28, 13), new Cell(28, 14), 
            new Cell(29, 4), new Cell(34, 20), new Cell(34, 22), new Cell(35, 3), new Cell(35, 4), new Cell(35, 21),
            new Cell(35, 22), new Cell(36, 3), new Cell(36, 4), new Cell(36, 21), new Cell(41, 28), new Cell(42, 29), 
            new Cell(42, 30), new Cell(43, 28), new Cell(43, 29)
        };

        if (grid.stream().filter(c -> c.isAlive()).count() != expected.length) {
            return false;
        }

        return true;
    }

    public static void main(String... args) {
        // Create board with pre-initialised capacity
        ArrayList<Cell> grid = new ArrayList<>(board_sz * board_sz);

        for (int i = 0; i < board_sz; i++) {
            for (int j = 0; j < board_sz; j++) {
                grid.add(new Cell(i, j));
            }
        }

        for (Cell c: gliderGun) {
            grid.get(find(c.x, c.y)).toggle();
        }


        // Iterate
        final int iterations = 100_000;
        for (int i = 0; i < iterations; i++) {
            ArrayList<Cell> new_grid = new ArrayList<>(board_sz * board_sz);
            for (int j = 0; j < board_sz; j++) {
                for (int k = 0; k < board_sz; k++) {

                    int live = 0;
                    for (Cell rel: relatives) {
                        try {
                            if (grid.get(find(j + rel.x, k + rel.y)).isAlive()) { live++; }
                        } catch (IndexOutOfBoundsException e) {
                            continue;
                        }
                    }

                    if (grid.get(find(j, k)).isAlive()) {
                        boolean checkIsAlive = live == 2 || live == 3 ? true : false;
                        new_grid.add(new Cell(j, k, checkIsAlive));
                    } else {
                        new_grid.add(new Cell(j, k, live == 3));
                    }
                }
            }

            grid = new_grid;
        }

        System.out.printf("Valid output: %b\n", verifyOutput(grid));
    }
}
