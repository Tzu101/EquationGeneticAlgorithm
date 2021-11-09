import time
import random


class Equation: # Class for genetic selection

    sign_set = ["+", "-", "*", "/"]

    def __init__(self, numbers, signs):  # Equation constructor

        self.numbers = numbers  # 5 unique numbers
        self.signs = signs      # 4 signs of any allowed type
        self.error = -1         # Fitness variable of the class


    def evaluate(self):  # Calculates the value of the equation

        resoult = 0                 # Final resoult
        numbers = self.numbers.copy()  # Work copy
        signs = self.signs.copy()   # Work copy
        
        first_order = True
        while first_order:  # Multiplication and division

            first_order = False
            for s in range(len(signs)):

                first_order = False

                if signs[s] == "*":  # Calculate 1 step of multiplication
                    mul = numbers[s] * numbers[s+1]
                    numbers[s] = mul
                    numbers.pop(s+1)
                    signs.pop(s)
                    first_order = True
                    break

                elif signs[s] == "/":  # Calculate 1 step of division
                    if numbers[s+1] == 0:
                        return 999999999999999
                    div = numbers[s] / numbers[s+1]
                    numbers[s] = div
                    numbers.pop(s+1)
                    signs.pop(s)
                    first_order = True
                    break
        	
        resoult += numbers[0]
        for s in range(len(signs)):  # Addition and subtraction

            if signs[s] == "+":  # Add
                resoult += numbers[s+1]

            elif signs[s] == "-":  # Subtract
                resoult -= numbers[s+1]

        return resoult

    
    def mutate(self, chance):  # Mutates the current equation
        
        if random.randint(0, 99) < chance:  # Only mutates by chance

            if random.randint(0, 1) == 0:  # Swaps two numbers

                num1 = random.randint(0, len(self.numbers)-1)
                num2 = random.randint(0, len(self.numbers)-1)

                self.numbers[num1], self.numbers[num2] = self.numbers[num2], self.numbers[num1]

            else:  # Changes a sign
                
                signs = Equation.sign_set
                sign1 = random.randint(0, len(self.signs)-1)
                sign2 = random.randint(0, len(signs)-1)

                self.signs[sign1] = signs[sign2]
        

    def crossover(self, equation):  # Returns a new equation thats a mix between it and the one given

        '''number_split1 = len(self.numbers) // 4
        number_split2 = len(self.numbers) - 2*number_split1

        new_numbers = self.numbers[0 : number_split1]
        added_num = 0
        for n in equation.numbers:
            if n not in new_numbers:
                new_numbers.append(n)
                added_num += 1
                if added_num == number_split2:
                    break
        
        for n in self.numbers:
            if n not in new_numbers:
                new_numbers.append(n)'''
        
        number_split = len(self.numbers) // 2 + 1
        
        new_numbers = self.numbers[0 : number_split]  # Child numbers
        for n in equation.numbers:
            if n not in new_numbers:
                new_numbers.append(n)

        sign_split = len(self.signs) // 2
        new_signs = self.signs[0 : sign_split] + equation.signs[sign_split: len(self.signs)]  # Child signs

        return Equation(new_numbers, new_signs)


    def __str__(self):  # Turns equation into string representation

        equation = str(self.numbers[0])

        for n in range(1, len(self.numbers)):
            equation += " " + self.signs[n-1]
            equation += " " + str(self.numbers[n])

        equation += " = {:.2f}".format(self.evaluate())

        return equation

    
    def unique_id(self):

        id = self.numbers[-1]
        for i in range(len(self.numbers)-1):
            id += 10**(2*i) * ( self.numbers[i] % 9)
            id += 10**(2*i+1) * ( ord(self.signs[i]) % 9)

        return id


