#Global Variables
print("example 1") 
x = "awesome"

def func():
  print("Python is " + x)

func()

print(" ")
print("example 2")
x = "awesome"

def func():
  x = "fantastic"
  print("Python is " + x)

func()

print("Python is " + x)

print(" ")
print("example 3")
def func():
  global x
  x = "fantastic"

func()

print("Python is " + x)

print(" ")
print("example 4")
x = "awesome"

def func():
  global x
  x = "fantastic"

func()

print("Python is " + x)