# Simulateur

Simulation du déplacement des agents dans un monde défini par deux fichiers de configuration

## Fichiers de configuration

### terrain.txt
Contient la configuration du terrain, qui doit être rectangulaire, chaque case est encodée en utilisant un entier représentant son type, avec :
```
 {
    '1' : 'droiteHorizontale',
    '2' : 'droiteVerticale',
    '3' : 'intersectionN',
    '4' : 'intersectionE',
    '5' : 'intersectionS',
    '6' : 'intersectionO',
    '7' : 'virageNE',
    '8' : 'virageNO',
    '9' : 'virageSE',
    '10' : 'virageSO'
}
```

### config.txt
Contient le positionnement initiale de chaque agent, victime et hôpital. Ce fichier doit être de même dimension que terrain.txt. Chaque case est encodée comme suit :
```
 {
    '_' : 'case vide',
    'X' : 'mur',
    'P' : 'victime',
    'H' : 'hôpital',
    'R<ID><orientation>' : 'robot/agent'
}
```
Chaque agent est encodé en ajoutant son identifiant (un chiffre) ainsi que son orientation initiale (N, S, E, W)

## Code
### Robot
Est une classe qui représente un robot, avec ses attributs (position dans le monde, orientation actuelle, etc...)

Un Robot possède une méthode ```doAction()``` qui lui permet de choisir aléatoirement une action parmi ```
['drop','take','move','left','right','uturn']``` en donnant la priorité à ```drop``` puis ```take``` si elles sont réalisables.
 
##Simulator
Est une classe qui gère l'évolution du monde ainsi que son affichage.

Simulator contient une méthode ```check_action()``` qui vérifie si action choisie par le Robot est correcte, et lui retourne la même action, sinon ```nop```
