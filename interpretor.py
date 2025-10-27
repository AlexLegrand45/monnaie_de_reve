

# inspiring from https://www.youtube.com/watch?v=Q2UDHY5as90
#
class Interpretor():
    def ev(self,text):
        self.vars={}
        lines=[x for x in text.split("\n") if x.strip() != ""]
#        print(lines)
        pc=0
        while pc< len(lines):
            line=lines[pc]
  #          print("line:  ",line)
            match line.split(maxsplit=1)[0]:
                case 'while':
              #      print("res:",self.ev_expr(line.split(maxsplit=1)[1]))
                    if self.ev_expr(line.split(maxsplit=1)[1])==1: pc+=1
                    else:
                        while lines[pc].split(maxsplit=1)[0] != 'end' : pc +=1
                        pc +=1
                case 'end':
                    while lines[pc].split(maxsplit=1)[0] != 'while': pc -=1
                case _:
                    (name,_,expr)=line.split(maxsplit=2)
 #                   print("actions   name:",name,"   expr:", expr, "\n")
                    self.vars[name]=self.ev_expr(expr)
                    pc+=1
#            print(self.vars)

        print(self.vars)
    def ev_expr(self,text):
        toks=text.split()
        stack=[]
        for tok in toks:
            if tok.isdigit(): stack.append(int(tok))
            elif tok in self.vars: stack.append(self.vars[tok])
            else:
                rhs=stack.pop()
                lhs=stack.pop()
#                print("var:",self.vars,"  rhs: ", rhs, "lhs:",lhs)

                if tok=="+":    stack.append(lhs+rhs)
                elif tok=="-":    stack.append(lhs-rhs)
                elif tok=="*":    stack.append(lhs*rhs)
                elif tok=="<":
                    if lhs < rhs: stack.append(1)
                    else: stack.append(0)
                elif tok==">":
                    if lhs > rhs: stack.append(1)
                    else: stack.append(0)
                elif tok=="<=":
                    if lhs <= rhs: stack.append(1)
                    else: stack.append(0)
                elif tok==">=":
                    if lhs >= rhs: stack.append(1)
                    else: stack.append(0)
                elif tok=="==":
                    if lhs == rhs: stack.append(1)
                    else: stack.append(0)


        return(stack[0])

text="n = 13  \n"
text=text+"r = 1  \n"
text=text+"while n 1 >= \n"
text=text+"r = r n * \n"
text=text+"n =  n 1 - \n"
text=text+"end \n"

Interpretor().ev(text)
