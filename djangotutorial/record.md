from djangotutorial.polls.models import QuestionAction > Résultat attendu > Résultat obtenu

2.2.1.3 :
Visualisez le résultat de vos saisies dans l'interface d'admin.
    o Voyez-vous tous les attributs de vos classes ?
    o Pouvez-vous filtrer vos données suivants tous les attributs ?
    o Pouvez-vous trier vos données suivants tous les attributs ?
    o Pouvez-vous chercher un contenu parmi tous les champs ?
- L'interface admin est limité et ne permet pas le filtrage.


2.2.1.5 :
Ajouter un nouvel utilisateur sans permissions.
    - Résultat attendu : Création d'un utilisateur simple et s'y connecter.
    - Résultat obtenu : Impossible de se connecter


2.2.1.6 :
Ajouter le statut d'équipe à l'utilisateur.
    - Résultat : Connection à l'interface sans permissions préalables.


2.2.1.7 :
Supprimer l'utilisateur de l'organisation.
    - Résultat : Impossible de se connecter.


## [Exercice Shell]
### 1. Lister les questions sur plusieurs lignes :
```python
for question in enumerate(Question.objects.all()):
    print(question)
"""(0, <Question: What's up?>)
(1, <Question: Do you like me?>)"""
```

### 2. Ajouter un filtre sur la date de publication :
```python
import datetime
from django.utils import timezone
time_filter = timezone.now() - datetime.timedelta(days=1)
for question in enumerate(Question.objects.filter(published_date__year=timezone.now().year)):
    print(question)
"(0, <Question: What's up?>)"
```

### 3. Trouver une question par son id et afficher ses valeurs :
```python
import datetime
from django.utils import timezone
q = Question.objects.get(id=2)
print(q.published_date.date(), q.choice_set.all())
"2026-02-23 <QuerySet [<Choice: Yes.>, <Choice: Absolutely!>, <Choice: Definitely!>]>"
```

### 4. Boucler sur toutes les questions et afficher leurs valeurs :
```python
import datetime
from django.utils import timezone
for i, q in enumerate(Question.objects.all()):
    print(q.question_text, q.published_date.date())
    for choice in Choice.objects.filter(question=q):
        print(choice.choice_text)
"""What's up? 2026-02-23
My disappointment is immeasurable, and my day is ruined.
I'm doing fine.
Amazing!
Do you like me? 2026-02-23
Yes.
Absolutely!
Definitely!"""
```

### 5. Afficher le nombre de choix pour chaque question :
```python
for q in Question.objects.all():
    print(q.question_text, q.choice_set.all().count());
"""What's up? 3
Do you like me? 3"""
```

### 7. Trier les questions par order antéchronologique :
```python
for q in Question.objects.all().order_by("-published_date"):
    print(q.question_text);
"""Do you like me?
What's up?"""
```

### 9. Créer une question à partir du Shell :
```python
Question(question_text="", published_date=timezone.now())
```

### 10. Ajouter des choix à partir du Shell :
```python
q = Question.objects.get(id=1)
q.choice_set.create(choice_text="I don't know.", votes=0)
q.choice_set.create(choice_text="Better than you.", votes=0)
q.choice_set.create(choice_text=":c", votes=0)
```

### 11. Listez les questions publiées récemment :
```python
Question.objects.filter(published_date__gte=timezone.now() - datetime.timedelta(days=1))
"<QuerySet [<Question: What's up?>, <Question: Do you like me?>]"
```