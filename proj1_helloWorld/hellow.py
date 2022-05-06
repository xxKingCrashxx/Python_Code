

def main():
    isEligible = bool() 
    name = input("what is your name?\n")
    age = int(input("what is your age\n"))

    print(f"hello {name}")
    
    if(age >= 18):
        isEligible = True
        
    if(isEligible):
        print("you are an adult, you are eligible to vote")
        return

    print(f"Sorry you cannot vote yet, you have {(18 - age)} more years until you can vote.")

main()

