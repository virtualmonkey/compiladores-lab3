class Main {
    a: Int;
    total: Int;
    b: Int;
    x: Int;
    total2: Int;
    y: Int;

    s: String;
    r: String;
    sumaS: String;

    main() : String {
        {
            a <- 2;
            b <- 4;
            total <- a + b;
            x <- 5-2 * total;
            y <- total / 5;
            total2 <- x + y;

            s <- "isa";
            r <- "urbina";
            sumaS <- s + r;
            sumaS;
        }
    };
};