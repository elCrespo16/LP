from turtle3d import Turtle3D

if __name__ is not None and "." in __name__:
    from .logo3dParser import logo3dParser
    from .logo3dVisitor import logo3dVisitor
else:
    from logo3dParser import logo3dParser
    from logo3dVisitor import logo3dVisitor


class EvalVisitor(logo3dVisitor):

    def add_funcions_tortuga(self):
        """
        Funcion para añadir a la lista de funciones las funciones de la tortuga y sus parametros
        """
        self.funcions["left"] = TortugaFunction(["angle"], self.tortuga.left)
        self.funcions["right"] = TortugaFunction(["angle"], self.tortuga.right)
        self.funcions["forward"] = TortugaFunction(["mida"], self.tortuga.forward)
        self.funcions["backward"] = TortugaFunction(["mida"], self.tortuga.backward)
        self.funcions["up"] = TortugaFunction(["angle"], self.tortuga.up)
        self.funcions["down"] = TortugaFunction(["angle"], self.tortuga.down)
        self.funcions["hide"] = TortugaFunction([], self.tortuga.hide)
        self.funcions["show"] = TortugaFunction([], self.tortuga.show)
        self.funcions["home"] = TortugaFunction([], self.tortuga.home)
        self.funcions["color"] = TortugaFunction(["r", "g", "b"], self.tortuga.color)

    def __init__(self):
        """
        Funcion de inicializacion de la clase
        - funcions contiene todas las funciones llamables por el usuario
        - pila_diccionaris contiene la tablas de simbolos de las funciones
        - tortuga contiene una instacia de Tortuga3D
        - tortuga_inicialized contiene un bool para saber si se ha hecho alguna llamada de tortuga
        - funcions_tortuga contiene el nombre de las funciones de tortuga y se podria usar para funciones predefinidas
        """
        self.funcions = {}
        self.pila_diccionaris = []
        self.tortuga = Turtle3D()
        self.tortuga_inicialized = False
        self.funcions_tortuga = ["left", "right", "forward", "backward", "up", "down", "hide", "show", "home", "color"]
        self.add_funcions_tortuga()

    def visitRoot(self, ctx: logo3dParser.RootContext):
        """
        Funcion para visitar la raiz del arbol. Los hijos de este son las funciones definidas por el usuario
        :param ctx: Contexto de la raiz
        :return: No devuelve nada
        """
        l = list(ctx.getChildren())
        for fills in l:
            self.visit(fills)

    def visitFunc(self, ctx: logo3dParser.FuncContext):
        """
        Funcion para añadir funciones definidas por el usuario a la lista de funciones
        :param ctx: Contexto de una funcion
        :return: No devuelve nada
        """
        l = list(ctx.getChildren())
        name = l[1].getText()
        if name in self.funcions:
            raise Exception(f"Funcio {name} repetida")
        parameters = self.visit(l[2])
        self.funcions[name] = UserFunction(list_parameters=parameters, context=ctx, visitor=self)

    def visitFunction_list_params_names(self, ctx: logo3dParser.Function_list_params_namesContext):
        """
        Funcion para tratar la lista de parametros en la cabecera de una funcion
        :param ctx: Contexto de la lista
        :return: Devuelve una lista con los nombres de los parametros de la cabecera de una funcion
        """
        l = list(ctx.getChildren())
        if len(l) == 2:
            return []
        return self.visit(l[1])

    def visitMultipleParamsNames(self, ctx: logo3dParser.MultipleParamsNamesContext):
        """
        Funcion para tratar un conjunto no vacio de parametros en la cabecera de una funcion
        :param ctx: Contexto de los parametros
        :return: Lista no vacia de los nombres de los parametros de la cabecera de una funcion
        """
        l = list(ctx.getChildren())
        a1 = self.visit(l[0])
        a2 = self.visit(l[2])
        if a1 and a2:
            return a1 + a2
        elif a1:
            return a1
        return a2

    def visitOneParamName(self, ctx: logo3dParser.OneParamNameContext):
        """
        Funcion para tratar un unico parametro en la cabecera de una funcion
        :param ctx: Contexto del parametro
        :return: Lista no vacia con el nombre del parametro de la cabecera
        """
        return [ctx.getText()]

    def execute_function(self, func: str = "main", list_parameters: list = None):
        """
        Funcion para ejecutar una funcion especifica
        :param func: Nombre de la funcion a ejecutar
        :param list_parameters: Lista de parametros de la funcion a ejecutar
        :return: Si no existe la funcion o no hay suficientes parametros ejecuta una excepcion, si no, no devuelve nada
        """
        list_parameters = list_parameters or []
        if func in self.funcions_tortuga and not self.tortuga_inicialized:
            self.tortuga.inicialize_scene()
            self.tortuga_inicialized = True
        if func not in self.funcions:
            raise Exception(f"Crida a funcio {func} no definida")
        if len(list_parameters) == len(self.funcions[func].parameters):
            self.funcions[func].execute(list_parameters)
        else:
            raise Exception(f"Crida a funcio {func} sense suficients arguments")

    def visitList_params_call(self, ctx: logo3dParser.List_params_callContext):
        """
        Funcion para tratar los parametros en la llamada a una funcion
        :param ctx: Contexto de la llamada
        :return: Devuelve una lista de parametros de una llamada a una funcion
        """
        l = list(ctx.getChildren())
        if len(l) == 2:
            return []
        return self.visit(l[1])

    def visitMultipleParamsCall(self, ctx: logo3dParser.MultipleParamsCallContext):
        """
        Funcion para tratar un conjunto no vacio de parametros en la llamada a una funcion
        :param ctx: Contexto de los parametros
        :return: Devuelve una lista no vacia con los valores de los parametros en una llamada a una funcion
        """
        l = list(ctx.getChildren())
        a1 = self.visit(l[0])
        a2 = self.visit(l[2])
        if a1 and a2:
            return a1 + a2
        elif a1:
            return a1
        return a2

    def visitOneParamCall(self, ctx: logo3dParser.OneParamCallContext):
        """
        Funcion para tratar un parametro en la llamada a una funcion
        :param ctx: Contexto del parametro
        :return: Lista con el valor del parametro
        """
        return [self.visitChildren(ctx)]

    def visitCridaFunc(self, ctx: logo3dParser.CridaFuncContext):
        """
        Funcion para gestionar la llamada a una funcion
        :param ctx: Contexto de la llamada a la funcion
        :return: No devuelve nada
        """
        l = list(ctx.getChildren())
        name = l[0].getText()
        if name in self.funcions:
            parameters = self.visit(l[1])
            self.execute_function(name, parameters)
        else:
            raise Exception(f"Crida a funcio {name} no definida")

    def visitSuma(self, ctx: logo3dParser.SumaContext):
        """
        Funcion para gestionar la llamada a una suma
        :param ctx: Contexto de la suma
        :return: Devuelve el valor de la suma
        """
        l = list(ctx.getChildren())
        return self.visit(l[0]) + self.visit(l[2])

    def visitValor(self, ctx: logo3dParser.ValorContext):
        """
        Funcion para gestionar la llamada a un valor
        :param ctx: Contexto de la suma
        :return: Devuelve el valor
        """
        l = list(ctx.getChildren())
        return float(l[0].getText())

    def visitProducte(self, ctx: logo3dParser.ProducteContext):
        """
        Funcion para gestionar la llamada a un producto
        :param ctx: Contexto del producto
        :return: Devuelve el valor del producto
        """
        l = list(ctx.getChildren())
        return self.visit(l[0]) * self.visit(l[2])

    def visitDivisio(self, ctx: logo3dParser.DivisioContext):
        """
        Funcion para gestionar la llamada a una division
        :param ctx: Contexto de la divison
        :return: Si es division entre 0 da una excepcion, sino, devuelve el valor de la division
        """
        l = list(ctx.getChildren())
        aux1 = self.visit(l[0])
        aux2 = self.visit(l[2])
        if aux2 == 0:
            raise ZeroDivisionError();
        return aux1 / aux2

    def visitPotencia(self, ctx: logo3dParser.PotenciaContext):
        """
        Funcion para gestionar la llamada a una potencio
        :param ctx: Contexto de la potencia
        :return: Devuelve el resultado de la potencia
        """
        l = list(ctx.getChildren())
        return self.visit(l[0]) ** self.visit(l[2])

    def visitResta(self, ctx: logo3dParser.RestaContext):
        l = list(ctx.getChildren())
        return self.visit(l[0]) - self.visit(l[2])

    def visitVariable(self, ctx: logo3dParser.VariableContext):
        """
        Funcion para gestionar la llamada a una resta
        :param ctx: Contexto de la resta
        :return: Devuelve el resultado de la resta
        """
        l = ctx.getText()
        if l in self.pila_diccionaris[-1]:
            return self.pila_diccionaris[-1][l]
        else:
            raise Exception(f"Variable {l} no definida")

    def visitAsignacion(self, ctx: logo3dParser.AsignacionContext):
        """
        Funcion para gestionar una asignacion
        :param ctx: Contexto de la asignacion
        :return: No devuelve nada
        """
        l = list(ctx.getChildren())
        self.pila_diccionaris[-1][l[0].getText()] = self.visit(l[2])

    def visitWrite(self, ctx: logo3dParser.WriteContext):
        """
        Funcion para gestionar un write
        :param ctx: Contexto del write
        :return: No devuelve nada
        """
        l = list(ctx.getChildren())
        print(self.visit(l[1]))

    def visitMenorIgual(self, ctx: logo3dParser.MenorIgualContext):
        """
        Funcion para gestionar un <=
        :param ctx: Contexto de la expresion
        :return: 1 si expr1 <= expr2
        """
        l = list(ctx.getChildren())
        if self.visit(l[0]) <= self.visit(l[2]):
            return 1
        return 0

    def visitMayorIgual(self, ctx: logo3dParser.MayorIgualContext):
        """
        Funcion para gestionar un >=
        :param ctx: Contexto de la expresion
        :return: 1 si expr1 >= expr2
        """
        l = list(ctx.getChildren())
        if self.visit(l[0]) >= self.visit(l[2]):
            return 1
        return 0

    def visitMayor(self, ctx: logo3dParser.MayorContext):
        """
        Funcion para gestionar un >
        :param ctx: Contexto de la expresion
        :return: 1 si expr1 > expr2
        """
        l = list(ctx.getChildren())
        if self.visit(l[0]) > self.visit(l[2]):
            return 1
        return 0

    def visitDesigual(self, ctx: logo3dParser.DesigualContext):
        """
        Funcion para gestionar un !=
        :param ctx: Contexto de la expresion
        :return: 1 si expr1 != expr2
        """
        l = list(ctx.getChildren())
        if self.visit(l[0]) != self.visit(l[2]):
            return 1
        return 0

    def visitMenor(self, ctx: logo3dParser.MenorContext):
        """
        Funcion para gestionar un <
        :param ctx: Contexto de la expresion
        :return: 1 si expr1 < expr2
        """
        l = list(ctx.getChildren())
        if self.visit(l[0]) < self.visit(l[2]):
            return 1
        return 0

    def visitIgual(self, ctx: logo3dParser.IgualContext):
        """
        Funcion para gestionar un ==
        :param ctx: Contexto de la expresion
        :return: 1 si expr1 == expr2
        """
        l = list(ctx.getChildren())
        if self.visit(l[0]) == self.visit(l[2]):
            return 1
        return 0

    def evalua_cond(self, ctx):
        """
        Funcion para evaluar una condicion
        :param ctx: Contexto de la condicion
        :return: False si la condicion esta entre -1e-6 y 1e-6, True en cualquier otro caso
        """
        if -1e-6 <= self.visit(ctx) <= 1e-6:
            return False
        return True

    def visitIf(self, ctx: logo3dParser.IfContext):
        """
        Funcion para evaluar un if
        :param ctx: Contexto del if
        :return: No devuelve nada
        """
        l = list(ctx.getChildren())
        if self.evalua_cond(l[1]):
            for i in l[3:-1]:
                self.visit(i)

    def visitIfElse(self, ctx: logo3dParser.IfElseContext):
        """
        Funcion para evaluar un If then Else
        :param ctx: Contexto del If then Else
        :return: No devuelve nada
        """
        l = list(ctx.getChildren())
        stop_statement = 0
        for idx, val in enumerate(l):
            if val.getText() == "ELSE":
                stop_statement = idx
        if self.evalua_cond(l[1]):
            for i in l[3:stop_statement]:
                self.visit(i)
        else:
            for i in l[stop_statement:-1]:
                self.visit(i)

    def visitWhile(self, ctx: logo3dParser.WhileContext):
        """
        Funcion para evaluar un while
        :param ctx: Contexto del while
        :return: No devuelve nada
        """
        l = list(ctx.getChildren())
        while self.evalua_cond(l[1]):
            for i in l[3:-1]:
                self.visit(i)

    def visitFor(self, ctx: logo3dParser.ForContext):
        """
       Funcion para evaluar un for
       :param ctx: Contexto del for
       :return: No devuelve nada
       """
        l = list(ctx.getChildren())
        stop_statement = 0
        for idx, val in enumerate(l):
            if val.getText() == "DO":
                stop_statement = idx
        var = l[1].getText()
        ini = self.visit(l[3])
        fin = self.visit(l[5])
        ranges = []
        while ini < fin:
            ranges.append(ini)
            ini += 1
        i = 0
        while i < len(ranges):
            self.pila_diccionaris[-1][var] = ranges[i]
            for s in l[stop_statement:-1]:
                self.visit(s)
            i += 1
        del self.pila_diccionaris[-1][var]

    def visitRead(self, ctx: logo3dParser.ReadContext):
        """
        Funcion para gestionar un read
        :param ctx: Contexto del read
        :return: No devuelve nada
        """
        l = list(ctx.getChildren())
        self.pila_diccionaris[-1][l[1].getText()] = float(input('? '))


