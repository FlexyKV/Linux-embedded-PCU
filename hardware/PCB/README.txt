Les plans prototypes correspondent aux circuits actuellement utilisés dans le prototype. 

Les plans "modifiés" comprennent une série de modifications visant à améliorer le prototype:
- Changement des header entre les pcbs pour des 2x4 plutot que 1x8
- Retrait d'un bon nombre de jumper uniquement présents pour des tests
- Les fusibles et Varistors sont placés dans la bonne séquence afin de proteger le circuit


Changement non testé:
- Ajout d'un circuit permettant de faire une référence à 5V à partir du PSU 12V
- Ajout d'un bridge permettant de deconnecté le 5V du RPI aux autres 5V du circuit si celui-ci
est alimenté par son bloc mural.