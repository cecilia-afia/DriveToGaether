# Commencer à developper avec Arduino IDE

 - Téléchargez la [dernière version de l'IDE Arduino](https://www.arduino.cc/en/software) (site officiel Arduino).  
   Sous Linux :
   - Téléchargez l'IDE en format *AppImage*,
   - Changez les droits d'exécution du fichier `.AppImage`,
   - Exécutez le fichier `.AppImage` ⇾ L'IDE doit s'afficher,
 - Ouvrez le *sketch* (fichier `.ino` utilisé par Cecilia),
 - Ajoutez la bibliothèque Makeblock-libraries:
   - Téléchargez [la bibliothèque Makeblock-libraries](https://github.com/Makeblock-official/Makeblock-Libraries/archive/refs/heads/master.zip) depuis le Github de Makeblock (lien direct),
   - Ajoutez la bibliothèque au projet : `Menu Sketch > Include Library > Add ZIP Library...`  
     Et sélectionnez le fichier `Makeblock-Libraries-master.zip` précédemment téléchargé.
 - Sélectionnez la carte correspondant au mBot (*Arduino UNO*):  
   `Menu Tools > Boards > Arduino AVR Boards > Arduino UNO`
 - Sélectionnez le port sur lequel est branché sur mBot (`ttyUSB0` si le robot est branché *via* USB):  
   `Menu Tools > Port > ttyUSB0`
 - Développement :
   - **Pour compiler** : cliquez sur l'icone « Checkmark »,
   - **Pour mettre à jour le robot** : cliquez sur l'icone « Flèche »,
 - Plus d'informations sur [l'installation Linux](https://docs.arduino.cc/software/ide-v2/tutorials/getting-started/ide-v2-downloading-and-installing#linux) sont disponible dans la documentation Makeblock.

# Utiliser `arduino-cli` (avancé)

Le programme en ligne de commande `arduino-cli` permet de compiler et de mettre à jour le mBot depuis le Raspberry Pi.

Les instructions ci-dessous résument les étapes à suivre pour installer le logiciel, puis compiler et déployer un programme sur l'Arduino du mBot depuis le Pi.

## Installation de `arduino-cli`

Téléchargement et installation de `arduino-cli` (note : l'installeur s'adapte à la plateforme, PC ou Raspberry Pi).
```
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=~/.local/bin sh
```
Suite à l'installation, pensez à mettre à jour le `PATH` utilisateur pour inclure `~/.local/bin`.

Ajout des biliothèques standards pour développer avec Arduino UNO (utilisé sur mBot).
```
arduino-cli core install arduino:avr
```
Creation d'un fichier de configuration par défaut pour `arduino-cli` et autorisation des installations de bibliothèques tierces (pour installer la bibliothèques Makeblock).
```
sudo apt install yq
arduino-cli config init
yq -i --yaml-output '.library.enable_unsafe_install = true' ~/.arduino15/arduino-cli.yaml
```
Téléchargement et installation de la bibliothèque Makeblock.
```
arduino-cli lib install --git-url https://github.com/Makeblock-official/Makeblock-Libraries.git
```

## Compilation du program et mise à jour du robot

**Les commandes de compilation et de mise à jour sont exécutées depuis le dossier contenant le fichier `.ino`**.

Compilation du programme:
```
arduino-cli compile --fqbn arduino:avr:uno
```

Mise à jour du robot, connecté ici au port `/dev/ttyUSB0`:
```
arduino-cli upload --fqbn arduino:avr:uno --port /dev/ttyUSB0
```
