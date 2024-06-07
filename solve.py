t = int(input("Введите t: "))
a = []

while len(a) < t * 4:
    for i in range(4):
        a.append(int(input("Введите число: ")))
a1 = [a[:4:]] 
a1.append(a[a.index(a[-4])::])

#Спасибо за день, очень был благодарен!
    
        