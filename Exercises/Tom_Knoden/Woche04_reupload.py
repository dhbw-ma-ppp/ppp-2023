def bearbeite_programm(programm, inputs):
    position = 0
    ausgabe = []
    input_index = 0

    while True:
        instruktion = programm[position]
        opcode, modus1, modus2, modus3 = instruktion % 100, (instruktion // 100) % 10, (instruktion // 1000) % 10, (instruktion // 10000) % 10

        if opcode == 1:  # Addition
            # ... (unchanged)
        elif opcode == 2:  # Multiplikation
            # ... (unchanged)
        elif opcode == 3:  # Eingabe
            programm[programm[position + 1]] = inputs[input_index]
            input_index += 1
            position += 2
        elif opcode == 4:  # Ausgabe
            print(programm[programm[position + 1]] if modus1 == 0 else programm[position + 1])
            position += 2
        # ... (rest of the code, unchanged)

# Beispiel-Eingabe und Ausführung des Programms
programm = [int(x) for x in input("Geben Sie das Programm als Liste von Zahlen ein: ").split(",")]
eingabe = int(input("Geben Sie die Eingabe (z.B. 5) ein: "))
ausgabe = bearbeite_programm(programm, [eingabe])
