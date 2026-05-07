# KAM-Language
A custom programming language compiler and interpreter built with Python and Lark.

# K-Lang Compiler & Interpreter 🚀

A complete custom programming language compiler and interpreter, built from scratch using **Python** and the **Lark** parsing library.

## 📌 Project Overview
This project demonstrates the full pipeline of language processing, from lexical analysis to semantic execution, wrapped in a custom IDE built with Tkinter.

## 📂 Files Included

### 1. `compiler1.py` (The Full Engine)
This is the main file containing both **Syntax Analysis** and **Semantic Execution**. 
* **Parser:** Builds the Abstract Syntax Tree (AST).
* **Interpreter:** Executes the AST using the Visitor Pattern.
* **Features:** Memory management (Symbol Table), arithmetic evaluations, variable declarations, loops, conditionals, and built-in function execution (e.g., `print`).

### 2. `compiler2.py` (Syntax Analyzer)
This file represents the first phase of the evaluation. It contains the Context-Free Grammar (CFG) and the LALR parser to validate the syntax of the language and generate the Parse Tree, without semantic execution.

## 🛠️ Technologies Used
* **Language:** Python 3
* **Parsing Library:** Lark (LALR Parser)
* **GUI:** Tkinter
