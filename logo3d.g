grammar logo3d;
root : funcion*
    EOF ;

function_list_params_names:
    | '('')'
    | '('function_params_names')'
    ;
function_params_names: function_params_names ',' function_params_names #MultipleParamsNames
    | VAR #OneParamName
    ;

funcion: PROC VAR function_list_params_names IS stmt* END #Func ;


expr : '(' expr ')' #Parentesis
    | <assoc=right> expr POT expr #Potencia
    | expr PROD expr #Producte
    | expr DIV expr #Divisio
    | expr MES expr #Suma
    | expr MENYS expr #Resta
    | expr MENOR expr #Menor
    | expr MAYOR expr #Mayor
    | expr MENORIGUAL expr #MenorIgual
    | expr MAYORIGUAL expr #MayorIgual
    | expr IGUALDAD expr #Igual
    | expr DESIGUALDAD expr #Desigual
    | VAR #Variable
    | NUMBER #Valor
    ;

list_params_call: '('')'
    | '('params_call')'
    ;

params_call: params_call ','params_call #MultipleParamsCall
    | expr #OneParamCall
    ;

stmt : VAR list_params_call #CridaFunc
    | VAR ASSIG expr #Asignacion
    | WRITE expr #Write
    | READ VAR #Read
    | IF expr THEN stmt+ ELSE stmt+ END #IfElse
    | IF expr THEN stmt+ END #If
    | WHILE expr DO stmt+ END #While
    | FOR VAR FROM expr TO expr DO stmt+ END #For
    ;

PROC: 'PROC';
IS: 'IS';

TO: 'TO';
FOR: 'FOR';
FROM: 'FROM';
DO: 'DO';
WHILE: 'WHILE';

ELSE: 'ELSE';
IF: 'IF';
THEN: 'THEN';
END: 'END';

ASSIG: ':=';
WRITE: '<<';
READ: '>>';

VAR: LETRA(LETRA|NUMBER)*;
LETRA: [a-zA-Z];

NUMBER: NUM
    | NUM 'e' NUM;
NUM : [0-9]+ '.' [0-9]*
    | '.' [0-9]+
    | [0-9]+
    ;

MES : '+' ;
MENYS: '-' ;
PROD: '*' ;
DIV: '/' ;
POT: '^' ;
IGUALDAD: '==';
DESIGUALDAD: '!=';
MENOR: '<';
MAYOR: '>';
MENORIGUAL: '<=';
MAYORIGUAL: '>=';

COMENTARIOS: '//' ~( '\r' | '\n' )* -> skip ;

WS : [ \n\r]+ -> skip ;


