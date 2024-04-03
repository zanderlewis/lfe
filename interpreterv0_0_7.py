import re
import os
import sys
import subprocess

is_python_ibrary = False

class Markup:
    def __init__(self, text):
        self.text = text
        self.html = ""
        self.php = ""
        self.php_file = ""
        self.php_file_name = ""
        self.theme = "light"

    def compile(self):
        self.compile_html()
        self.compile_php()

    def compile_html(self):
        self.html = self.text
        theme_used = False
        if re.search(r'::theme-preset{(light)}', self.html):
            self.html = re.sub(r'::theme-preset{(light)}', r'<div class="theme-light">', self.html)
            theme_used = True
            self.theme = "light"
        if re.search(r'::theme-preset{(dark)}', self.html):
            self.html = re.sub(r'::theme-preset{(dark)}', r'<div class="theme-dark">', self.html)
            theme_used = True
            self.theme = "dark"
        if re.search(r'::theme-preset{(system)}', self.html):
            self.html = re.sub(r'::theme-preset{(system)}', r'<div class="theme-system">', self.html)
            theme_used = True
            self.theme = "system"
        self.html = re.sub(r'###### (.*?)\n', r'<h6>\1</h6>', self.html)
        self.html = re.sub(r'##### (.*?)\n', r'<h5>\1</h5>', self.html)
        self.html = re.sub(r'#### (.*?)\n', r'<h4>\1</h4>', self.html)
        self.html = re.sub(r'### (.*?)\n', r'<h3>\1</h3>', self.html)
        self.html = re.sub(r'## (.*?)\n', r'<h2>\1</h2>', self.html)
        self.html = re.sub(r'# (.*?)\n', r'<h1>\1</h1>', self.html)
        self.html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', self.html)
        self.html = re.sub(r'\*(.*?)\*', r'<i>\1</i>', self.html)
        self.html = re.sub(r'__(.*?)__', r'<u>\1</u>', self.html)
        self.html = re.sub(r'_(.*?)_', r'<i>\1</i>', self.html)
        self.html = re.sub(r'~~(.*?)~~', r'<s>\1</s>', self.html)
        self.html = re.sub(r'`(.*?)`', r'<code>\1</code>', self.html)
        self.html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', self.html)
        self.html = re.sub(r'\n', r'<br>', self.html)
        if theme_used:
            self.html += "</div>"
        return self.html

    def compile_php(self):
        self.php = "<?php\n"
        self.php += "echo <<<EOT\n"
        self.php += "<!DOCTYPE html>\n"
        self.php += "<html>\n"
        self.php += "<head>\n"
        self.php += "<style>\n"
        self.php += "a { color: inherit; font-weight: 700; }\n"
        self.php += ".theme-light { --bg-color: #ffffff; --text-color: #000000; --code-bg-color: #e8e8e8; }\n"
        self.php += ".theme-dark { --bg-color: #1a202c; --text-color: #Cbd5e0; --code-bg-color: #44475a; }\n"
        self.php += ".theme-system { --bg-color: #ffffff; --text-color: #000000; --code-bg-color: #e8e8e8; }\n"
        self.php += "@media (prefers-color-scheme: dark) { .theme-system { --bg-color: #1a202c; --text-color: #Cbd5e0; --code-bg-color: #44475a; } }\n"
        self.php += "body { background-color: var(--bg-color); color: var(--text-color); }\n"
        self.php += "code { background-color: var(--code-bg-color); padding: 0.2em 0.4em; margin: 0; font-size: 85%; border-radius: 6px; }\n"
        self.php += "</style>\n"
        self.php += "</head>\n"
        self.php += "<body " + ("class='theme-" + self.theme + "'" if self.theme else "light") + ">\n"
        self.php += self.html
        self.php += "</body>\n"
        self.php += "</html>\n"
        self.php += "\nEOT;\n"
        self.php += "?>\n"
        return self.php

    def write_php_file(self, file_name):
        self.php_file_name = file_name
        self.php_file = open(file_name, "w")
        self.php_file.write(self.php)
        self.php_file.close()

def read_lfe(file_name):
    file = open(file_name, "r")
    text = file.read()
    file.close()
    return text

class Interpreter:
    def __init__(self, text="", is_in_library=True):  # Add is_in_library parameter
        self.is_in_library = is_in_library  # Store it in an instance variable
        if is_in_library and not text:
            raise ValueError("Text must be provided when in library mode.")
            
        self.text = text
        base_name = "output"
        self.markup = Markup(self.text)
        self.markup.compile()
        php = self.markup.php
        open(base_name + ".php", "w").write(php)
        subprocess.run(["php", base_name + ".php"])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <file_name>")
    else:
        interpreter = Interpreter(sys.argv[1])