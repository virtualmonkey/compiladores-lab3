class Fibonacci {
  	fibonacci(n: Int) : Int {
        {( let f : Int in
      	 if n=1 then f<-1 else
         if n=2 then f<-1 else
        	 f<-fibonacci(n-1)+fibonacci(n-2)
         fi fi
       );}
     };
  
  };

class Main {
  	fibo: Fibonacci <- (new Fibonacci);

  	main() : SELF_TYPE {
        {
            out_string("Enter a number to calculate fibonacci\n");
            out_int(fibo.fibonacci(in_int()));
            self;
        }
    };
};