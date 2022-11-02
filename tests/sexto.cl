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
    
    n: Int <- 10;
  	facto: Factorial;
  	fibo: Fibonacci;
  
  	main() : SELF_TYPE {
	{
      	fibo <- new Fibonacci;
      	out_int(fibo.fibonacci(n));
      	self;
	}
    };
};