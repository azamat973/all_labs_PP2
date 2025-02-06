#the task 1
def grams_to_ounces(grams):
    return 28.3495231 * grams

#the task 4
def filter_prime(numbers):
    def is_prime(num):
        if num <= 1:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    return [num for num in numbers if is_prime(num)]

#the task 9
def sphere_volume(radius):
    return (4/3) * 3.14159 * radius**3
