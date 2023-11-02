def bearbeite_programm(programm, eingabe):
    position = 0
    ausgabe = []
    while True:
        instruktion = programm[position]
        opcode, modus1, modus2, modus3 = instruktion % 100, (instruktion // 100) % 10, (instruktion // 1000) % 10, (instruktion // 10000) % 10

        if opcode == 1:  # Addition
            param1 = programm[position + 1] if modus1 == 1 else programm[programm[position + 1]]
            param2 = programm[position + 2] if modus2 == 1 else programm[programm[position + 2]]
            programm[programm[position + 3]] = param1 + param2
            position += 4
        elif opcode == 2:  # Multiplikation
            param1 = programm[position + 1] if modus1 == 1 else programm[programm[position + 1]]
            param2 = programm[position + 2] if modus2 == 1 else programm[programm[position + 2]]
            programm[programm[position + 3]] = param1 * param2
            position += 4
        elif opcode == 3:  # Eingabe
            programm[programm[position + 1]] = eingabe
            position += 2
        elif opcode == 4:  # Ausgabe
            ausgabe.append(programm[programm[position + 1]] if modus1 == 0 else programm[position + 1])
            position += 2
        elif opcode == 5:  # jump-Befehl, wenn wahr
            param1 = programm[position + 1] if modus1 == 1 else programm[programm[position + 1]]
            param2 = programm[position + 2] if modus2 == 1 else programm[programm[position + 2]]
            if param1 != 0:
                position = param2
            else:
                position += 3
        elif opcode == 6:  # jump-Befehl, wenn falsch
            param1 = programm[position + 1] if modus1 == 1 else programm[programm[position + 1]]
            param2 = programm[position + 2] if modus2 == 1 else programm[programm[position + 2]]
            if param1 == 0:
                position = param2
            else:
                position += 3
        elif opcode == 7:  # Kleiner als
            param1 = programm[position + 1] if modus1 == 1 else programm[programm[position + 1]]
            param2 = programm[position + 2] if modus2 == 1 else programm[programm[position + 2]]
            programm[programm[position + 3]] = 1 if param1 < param2 else 0
            position += 4
        elif opcode == 8:  # Gleich
            param1 = programm[position + 1] if modus1 == 1 else programm[programm[position + 1]]
            param2 = programm[position + 2] if modus2 == 1 else programm[programm[position + 2]]
            programm[programm[position + 3]] = 1 if param1 == param2 else 0
            position += 4
        elif opcode == 99:  # Beenden
            break
        else:
            raise ValueError("Ungültiger Opcode")

    return ausgabe

# Beispiel-Eingabe und Ausführung des Programms
programm = [int(x) for x in input("Geben Sie das Programm als Liste von Zahlen ein: ").split(",")]
eingabe = int(input("Geben Sie die Eingabe (z.B. 5) ein: ")

ausgabe = bearbeite_programm(programm, eingabe)
print("Ausgabe:", ausgabe)
