# API Choice

- Étudiant : Ré-anh Jondeau
- API choisie : Frankfurter
- URL base : https://api.frankfurter.app
- Documentation officielle / README : https://frankfurter.dev/
- Auth : None / aucune clé API

## Endpoints testés

- GET /latest?from=EUR
- GET /latest?from=EUR&to=USD
- GET /latest?from=EUR&to=GBP

## Contrat de l'API

La requête principale utilisée est :

GET /latest?from=EUR

La réponse est au format JSON et contient notamment :

- `amount` : nombre
- `base` : chaîne de caractères représentant la devise de base
- `date` : chaîne représentant la date
- `rates` : objet contenant les taux de change

Exemple :

{
  "amount": 1,
  "base": "EUR",
  "date": "2026-09-22",
  "rates": {
    "USD": 1.17,
    "GBP": 0.87
  }
}

## Tests prévus

1. Vérifier que la requête principale retourne HTTP 200.
2. Vérifier que la réponse est au format JSON.
3. Vérifier la présence des champs `amount`, `base`, `date` et `rates`.
4. Vérifier les types des données retournées.
5. Vérifier le filtrage sur une devise comme USD.
6. Vérifier la gestion d'une devise invalide.

## Limites / rate limiting connu

L'API publique ne nécessite pas de clé API et n'impose pas de quota quotidien ou mensuel. Elle applique cependant une limitation destinée à empêcher les abus.

## Risques

- Indisponibilité temporaire de l'API.
- Modification ou retard de publication des taux.
- Les taux correspondent aux dernières données disponibles et peuvent évoluer lors des mises à jour.

## Source

https://frankfurter.dev/
