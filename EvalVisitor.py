if __name__ is not None and "." in __name__:
    from .ExprParser import ExprParser
    from .ExprVisitor import ExprVisitor
else:
    from ExprParser import ExprParser
    from ExprVisitor import ExprVisitor


class EvalVisitor(ExprVisitor):
    def __init__(self):
        self.nivell = 0

    def visitRoot(self, ctx: ExprParser.RootContext):
        l = list(ctx.getChildren())
        print(self.visit(l[0]))

    def visitSuma(self, ctx: ExprParser.SumaContext):
        l = list(ctx.getChildren())
        print('  ' * self.nivell + 'MES(+)')
        self.nivell += 1
        aux = self.visit(l[0]) + self.visit(l[2])
        self.nivell -= 1
        return aux

    def visitValor(self, ctx: ExprParser.ValorContext):
        l = list(ctx.getChildren())
        print("  " * self.nivell +
              ExprParser.symbolicNames[l[0].getSymbol().type] +
              '(' + l[0].getText() + ')')
        return int(l[0].getText())

    def visitProducte(self, ctx: ExprParser.ProducteContext):
        l = list(ctx.getChildren())
        print('  ' * self.nivell + 'PROD(*)')
        self.nivell += 1
        aux = self.visit(l[0]) * self.visit(l[2])
        self.nivell -= 1
        return aux

    # Visit a parse tree produced by ExprParser#Divisio.
    def visitDivisio(self, ctx: ExprParser.DivisioContext):
        l = list(ctx.getChildren())
        print('  ' * self.nivell + 'DIV(/)')
        self.nivell += 1
        aux = self.visit(l[0]) * self.visit(l[2])
        self.nivell -= 1
        return aux

    # Visit a parse tree produced by ExprParser#Potencia.
    def visitPotencia(self, ctx: ExprParser.PotenciaContext):
        l = list(ctx.getChildren())
        print('  ' * self.nivell + 'POT(^)')
        self.nivell += 1
        aux = self.visit(l[0]) ** self.visit(l[2])
        self.nivell -= 1
        return aux

    # Visit a parse tree produced by ExprParser#Resta.
    def visitResta(self, ctx: ExprParser.RestaContext):
        l = list(ctx.getChildren())
        print('  ' * self.nivell + 'MENYS(-)')
        self.nivell += 1
        aux = self.visit(l[0]) - self.visit(l[2])
        self.nivell -= 1
        return aux
