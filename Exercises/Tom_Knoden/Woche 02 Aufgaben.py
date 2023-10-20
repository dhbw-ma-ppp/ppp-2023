def bearbeite_programm(programm):
    position = 0
    while True:
        aktion = programm[position]
        if aktion == 1:
            wert1 = programm[programm[position + 1]]
            wert2 = programm[programm[position + 2]]
            programm[programm[position + 3]] = wert1 + wert2
            position += 4
        elif aktion == 2:
            wert1 = programm[programm[position + 1]]
            wert2 = programm[programm[position + 2]]
            programm[programm[position + 3]] = wert1 * wert2
            position += 4
        elif aktion == 99:
            break
        else:
            raise ValueError("Ungültige Aktion")
    return programm[0]

print(bearbeite_programm([1, 0, 0, 0, 99]))
print(bearbeite_programm([1, 1, 1, 4, 99, 5, 6, 0, 99]))
befehlsliste = [1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 9, 19, 1, 5, 19, 23, 1, 6, 23, 27, 1, 27, 10, 31, 1, 31, 5, 35, 2, 10, 35, 39, 1, 9, 39, 43, 1, 43, 5, 47, 1, 47, 6, 51, 2, 51, 6, 55, 1, 13, 55, 59, 2, 6, 59, 63, 1, 63, 5, 67, 2, 10, 67, 71, 1, 9, 71, 75, 1, 75, 13, 79, 1, 10, 79, 83, 2, 83, 13, 87, 1, 87, 6, 91, 1, 5, 91, 95, 2, 95, 9, 99, 1, 5, 99, 103, 1, 103, 6, 107, 2, 107, 13, 111, 1, 111, 10, 115, 2, 10, 115, 119, 1, 9, 119, 123, 1, 123, 9, 127, 1, 13, 127, 131, 2, 10, 131, 135, 1, 135, 5, 139, 1, 2, 139, 143, 1, 143, 5, 0, 99, 2, 0, 14, 0))

def verarbeite_eingabe(eingabe_argumente):
    zahlen = []
    zeichen = []
    for arg in eingabe_argumente:
        if arg.isdigit():
            zahlen.append(int(arg))
        elif len(arg) == 1 and arg.isalpha():
            zeichen.append(arg)
    return zahlen, zeichen

print(verarbeite_eingabe("123", "A", "B", "45", "C", "D", "E", "F", "2"))
print(verarbeite_eingabe("7", "X", "9", "Y", "Z"))
print(verarbeite_eingabe("Hallo", "Welt", "1", "2", "3", "A", "B", "C"))
