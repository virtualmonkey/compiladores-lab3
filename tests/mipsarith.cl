class Main {
    a: Int;
    b: Int;
    x: Int;
    y: Int;
    total: Int;
    total2: Int;

    main() : Int {
        {
            a <- 2;
            b <- 4;
            total <- a + b;
            x <- 10;
            y <- 5;
            total2 <- x / y;

            total2;
        }
    };
};