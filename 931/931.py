from abc import ABC, abstractmethod

class Student:
    def __init__(self, program, required_credits, money):
        self.program = program.strip()
        self.required_credits = int(required_credits)
        self.money = int(money)
        self.credits = 0
        self.expelled = False
    def accept(self, visitor):
        if not self.expelled:
            visitor.visit(self)
    def __str__(self):
        return f"{self.program}  C:{self.credits}/{self.required_credits}  $:{self.money}"
    def can_learn(self, subject_type):
        if self.program == "mixed":
            return True
        return self.program == subject_type

class Visitor(ABC):
    @abstractmethod
    def visit(self, student):
        pass

class TeachVisitor(Visitor):
    def __init__(self, subject_type, credits):
        self.subject_type = subject_type.strip()
        self.credits = int(credits)
    def visit(self, student):
        if student.can_learn(self.subject_type):
            student.credits += self.credits
            print(f"TEACH ✓ +{self.credits} credits")
        else:
            print("TEACH ✗ incompatible")

class PayHostelVisitor(Visitor):
    def __init__(self, amount):
        self.amount = int(amount)
    def visit(self, student):
        if student.money >= self.amount:
            student.money -= self.amount
            print(f"HOSTEL -{self.amount}")
        else:
            student.expelled = True
            print("HOSTEL ✗ expelled")

class PayCanteenVisitor(Visitor):
    def __init__(self, amount):
        self.amount = int(amount)
    def visit(self, student):
        if student.money >= self.amount:
            student.money -= self.amount
            print(f"CANTEEN -{self.amount}")
        else:
            student.expelled = True
            print("CANTEEN ✗ expelled")

class ScholarshipVisitor(Visitor):
    def __init__(self, amount):
        self.amount = int(amount)
    def visit(self, student):
        student.money += self.amount
        print(f"SCHOLARSHIP +{self.amount}")

class HelpVisitor(Visitor):
    def __init__(self, amount):
        self.amount = int(amount)
    def visit(self, student):
        student.money += self.amount
        print(f"HELP +{self.amount}")

def read(line):
    p = line.split()
    if not p:
        return None
    if p[0] == "teach":
        return TeachVisitor(p[1], p[2])
    if p[0] == "pay" and p[1] == "hostel":
        return PayHostelVisitor(p[2])
    if p[0] == "pay" and p[1] == "canteen":
        return PayCanteenVisitor(p[2])
    if p[0] == "obtain" and p[1] == "scholarship":
        return ScholarshipVisitor(p[2])
    if p[0] == "obtain" and p[1] == "help":
        return HelpVisitor(p[2])
    return None

def run_file(filename):
    print("\n" + "=" * 45)
    print(filename)
    print("=" * 45)
    with open(filename, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    student = Student(lines[0], lines[1], lines[2])
    for line in lines[3:]:
        visitor = read(line)
        if visitor:
            visitor.visit(student)
        print(" ", line)
        print(" ", student)
        if student.expelled:
            print(">>> EXPELLED")
            break
    print("\nRESULT:", end=" ")
    if not student.expelled and student.credits >= student.required_credits:
        print("DIPLOMA ✓")
    else:
        print("NO DIPLOMA ✗")

if __name__ == "__main__":
    run_file("input01.txt")
    # run_file("input02.txt")
