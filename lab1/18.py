#Python Strings
print("Hello")
print('Hello')

print (' ')
print("It's alright")
print("He is called 'Johnny'")
print('He is called "Johnny"')

print (' ')
a = "Hello"
print(a)

print (' ')
a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)

print (' ')
a = '''Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua.'''
print(a)

print (' ')
a = "Hello, World!"
print(a[1])

print (' ')
for x in "banana":
  print(x)

print (' ')
a = "Hello, World!"
print(len(a))

print (' ')
txt = "The best things in life are free!"
print("free" in txt)

print (' ')
txt = "The best things in life are free!"
if "free" in txt:
  
  print("Yes, 'free' is present.")

print (' ')
txt = "The best things in life are free!"
print("expensive" not in txt)

print (' ')
txt = "The best things in life are free!"
if "expensive" not in txt:
  print("No, 'expensive' is NOT present.")