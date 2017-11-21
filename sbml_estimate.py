import sys
from libsbml import *

def getODEFromModel(y, t, *args):
    model = args[0]
    species = args[1]
    dSpecies = 0

    for reaction in model.getListOfReactions():
        for reactant in reaction.getListOfReactants():
            if reactant.getId() == species:
                ast = reaction.getKineticLaw()
                dSpecies = dSpecies - (reactant.getStoichiometry() * astToEquation(ast))
                
        for product in reaction.getListOfProducts():
            if product.getId() == species:
                ast = reaction.getKineticLaw()
                dSpecies = dSpecies + (product.getStoichiometry() * astToEquation(ast))
                
    return dSpecies


def getASTFromModel(model, species):
    ast = ASTNode(AST_INTEGER)
    ast.setValue(0)

    for reaction in model.getListOfReactions():
        for reactant in reaction.getListOfReactants():
            if reactant.getId() == species:
                equation = reaction.getKineticLaw()
                if reactant.getStoichiometry() > 1:
                    stoicNode = ASTNode(AST_INTEGER)
                    stoicNode.setValue(reactant.getStoichiometry())
                    multNode = ASTNode(AST_TIMES)
                    multNode.addChild(stoicNode)
                    multNode.addChild(equation)
                    equation = multNode
                newNode = ASTNode(AST_MINUS)
                newNode.addChild(ast)
                newNode.addChild(equation)
                ast = newNode
                
        for product in reaction.getListOfProducts():
            if product.getId() == species:
                equation = reaction.getKineticLaw()
                if product.getStoichiometry() > 1:
                    stoicNode = ASTNode(AST_INTEGER)
                    stoicNode.setValue(product.getStoichiometry())
                    multNode = ASTNode(AST_TIMES)
                    multNode.addChild(stoicNode)
                    multNode.addChild(equation)
                    equation = multNode
                newNode = ASTNode(AST_PLUS)
                newNode.addChild(ast)
                newNode.addChild(equation)
                ast = newNode
                
    return ast

def astToEquation(ast, values):
    if ast.getType() == AST_PLUS:
        return (astToEquation(ast.getLeftChild()) + astToEquation(ast.getRightChild()))
    elif ast.getType() == AST_MINUS:
        return (astToEquation(ast.getLeftChild()) - astToEquation(ast.getRightChild()))
    elif ast.getType() == AST_TIMES:
        return (astToEquation(ast.getLeftChild()) * astToEquation(ast.getRightChild()))
    elif ast.getType() == AST_DIVIDE:
        return (astToEquation(ast.getLeftChild()) / astToEquation(ast.getRightChild()))
    elif ast.getType() == AST_POWER:
        return (astToEquation(ast.getLeftChild()) ** astToEquation(ast.getRightChild()))
    elif ast.getType() == AST_INTEGER:
        return ast.getInteger()
    elif ast.getType() == AST_REAL:
        return ast.getReal()
    elif ast.getType() == AST_RATIONAL:
        return (ast.getNumerator() / ast.getDenominator())
    elif ast.getType() == AST_REAL_E:
        return (ast.getMantissa() ** ast.getExponent())
    elif ast.getType() == AST_NAME:
        for name, value in values:
            if ast.getName() == name:
                return value
            