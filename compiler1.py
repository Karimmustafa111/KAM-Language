import tkinter as tk
from tkinter import messagebox
from lark import Lark, exceptions
from lark.visitors import Interpreter

# 1. Grammar Syntax 
k_lang_grammar = """
start: statement+

?statement: declaration ";" | assignment ";" | condition | loop | method_decl | method_call ";"

declaration: "create" TYPE CNAME
TYPE: "int" | "float" | "string" | "array" | "bool"

assignment: CNAME "=" expression -> assign_var
          | CNAME "[" expression "]" "=" expression -> assign_array

condition: "if" "(" cond_expr ")" block ("else" block)?
loop: "repeat" "(" cond_expr ")" block
method_decl: "function" CNAME "(" param_list? ")" block
block: "{" statement+ "}"

param_list: TYPE CNAME ("," TYPE CNAME)*
method_call: "call" CNAME "(" arg_list? ")"
arg_list: expression ("," expression)*

?cond_expr: expression OP expression
OP: ">" | "<" | "==" | "!=" | ">=" | "<="

expression: term (ADD_OP term)*
term: factor (MUL_OP factor)*
ADD_OP: "+" | "-"
MUL_OP: "*" | "/"

?factor: CNAME -> var | SIGNED_NUMBER -> number | ESCAPED_STRING -> string
       | "true" -> true_val | "false" -> false_val | CNAME "[" expression "]" -> array_access
       | "length" "(" CNAME ")" -> array_length | "(" expression ")" | "[" arg_list? "]" -> array_literal

%import common.CNAME
%import common.SIGNED_NUMBER
%import common.ESCAPED_STRING
%import common.WS
%ignore WS
"""

parser = Lark(k_lang_grammar, parser='lalr')

# 2. Semantics Engine
class KLangEngine(Interpreter):
    def __init__(self, console_fn):
        self.memory = {}  # RAM
        self.print_out = console_fn

    def start(self, tree): [self.visit(c) for c in tree.children]
    def block(self, tree): [self.visit(c) for c in tree.children]

    # Memory
    def declaration(self, tree): self.memory[tree.children[1].value] = None
    def assign_var(self, tree): self.memory[tree.children[0].value] = self.visit(tree.children[1])
    def assign_array(self, tree): self.memory[tree.children[0].value][int(self.visit(tree.children[1]))] = self.visit(tree.children[2])
    def var(self, tree): return self.memory.get(tree.children[0].value, 0)

    # Values
    def number(self, tree): return float(tree.children[0]) if '.' in tree.children[0] else int(tree.children[0])
    def string(self, tree): return tree.children[0][1:-1]
    def true_val(self, tree): return True
    def false_val(self, tree): return False
    def array_literal(self, tree): return self.visit(tree.children[0]) if tree.children else []
    def arg_list(self, tree): return [self.visit(c) for c in tree.children]
    def array_access(self, tree): return self.memory[tree.children[0].value][int(self.visit(tree.children[1]))]
    def array_length(self, tree): return len(self.memory[tree.children[0].value])

    # Math
    def expression(self, tree):
        res = self.visit(tree.children[0])
        for i in range(1, len(tree.children), 2):
            op, nxt = tree.children[i], self.visit(tree.children[i+1])
            res = res + nxt if op == '+' else res - nxt
        return res

    def term(self, tree):
        res = self.visit(tree.children[0])
        for i in range(1, len(tree.children), 2):
            op, nxt = tree.children[i], self.visit(tree.children[i+1])
            res = res * nxt if op == '*' else res / nxt
        return res

    # Logic
    def cond_expr(self, tree):
        l, op, r = self.visit(tree.children[0]), tree.children[1], self.visit(tree.children[2])
        if op == '>': return l > r
        if op == '<': return l < r
        if op == '==': return l == r
        if op == '!=': return l != r
        if op == '>=': return l >= r
        return l <= r

    def condition(self, tree):
        if self.visit(tree.children[0]): self.visit(tree.children[1])
        elif len(tree.children) > 2: self.visit(tree.children[2])

    def loop(self, tree):
        while self.visit(tree.children[0]): self.visit(tree.children[1])

    # Functions
    def method_decl(self, tree): self.memory[tree.children[0].value] = tree
    def method_call(self, tree):
        name = tree.children[0].value
        args = self.visit(tree.children[1]) if len(tree.children) > 1 and tree.children[1] else []
        if name == "print":
            self.print_out(" ".join(str(a) for a in args) + "\n")
        elif name in self.memory:
            self.visit(self.memory[name].children[-1])

# 3. UI Application 
def print_to_console(text):
    console_output.config(state=tk.NORMAL)
    console_output.insert(tk.END, text)
    console_output.config(state=tk.DISABLED)
    console_output.see(tk.END)

def compile_and_run():
    code = text_editor.get("1.0", tk.END)
    console_output.config(state=tk.NORMAL)
    console_output.delete("1.0", tk.END)
    console_output.config(state=tk.DISABLED)
    try:
        tree = parser.parse(code)
        print_to_console("--- Execution Started ---\n")
        engine = KLangEngine(print_to_console)
        engine.visit(tree)
        print_to_console("--- Execution Finished ---\n")
        messagebox.showinfo("Success", "Code Compiled & Executed Successfully!")
    except exceptions.UnexpectedInput as e:
        messagebox.showerror("Syntax Error", f"Compilation Failed:\n\n{e.get_context(code)}")
    except Exception as e:
        messagebox.showerror("Runtime Error", f"Execution Failed:\n\n{str(e)}")

app = tk.Tk()
app.title("KAM Compiler & Interpreter")
app.geometry("700x750")
app.configure(bg="#2d2d2d")

tk.Label(app, text="KAM IDE 💻", font=("Arial", 16, "bold"), bg="#2d2d2d", fg="white").pack(pady=10)
text_editor = tk.Text(app, font=("Consolas", 14), height=14, width=60, bg="#1e1e1e", fg="#56db3a", insertbackground="white")
text_editor.pack(pady=5)

sample_code = '''create array degrees;
degrees = [10, 20, 30];

create int counter;
counter = 0;

call print("Printing Array Elements:");

repeat (counter < length(degrees)) {
    call print("Element =", degrees[counter]);
    counter = counter + 1;
}

create bool passed;
passed = true;

if (passed == true) {
    call print("Evaluation Passed Successfully!");
}
'''
text_editor.insert(tk.END, sample_code)

compile_btn = tk.Button(app, text="▶ Compile & Run", bg="#007acc", fg="white", font=("Arial", 14, "bold"), command=compile_and_run)
compile_btn.pack(pady=10)

tk.Label(app, text="Output Console", font=("Arial", 12), bg="#2d2d2d", fg="#aaaaaa").pack()
console_output = tk.Text(app, font=("Consolas", 12), height=8, width=60, bg="#000000", fg="#ffffff", state=tk.DISABLED)
console_output.pack(pady=5)

app.mainloop()