class Equation2(Equation):

    def __init__(self, numbers, signs):  # Equation2 constructor
        Equation.__init__(self, numbers, signs)

        self.length_error = -1
        self.number_dic = {}
        self.build_dic()
       

    def build_dic(self):

        self.number_dic = {}
        for number in self.numbers:
            
            if number in self.number_dic:
                self.number_dic[number] += 1
            else:
                self.number_dic.update({number : 1})


    def mutate(self, chance):  # Mutates the current equation
        
        if random.randint(0, 99) < chance:  # Only mutates by chance

            mutation_type = random.randint(0, 2)

            if mutation_type == 0:  # Swaps two numbers / change number

                num1 = random.randint(0, len(self.numbers)-1)
                num2 = random.randint(0, len(self.numbers)-1)

                self.numbers[num1], self.numbers[num2] = self.numbers[num2], self.numbers[num1]

            elif mutation_type == 1:  # Changes a sign
                
                signs = Equation.sign_set
                sign1 = random.randint(0, len(self.signs)-1)
                sign2 = random.randint(0, len(signs)-1)

                self.signs[sign1] = signs[sign2]

            else:  # Adds / Removes number

                spot = random.randint(0, len(self.signs)-1)  # Place to add / remove new number

                if random.randint(0, 1) == 0:  # Add number

                    number = list(self.number_dic.keys())[random.randint(0, len(self.number_dic.keys()) - 1)]
                    if self.number_dic[number] < 5:
                        self.numbers.insert(spot, number)

                        signs = Equation.sign_set
                        sign = random.randint(0, len(signs)-1)
                        self.signs.insert(spot, signs[sign])

                else:  # Remove number

                    if len(self.signs) == 1:  # Prevents equation becoming to short
                        return

                    number = self.numbers.pop(spot)
                    self.signs.pop(spot)

                self.build_dic()


    def crossover(self, equation):  # Returns a new equation thats a mix between it and the one given
        
        number_split1 = random.randrange(0, len(self.numbers) - 1)
        sign_split1 = number_split1
        number_split2 = random.randrange(0, len(equation.numbers) - 1)
        sign_split2 = number_split2

        numbers = self.numbers[0 : number_split1] + equation.numbers[number_split2 : len(equation.numbers) ]
        signs = self.signs[0 : sign_split1] + equation.signs[sign_split2 : len(equation.signs)]

        if len(numbers) == len(signs):
            signs.pop()

        correct_dir = {}
        for number in range(len(numbers)):  # Builds dictionary
            if numbers[number] in correct_dir:
                correct_dir[numbers[number]] += 1     
            else:
                correct_dir.update({numbers[number] : 1})

        correcting = True
        while correcting:  # Removes numbers that repeat more than 5 times
            for number in range(len(numbers)):

                correcting = False

                if correct_dir[numbers[number]] > 5:
                    correct_dir[numbers[number]] -= 1
                    numbers.pop(number)
                    signs.pop(number)

                    correcting = True
                    break
                    
        return Equation2(numbers, signs) 




def seed_generation(size, numbers, signs):  # Generates a random starting generation
    
    numbers = numbers.copy()
    generation = [None] * size

    for eq in range(size):
        random.shuffle(numbers)  # Randomly sorts the numbers
        
        eq_signs = []
        signs_len = len(signs)
        for _ in range(len(numbers)-1):
            eq_signs.append(signs[ random.randint(0, signs_len-1) ])

        generation[eq] = Equation(numbers.copy(), eq_signs)

    return generation


def seed_generation2(size, numbers, signs):  # Generates a random starting generation
    
    generation = [None] * size

    for eq in range(size):

        numbers5 = numbers * 5
        
        eq_len = random.randint(2, 20)
        eq_signs = []
        eq_numbers = [ numbers5.pop(random.randint(0, len(numbers5)-1)) ]

        for _ in range(1, eq_len):
            n = random.randint(0, len(numbers5)-1)
            eq_numbers.append(numbers5.pop(n))

            s = random.randint(0, len(signs)-1)
            eq_signs.append(signs[s])

        generation[eq] = Equation2(eq_numbers, eq_signs)

    return generation


def sort_generation(generation, solution):  # Orders generation equations by fitness

    for eq in generation:
        eq.error = abs(solution - eq.evaluate())

    generation.sort(key = lambda x: x.error)


def sort_generation2(generation, solution):  # Orders generation equations by fitness

    for eq in generation:
        eq.error = abs(solution - eq.evaluate())
        eq.length_error = eq.error + len(eq.numbers)**2

    generation.sort(key = lambda x: x.length_error)


def next_generation(survivors, children_num, mutation_chance):  # Creates a new generation with crossing previous survivors

    parent1 = 0
    parent2 = 1
    parent_max = len(survivors)-1

    children = []
    while len(children) < children_num:

        #parent1 = random.randrange(0, len(survivors)-1)
        #parent2 = random.randrange(0, len(survivors)-1)

        child1 = survivors[parent1].crossover(survivors[parent2])  # First crossover variant
        child2 = survivors[parent2].crossover(survivors[parent1])  # Second crossover variant
        child1.mutate(mutation_chance)  # Mutates child
        child2.mutate(mutation_chance)  # Mutates child

        unique1 = True
        unique2 = True
        c1_id = child1.unique_id()
        c2_id = child2.unique_id()

        for s in survivors:  # Eliminates children identical to survivors
            s_id = s.unique_id()

            if c1_id == s_id:
                unique1 = False
            if c2_id == s_id:
                unique2 = False
                
        for c in children:  # Eliminates children identical to eachother
            c_id = c.unique_id()

            if c1_id == c_id:
                unique1 = False
            if c2_id == c_id:
                unique2 = False

        if unique1: children.append(child1)  # Adds first child
        if unique2 and len(children) < children_num: children.append(child2)  # Adds second shild if theres room

        if parent2 < parent_max:  # Selects next parents
            parent2 += 1
        else:
            if parent1 < parent_max-1:
                parent1 += 1
                parent2 = parent1 + 1
            else:
                parent1 = 0
                parent2 = 1
            

    return children



