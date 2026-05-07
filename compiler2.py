import tkinter as tk
from tkinter import messagebox
from lark import Lark, exceptions

# 1. Grammar (Updated with bool, array access, and length function)
k_lang_grammar = """
start: statement+

statement: declaration ";"
         | assignment ";"
         | condition
         | loop
         | method_decl
         | method_call ";"

declaration: "create" TYPE CNAME
TYPE: "int" | "float" | "string" | "array" | "bool"

assignment: CNAME "=" expression
          | CNAME "[" expression "]" "=" expression

condition: "if" "(" cond_expr ")" "{" statement+ "}" ("else" "{" statement+ "}")?

loop: "repeat" "(" cond_expr ")" "{" statement+ "}"

method_decl: "function" CNAME "(" param_list? ")" "{" statement+ "}"
param_list: TYPE CNAME ("," TYPE CNAME)*

method_call: "call" CNAME "(" arg_list? ")"
arg_list: expression ("," expression)*

cond_expr: expression OP expression
OP: ">" | "<" | "==" | "!=" | ">=" | "<="

expression: term (("+"|"-") term)*
term: factor (("*"|"/") factor)*
factor: CNAME 
      | SIGNED_NUMBER 
      | ESCAPED_STRING 
      | "true"
      | "false"
      | CNAME "[" expression "]"
      | "length" "(" CNAME ")"
      | "(" expression ")"
      | "[" arg_list? "]" 

%import common.CNAME
%import common.SIGNED_NUMBER
%import common.ESCAPED_STRING
%import common.WS
%ignore WS
"""

# Initialize the Parser
parser = Lark(k_lang_grammar, parser='lalr')

# 2. (UI - Windows Forms Alternative)
def compile_code():
    code = text_editor.get("1.0", tk.END)
    try:
        tree = parser.parse(code)
        messagebox.showinfo("Success", "Great Job!\nCode compiled Successfully.")
        print("====== Parse Tree ======")
        print(tree.pretty()) 
    except exceptions.UnexpectedInput as e:
        messagebox.showerror("Syntax Error", f"There is an error in the code:\n\n{e.get_context(code)}")

# App window settings
app = tk.Tk()
app.title("KAM Compiler - By Karim")
app.geometry("650x600")
app.configure(bg="#2d2d2d")

tk.Label(app, text="KAM IDE 💻", font=("Arial", 16, "bold"), bg="#2d2d2d", fg="white").pack(pady=10)

# Code Editor text box
text_editor = tk.Text(app, font=("Consolas", 14), height=16, width=55, bg="#1e1e1e", fg="#56db3a", insertbackground="white")
text_editor.pack(pady=10)

# Sample code covering all requirements including the new updates
sample_code = '''create bool is_passed;
is_passed = true;

create array numbers;
numbers = [10, 20, 30];
numbers[1] = 50;

create int arr_size;
arr_size = length(numbers);

repeat (x < arr_size) {
    x = x + 1;
}

if (is_passed == true) {
    create string msg;
    msg = "Hello Data Scientist";
}

function calc(int a, bool flag) {
    create int result;
    result = a + 10;
}

call calc(5, false);
'''
text_editor.insert(tk.END, sample_code)

# Run button
compile_btn = tk.Button(app, text="▶ Compile Code", bg="#007acc", fg="white", font=("Arial", 14, "bold"), command=compile_code)
compile_btn.pack(pady=10)

app.mainloop()