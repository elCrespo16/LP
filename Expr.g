grammar Expr;
root : expr EOF ;
expr : <assoc=right> expr POT expr #Potencia
    | expr PROD expr #Producte
    | expr DIV expr #Divisio
    | expr MES expr #Suma
    | expr MENYS expr #Resta
    | NUM #Valor
    ;
NUM : [0-9]+ ;
MES : '+' ;
WS : [ \n]+ -> skip ;
MENYS: '-' ;
PROD: '*' ;
DIV: '/' ;
POT: '^' ;