class Function:
    """
    Clase que gestiona una funcion
    """
    def __init__(self, list_parameters: list = None):
        """
        Inicializacion de la clase funcion
        :param list_parameters: Lista de parametros de la funcion
        """
        list_parameters = list_parameters or []
        self.parameters = list_parameters[:]

    def execute(self, list_parameters: list = None):
        """
        Funcion abstracta para ejecutar la funcion
        :param list_parameters: Lista de parametros de la funcion
        :return:
        """
        return None


class TortugaFunction(Function):
    """
    Clase para gestionar las funciones de tortuga
    """
    def __init__(self, list_parameters: list, context):
        """
        Inicializacion de la clase
        :param list_parameters: lista de parametros de la funcion
        :param context: Referencia a la funcion a ejecutar
        """
        super().__init__(list_parameters)
        self.context = context

    def execute(self, list_parameters: list = None):
        """
        Funcion que ejecuta la funcion que hay en el contexto
        :param list_parameters: Lista de parametros para la funcion
        :return:
        """
        list_parameters = list_parameters or []
        self.context(*list_parameters)


class UserFunction(Function):
    """
    Clase para gestionar las funciones del usuario
    """
    def __init__(self, list_parameters: list, context: logo3dParser.FuncContext, visitor: EvalVisitor):
        """
        Inicializacion de la clase
        :param list_parameters: lista de parametros
        :param context: Contexto de la funcion en el arbol
        :param visitor: Visitador del arbol que ejecutara la funcion
        """
        super().__init__(list_parameters)
        self.context = context
        self.visitor = visitor

    def execute(self, list_parameters: list = None):
        """
        Funcion que ejecuta la funcion del arbol en contexto usando el visitor
        :param list_parameters: lista de parametros
        :return: No devuelve nada
        """
        list_parameters = list_parameters or []
        aux = {}
        for idx, val in enumerate(self.parameters):
            aux[val] = list_parameters[idx]
        self.visitor.pila_diccionaris.append(aux)
        self.visitor.visitChildren(self.context)
        self.visitor.pila_diccionaris.pop(-1)
