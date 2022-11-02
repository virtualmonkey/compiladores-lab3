class Main {
    a: Int;
    resultado: Int;
    b: Int;

    mult(
        x: Int,
        y: Int
    ): Int {
        x * y
    };

    main() : Int {
        {
            b <- 9;
            a <- mult(10, b);
            while resultado < 100 loop 
                if resultado < 50 then 
                    resultado <- resultado + 5
                else 
                    resultado <- resultado + 10
                fi 
            POOL
            resultado <- 0;
            resultado;
        }
    };
};