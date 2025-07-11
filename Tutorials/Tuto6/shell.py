
#base on : https://www.youtube.com/watch?v=Eythq9848Fg&list=PLZQftyCk7_SdoVexSmwy_tBgs7P0b97yD from Lexer

import law

while True:

    text= input("law > ")
    result,error=law.run('<stdin>',text)
    if error:print(error.as_string() )
    else: print(result)
