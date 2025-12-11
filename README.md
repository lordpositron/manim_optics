# Manim Optics - Dynamic Optical Ray Tracing

Un package pour Manim permettant de créer des simulations optiques dynamiques avec mise à jour automatique des rayons.

## 🎯 Caractéristiques

- ✅ **Lentilles minces** (convergentes et divergentes) - optique paraxiale
- ✅ **Miroirs plans** avec réflexion spéculaire
- ✅ **Tracé de rayons dynamique** - les rayons se recalculent automatiquement à chaque frame
- ✅ **Architecture extensible** - facile d'ajouter des éléments optiques complexes
- ✅ **Faisceaux de rayons** et rayons principaux

## 📦 Structure du package

```
manim-optics/
├── __init__.py              # Exports et métadonnées
├── optical_elements.py      # Classes de base et éléments optiques
│   ├── OpticalElement       # Classe abstraite
│   ├── ThinLens            # Lentille mince (base)
│   ├── ConvergingLens      # Lentille convergente
│   ├── DivergingLens       # Lentille divergente
│   ├── Mirror              # Miroir (base)
│   └── PlaneMirror         # Miroir plan
├── rays.py                  # Système de rayons dynamiques
│   ├── DynamicRay          # Rayon avec updaters automatiques
│   ├── RayBundle           # Faisceau de rayons parallèles
│   └── PrincipalRays       # Trois rayons principaux
└── scene_utils.py          # Utilitaires pour les scènes
    ├── OpticalScene        # Scene avec helpers optiques
    └── Helper functions    # Création d'objets, calculs, etc.
```

## 🚀 Utilisation

### Exemple 1 : Lentille convergente basique

```python
from manim import *
from manim_optics import *

class MyOpticsScene(OpticalScene):
    def construct(self):
        # Ajouter un axe optique
        self.setup_optical_axis()
        
        # Créer une lentille convergente
        lens = ConvergingLens(focal_length=2.0, height=3.0)
        self.add(lens)
        
        # Créer un faisceau de rayons parallèles
        bundle = create_parallel_bundle(
            num_rays=5,
            spacing=0.5,
            start_x=-5.0,
            optical_elements=[lens],
            color=YELLOW,
        )
        self.add(bundle)
        
        self.wait(2)
```

### Exemple 2 : Animation dynamique

```python
class DynamicLens(OpticalScene):
    def construct(self):
        self.setup_optical_axis()
        
        lens = ConvergingLens(focal_length=2.5)
        bundle = create_parallel_bundle(
            num_rays=7,
            optical_elements=[lens],
            color=RED,
        )
        
        self.add(lens, bundle)
        
        # 🎨 Magie : les rayons suivent automatiquement !
        self.play(lens.animate.shift(RIGHT * 2), run_time=3)
```

### Exemple 3 : Lentille + Miroir

```python
class LensAndMirror(OpticalScene):
    def construct(self):
        self.setup_optical_axis()
        
        lens = ConvergingLens(focal_length=2.0)
        lens.shift(LEFT * 2)
        
        mirror = PlaneMirror(height=2.5)
        mirror.shift(RIGHT * 2)
        
        # Les rayons interagissent avec les deux éléments
        ray = DynamicRay(
            start_point=LEFT * 5,
            direction=RIGHT,
            optical_elements=[lens, mirror],
            max_segments=5,  # Permet plusieurs rebonds
        )
        
        self.add(lens, mirror, ray)
        self.wait(2)
```

## 🧪 Tests

Le fichier `test_inital.py` contient 7 scènes de test :

1. **Test1_ConvergingLensBasic** - Lentille convergente avec rayons parallèles
2. **Test2_LensDynamicMovement** - Mouvement dynamique de la lentille
3. **Test3_DivergingLens** - Lentille divergente
4. **Test4_PlaneMirror** - Réflexion sur miroir plan
5. **Test5_LensAndMirror** - Combinaison lentille + miroir
6. **Test6_ThreePrincipalRays** - Les trois rayons principaux
7. **Test7_AnimatedObjectPosition** - Animation de la position de l'objet

### Lancer un test

```bash
# Depuis le terminal
manim test_inital.py Test1_ConvergingLensBasic -pql

# Ou en Python
python test_inital.py
```

## 🔧 Architecture technique

### Le système d'updaters

Le cœur du système est le **DynamicRay** qui utilise les updaters de Manim :

```python
class DynamicRay(VMobject):
    def __init__(self, start_point, direction, optical_elements, ...):
        # ...
        self.add_updater(self._update_ray_path)  # ✨ Magie !
    
    def _update_ray_path(self, mobject, dt=0):
        # Recalcule TOUT le chemin du rayon à chaque frame
        # basé sur les positions ACTUELLES des éléments
```

### Calculs optiques

**Optique paraxiale (lentilles minces) :**
- Formule : `1/f = 1/p + 1/p'`
- Approximation petits angles : `sin(θ) ≈ θ`
- Déviation angulaire : `θ_out = θ_in - h/f`

**Réflexion spéculaire (miroirs) :**
- Formule vectorielle : `R = D - 2(D·N)N`
- Angle d'incidence = angle de réflexion

## 🌟 Extensions futures

L'architecture permet facilement d'ajouter :

- **Lentilles épaisses** (optique générale avec loi de Snell)
- **Miroirs courbes** (sphériques, paraboliques)
- **Prismes** avec dispersion chromatique
- **Réflexion totale interne**
- **Aberrations optiques**

Il suffit d'hériter de `OpticalElement` et d'implémenter :
- `intersect(ray_start, ray_direction)` → trouve l'intersection
- `propagate_ray(...)` → calcule la nouvelle direction

## 📚 Documentation des classes

### OpticalElement (classe abstraite)

Classe de base pour tous les éléments optiques.

**Méthodes à implémenter :**
- `intersect()` : Calcule l'intersection avec un rayon
- `propagate_ray()` : Calcule la direction après interaction

### ThinLens

Lentille mince en approximation paraxiale.

**Paramètres :**
- `focal_length` : Distance focale (f > 0 : convergente, f < 0 : divergente)
- `height` : Hauteur de la lentille

### DynamicRay

Rayon qui se met à jour automatiquement.

**Paramètres :**
- `start_point` : Point de départ
- `direction` : Direction initiale
- `optical_elements` : Liste des éléments avec lesquels interagir
- `max_segments` : Nombre max de segments (évite les boucles infinies)

## 👨‍💻 Auteur

Corentin Nannini - Décembre 2025

## 📄 Licence

MIT License
