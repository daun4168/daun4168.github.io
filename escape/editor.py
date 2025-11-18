from pyscript import document

# Grab the editor script reference.
editor = document.querySelector('#editor')

# Output the live content of the editor.
print(editor.code)

# Update the live content of the editor.
editor.code = """
a = 1
b = 2
print(a + b)
"""

# Evaluate the live code in the editor.
# This could be any arbitrary code to evaluate in the editor's Python context.
editor.process(editor.code)
