

print("hello world")

sample_data = ["TUPC-18-0516", "EDELLON", "JY", "BET-COET-C", "5514"]

key=["TUPC", "BET"]

for student_info in sample_data:
    for keyword in key:
        if keyword in student_info:
            print(student_info)
            break