'''def random_search():

    number_set = [3, 5, 10, 11, 13, 25, 100]  # Numbers that must make up the solution
    sign_set = ["+", "-", "*", "/"]   # Signs that can make up the solution
    solution = 2512*11+13                   # Soulution for which we need an equation

    start = time.time()

    searching = True
    while(searching):

        random.shuffle(number_set)
        signs = []

        for s in range(len(number_set)-1):
            signs.append(sign_set[random.randint(0, 3)])

        eq = Equation(number_set.copy(), signs)
        if eq.evaluate() == solution:
            searching = False

    return time.time() - start'''



def genetic_search(number_set, solution, generation_size, generation_count, survivor_percentage, mutation_chance, algorithm):

    random.seed(time.time() * 1000)  # Seeds the random number generator

    sign_set = ["+", "-", "*", "/"]   # Signs that can make up the solution

    Equation.sign_set = sign_set  # Setting the usable signs

    if algorithm == 0:
        generate_generation = seed_generation  # Function for generating the first generation
        order_generation = sort_generation     # Fitness function
    else:
        generate_generation = seed_generation2  # Function for generating the first generation
        order_generation = sort_generation2     # Fitness function

    generation_survivors = generation_size * survivor_percentage // 100  # Number of survivors that move to next generation
    generation_survivors = min(generation_survivors, generation_size-1)

    geneartion_num = 0                                                       # Current generation number
    generation = generate_generation(generation_size, number_set, sign_set)  # Starting generation

    best = 999999999999  # Best score

    start = time.time()

    while geneartion_num < generation_count:

        order_generation(generation, solution)

        survivors = generation[0 : generation_survivors]

        children = next_generation(survivors, generation_size - generation_survivors, mutation_chance)

        generation = survivors + children

        if generation[0].error < best:
            best = generation[0].error

            if best == 0:
                break
            print("GEN {:04d}: {}".format(geneartion_num, str(generation[0])))

        geneartion_num += 1

    print()
    print("Generations run: {:d}".format(geneartion_num))
    print("Best equation: {}".format(generation[0]))
    print("Off by: {:.2f}".format(generation[0].error))

    return time.time() - start
    

if __name__ == '__main__':

    number_set = [3, 5, 10, 25, 100]  # Numbers that must make up the solution
    solution = 2512                 # Soulution for which we need an equation
    generation_size = 20
    generation_count = 100
    survivor_percentage = 50
    mutation_chance = 35
    algorithm = 0

    i = input("Command: ")
    if i != "": i = i.split()
    while(i != ""):

        if i[0] == "help":
            print("Available commands:")
            print("\t exit - Closes program")
            print("\t search - Begins genetic search")
            print("\t overview - Lists all variable values")
            print("\t config - Changes variable value")
            print("\t\t set [3 5 10 25... ] - All available numbers")
            print("\t\t solution [ N ] - Solution for which we need an equation")
            print("\t\t size [1 - ...] - Generation size")
            print("\t\t iterations [1 - ...] - Number of generations simulated")
            print("\t\t survivors [0 - 99] - Percentage of top equations that move to the next generation")
            print("\t\t mutation [0 - 100] - Percentage chance of mutation")
            print("\t\t algorithm [0 or 1] - Algorithm type")

        elif i[0] == "config":
            if i[1] == "set":
                number_set = i[2:]
                for n in range(len(number_set)):
                    number_set[n] = int(n)
            elif i[1] == "solution":
                solution = int(i[2])
            elif i[1] == "size":
                generation_size = int(i[2])
            elif i[1] == "iterations":
                generation_count = int(i[2])
            elif i[1] == "survivors":
                survivor_percentage = int(i[2])
            elif i[1] == "mutation":
                mutation_chance = int(i[2])
            elif i[1] == "algorithm":
                algorithm = int(i[2])
            else:
                print("Invalid config option, for information use the help command")

        elif i[0] == "overview":
            print("The current number set is: " + str(number_set))
            print("The current solution is: " + str(solution))
            print("The current generation size is: " + str(generation_size))
            print("The current iteration number is: " + str(generation_count))
            print("The current survivor percentage is: " + str(survivor_percentage))
            print("The current mutation chance is: " + str(mutation_chance))
            print("The current algorithm is: " + str(algorithm))

        elif i[0] == "search":
            print("The search took {:.2f}s".format(genetic_search(number_set, solution, generation_size, generation_count, survivor_percentage, mutation_chance, algorithm)))

        elif i[0] == "exit":
            print("Closing program")
            print()
            break

        else:
            print("Invalid command, for information use the help command")

        print()
        i = input("Command: ")
        if i != "": i = i.split()
