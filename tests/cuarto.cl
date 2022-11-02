class Main {
    a: Int;
    respuesta1: Int;
    b: Int;
    c: Int;
    respuesta2: Int;
    respuesta3: Int;
    respuesta4: Int;

    sumaS: String;

    sum(
        sum1: Int,
        sum2: Int
    ): Int {
        sum1 + sum2
    };

    res(
        res1: Int,
        res2: Int
    ): Int {
        res1 - res2
    };

    mult(
        mult1: Int,
        mult2: Int
    ): Int {
        mult1 * mult2
    };

    div(
        div1: Int,
        div2: Int
    ): Int {
        div1 / div2
    };

    concate(
        con1: String,
        con2: String
    ): String {
        con1 + con2
    };


    main() : String {
        {
            b <- 5;
            respuesta1 <- sum(10, b);
            a <- 4;
            c <- 5;
            respuesta2 <- res(c, a);
            respuesta3 <- mult(3, 5);
            respuesta4 <- div(6, 2);
            sumaS <- concate("isa", "urbina");
            sumaS;
        }
    };
};