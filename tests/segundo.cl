class Main {
    a: Int;
    nombre1: String;
    respuesta1: Int;
    sumaS: String;

    sum(
        sum1: Int,
        sum2: Int
    ): Int {
        sum1 + sum2
    };

    concate(
        con1: String,
        con2: String
    ): String {
        con1 + con2
    };


    main() : String {
        {
            a <- 5;
            nombre1 <- "Isa";
            respuesta1 <- sum(10, a);
            sumaS <- concate(nombre1, "urbina");
            sumaS;
        }
    };
};