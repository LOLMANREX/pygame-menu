score = 0
while True:
    print ("\n---MENU---")
    print ("1 - Gagner des points ")
    print ("2 - Voir le score")
    print ("3 - Quitter")
    
    choix = input("Ton choix : ")
    if choix == "1":
        score =score+1    
        print("🔥 +1 point")

    elif choix == "2":
        print("⭐ Ton score est :", score)

    elif choix == "3":
        print("👋 Fin du jeu, score final :", score)
        break

    else :
        print("❌ Choix invalide")
