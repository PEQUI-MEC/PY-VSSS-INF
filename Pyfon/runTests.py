import os

#os.system("ls -l")
print("Testing Communication...\n")
os.system("python -m unittest discover -s test/testCommunication -v")

print("\nTesting Control...\n")
os.system("python -m unittest discover -s test/testControl -v")

print("\nTesting Manager...\n")
os.system("python -m unittest discover -s test/testHades -v")

print("\nTesting Vision...\n")
os.system("python -m unittest discover -s test/testVision -v")

print("\nTesting Interface...\n")
os.system("python -m unittest discover -s test/testInterface -v")