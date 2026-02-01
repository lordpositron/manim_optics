"""
Module pour les éléments optiques en 3D avec support des rotations complètes.

Classes principales :
- OpticalElement3D : Base pour tous les éléments optiques 3D
- ThinLens3D : Lentille mince en 3D avec deux modes d'affichage
- RayBundle3D : Faisceau de rayons en 3D
"""

import numpy as np
from manim import *


class OpticalElement3D(VGroup):
    """
    Classe de base pour tous les éléments optiques 3D.

    Gère un plan optique dans l'espace 3D avec position et orientation arbitraires.
    Le plan est défini par un point et un vecteur normal.

    Parameters
    ----------
    position : np.ndarray
        Point de référence sur le plan optique (centre) [x, y, z]
    normal_vector : np.ndarray
        Vecteur normal au plan optique [nx, ny, nz]
        Par défaut UP = [0, 1, 0] (plan horizontal)
    **kwargs
        Arguments supplémentaires pour VGroup
    """

    def __init__(self, position=ORIGIN, normal_vector=UP, **kwargs):
        super().__init__(**kwargs)
        self.position = np.array(position, dtype=float)
        self.normal = np.array(normal_vector, dtype=float)
        self.normal = self.normal / np.linalg.norm(self.normal)

    def intersect_3d(self, ray_start, ray_direction):
        """
        Calcule l'intersection entre un rayon et le plan optique.

        Équation du plan : (P - P0) · n = 0
        Équation du rayon : P = R0 + t*d
        Solution : t = (P0 - R0) · n / (d · n)

        Parameters
        ----------
        ray_start : np.ndarray
            Point de départ du rayon [x, y, z]
        ray_direction : np.ndarray
            Direction du rayon (normalisée) [dx, dy, dz]

        Returns
        -------
        np.ndarray or None
            Point d'intersection [x, y, z] ou None si pas d'intersection
        """
        ray_direction = ray_direction / np.linalg.norm(ray_direction)

        denom = np.dot(ray_direction, self.normal)

        # Rayon parallèle au plan
        if abs(denom) < 1e-6:
            return None

        t = np.dot(self.position - ray_start, self.normal) / denom

        # Intersection derrière le point de départ
        if t < 1e-6:
            return None

        return ray_start + t * ray_direction

    def get_optical_plane_position(self):
        """Retourne la position du plan optique (centre)."""
        return self.position.copy()

    def get_normal_vector(self):
        """Retourne le vecteur normal au plan optique."""
        return self.normal.copy()

    def propagate_ray_3d(self, ray_start, ray_direction, intersection_point):
        """
        Propage un rayon à travers l'élément optique.
        À redéfinir dans les sous-classes.

        Parameters
        ----------
        ray_start : np.ndarray
            Point de départ du rayon
        ray_direction : np.ndarray
            Direction du rayon avant interaction
        intersection_point : np.ndarray
            Point d'intersection avec l'élément

        Returns
        -------
        tuple(np.ndarray, bool)
            (nouvelle_direction, continue)
            nouvelle_direction : direction après interaction
            continue : True si le rayon continue, False s'il est arrêté
        """
        raise NotImplementedError("Méthode à implémenter dans les sous-classes")


class ThinLens3D(OpticalElement3D):
    """
    Lentille mince en 3D avec support des rotations complètes.

    Implémente l'approximation de la lentille mince en 3D avec deux modes d'affichage :
    - Mode 'simple' : cercle 3D symbolique
    - Mode 'detailed' : surfaces biconvexes réalistes

    Parameters
    ----------
    focal_length : float
        Distance focale de la lentille (positive pour convergente)
    aperture_radius : float
        Rayon d'ouverture de la lentille
    position : np.ndarray
        Position du centre de la lentille [x, y, z]
    normal_vector : np.ndarray
        Vecteur normal au plan de la lentille
    display_mode : str
        'simple' pour un cercle, 'detailed' pour les surfaces
    thickness : float
        Épaisseur au centre (pour mode detailed)
    R1, R2 : float
        Rayons de courbure des faces (pour mode detailed)
    color : Color
        Couleur de la lentille
    opacity : float
        Opacité de la lentille
    show_focal_points : bool
        Afficher les points focaux
    **kwargs
        Arguments supplémentaires pour VGroup
    """

    def __init__(
        self,
        focal_length=3.0,
        aperture_radius=2.0,
        position=ORIGIN,
        normal_vector=UP,
        display_mode="simple",  # 'simple' ou 'detailed'
        thickness=0.2,
        R1=5.0,
        R2=5.0,
        color=BLUE_E,
        opacity=0.6,
        show_focal_points=False,
        **kwargs
    ):
        super().__init__(position=position, normal_vector=normal_vector, **kwargs)

        self.focal_length = focal_length
        self.aperture_radius = aperture_radius
        self.display_mode = display_mode
        self.thickness = thickness
        self.R1 = R1
        self.R2 = R2
        self.lens_color = color
        self.lens_opacity = opacity
        self.show_focal_points = show_focal_points

        # Calculer les vecteurs du repère local de la lentille
        self._compute_local_frame()

        # Créer le visuel
        self._create_visual()

    def _compute_local_frame(self):
        """
        Calcule un repère orthonormé local (u, v, n) pour la lentille.
        n = normal, u et v sont dans le plan de la lentille.
        """
        self.n = self.normal

        # Choisir un vecteur arbitraire non colinéaire à n
        if abs(self.n[2]) < 0.9:
            arbitrary = np.array([0, 0, 1])
        else:
            arbitrary = np.array([1, 0, 0])

        # u = arbitrary × n (produit vectoriel)
        self.u = np.cross(arbitrary, self.n)
        self.u = self.u / np.linalg.norm(self.u)

        # v = n × u
        self.v = np.cross(self.n, self.u)
        self.v = self.v / np.linalg.norm(self.v)

    def _create_visual(self):
        """Crée le visuel de la lentille selon le mode choisi."""
        if self.display_mode == "simple":
            self._create_simple_visual()
        else:
            self._create_detailed_visual()

        if self.show_focal_points:
            self._create_focal_points()

    def _create_simple_visual(self):
        """Crée un cercle 3D simple pour représenter la lentille."""
        # Créer un cercle dans le plan XY puis le transformer
        circle = Circle(
            radius=self.aperture_radius,
            color=self.lens_color,
            fill_opacity=self.lens_opacity,
            stroke_width=2,
        )

        # Positionner et orienter le cercle
        circle.move_to(ORIGIN)

        # Rotation pour aligner avec le vecteur normal
        # Par défaut, le cercle est dans le plan XY avec normale OUT
        default_normal = OUT

        # Calculer l'axe et l'angle de rotation
        axis = np.cross(default_normal, self.n)
        axis_length = np.linalg.norm(axis)

        if axis_length > 1e-6:
            axis = axis / axis_length
            angle = np.arccos(np.clip(np.dot(default_normal, self.n), -1.0, 1.0))
            circle.rotate(angle, axis=axis, about_point=ORIGIN)
        elif np.dot(default_normal, self.n) < 0:
            # Vecteurs opposés, rotation de 180°
            circle.rotate(PI, axis=RIGHT, about_point=ORIGIN)

        circle.shift(self.position)

        self.add(circle)
        self.lens_visual = circle

    def _create_detailed_visual(self):
        """Crée des surfaces biconvexes réalistes pour la lentille."""

        def front_face(u, v):
            x = u * np.cos(v)
            y = u * np.sin(v)
            r = np.sqrt(x**2 + y**2)
            z = -self.thickness / 2 + (r**2 - self.aperture_radius**2) / (2 * self.R1)
            return np.array([x, y, z])

        def back_face(u, v):
            x = u * np.cos(v)
            y = u * np.sin(v)
            r = np.sqrt(x**2 + y**2)
            z = self.thickness / 2 - (r**2 - self.aperture_radius**2) / (2 * self.R2)
            return np.array([x, y, z])

        def rim(u, v):
            x = self.aperture_radius * np.cos(v)
            y = self.aperture_radius * np.sin(v)
            z = np.linspace(
                self.thickness / 2,
                -self.thickness / 2,
                int(u * 10 + 1),
            )[-1]
            return np.array([x, y, z])

        front = Surface(
            front_face,
            u_range=[0, self.aperture_radius],
            v_range=[0, TAU],
            resolution=(24, 48),
            fill_opacity=self.lens_opacity,
            fill_color=self.lens_color,
            checkerboard_colors=[self.lens_color, self.lens_color],
            stroke_color=self.lens_color,
            stroke_width=0,
            should_make_jagged=True,
        )

        back = Surface(
            back_face,
            u_range=[0, self.aperture_radius],
            v_range=[0, TAU],
            resolution=(24, 48),
            fill_opacity=self.lens_opacity,
            fill_color=self.lens_color,
            checkerboard_colors=[self.lens_color, self.lens_color],
            stroke_color=self.lens_color,
            stroke_width=0,
            should_make_jagged=True,
        )

        rim_surface = Surface(
            rim,
            u_range=[0, 1],
            v_range=[0, TAU],
            resolution=(2, 48),
            fill_opacity=self.lens_opacity,
            fill_color=self.lens_color,
            checkerboard_colors=[self.lens_color, self.lens_color],
            stroke_color=self.lens_color,
            stroke_width=0,
            should_make_jagged=True,
        )

        lens_group = VGroup(front, back, rim_surface)

        # Orienter la lentille
        default_normal = OUT
        axis = np.cross(default_normal, self.n)
        axis_length = np.linalg.norm(axis)

        if axis_length > 1e-6:
            axis = axis / axis_length
            angle = np.arccos(np.clip(np.dot(default_normal, self.n), -1.0, 1.0))
            lens_group.rotate(angle, axis=axis, about_point=ORIGIN)
        elif np.dot(default_normal, self.n) < 0:
            lens_group.rotate(PI, axis=RIGHT, about_point=ORIGIN)

        lens_group.shift(self.position)

        self.add(lens_group)
        self.lens_visual = lens_group

    def _create_focal_points(self):
        """Crée les points focaux avant et arrière."""
        f_front = self.position - self.focal_length * self.n
        f_back = self.position + self.focal_length * self.n

        focal_front = Dot3D(point=f_front, color=RED, radius=0.05)
        focal_back = Dot3D(point=f_back, color=RED, radius=0.05)

        self.add(focal_front, focal_back)
        self.focal_points = VGroup(focal_front, focal_back)

    def propagate_ray_3d(self, ray_start, ray_direction, intersection_point):
        """
        Propage un rayon à travers la lentille mince en 3D.

        Utilise la formule de la lentille mince en décomposant le rayon
        dans le repère local de la lentille.

        Parameters
        ----------
        ray_start : np.ndarray
            Point de départ du rayon
        ray_direction : np.ndarray
            Direction du rayon avant la lentille
        intersection_point : np.ndarray
            Point d'intersection avec la lentille

        Returns
        -------
        tuple(np.ndarray, bool)
            (nouvelle_direction, True) - le rayon continue toujours
        """
        # Vérifier si le rayon passe à travers l'ouverture
        delta = intersection_point - self.position
        radial_distance = np.sqrt(
            np.dot(delta, self.u) ** 2 + np.dot(delta, self.v) ** 2
        )

        if radial_distance > self.aperture_radius:
            # Rayon bloqué par l'ouverture
            return None, False

        # Décomposer la direction dans le repère local
        ray_direction = ray_direction / np.linalg.norm(ray_direction)

        # Composante selon u et v (dans le plan de la lentille)
        d_u = np.dot(ray_direction, self.u)
        d_v = np.dot(ray_direction, self.v)
        d_n = np.dot(ray_direction, self.n)

        # Position dans le plan de la lentille
        h_u = np.dot(delta, self.u)
        h_v = np.dot(delta, self.v)

        # Formule de la lentille mince en 3D
        # Pour une lentille mince, la déviation angulaire est : Δθ = -h/f
        # où θ est l'angle par rapport à la normale du plan de la lentille
        #
        # En 3D, l'angle paraxial est : θ ≈ d_u / d_n
        # Après la lentille : θ_out = θ_in - h/f
        # Donc : d_u_out / d_n = d_u_in / d_n - h/f
        # Ce qui donne : d_u_out = d_u_in - h * d_n / f
        #
        # Note : d_n doit être multiplié (pas divisé) car la déviation
        # est proportionnelle à la composante normale du rayon

        if abs(d_n) < 1e-6:
            # Rayon quasi-parallèle au plan de la lentille
            return ray_direction, True

        # Nouvelle direction dans le repère local
        new_d_u = d_u - h_u * d_n / self.focal_length
        new_d_v = d_v - h_v * d_n / self.focal_length
        # d_n reste inchangé

        new_direction = new_d_u * self.u + new_d_v * self.v + d_n * self.n
        new_direction = new_direction / np.linalg.norm(new_direction)

        return new_direction, True


class RayBundle3D(VGroup):
    """
    Faisceau de rayons en 3D qui interagissent avec des éléments optiques 3D.

    Trace plusieurs rayons depuis des points de départ différents avec la même
    direction initiale, et les propage à travers une séquence d'éléments optiques.

    Parameters
    ----------
    start_points : list of np.ndarray
        Liste des points de départ des rayons [x, y, z]
    direction_vector : np.ndarray
        Direction initiale commune à tous les rayons [dx, dy, dz]
    optical_elements : list of OpticalElement3D
        Liste des éléments optiques à traverser (dans l'ordre)
    max_length : float
        Longueur maximale d'un segment de rayon
    color : Color
        Couleur des rayons
    stroke_width : float
        Épaisseur des rayons
    **kwargs
        Arguments supplémentaires pour VGroup
    """

    def __init__(
        self,
        start_points,
        direction_vector,
        optical_elements=None,
        max_length=20.0,
        color=YELLOW,
        stroke_width=2,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.start_points = [np.array(p, dtype=float) for p in start_points]
        self.direction = np.array(direction_vector, dtype=float)
        self.direction = self.direction / np.linalg.norm(self.direction)
        self.optical_elements = optical_elements or []
        self.max_length = max_length
        self.ray_color = color
        self.ray_stroke_width = stroke_width

        self._create_rays()

    def _create_rays(self):
        """Crée et trace tous les rayons du faisceau."""
        for start_point in self.start_points:
            ray_path = self._trace_single_ray(start_point, self.direction)

            if len(ray_path) > 1:
                # Créer les segments du rayon
                for i in range(len(ray_path) - 1):
                    segment = Line3D(
                        start=ray_path[i],
                        end=ray_path[i + 1],
                        color=self.ray_color,
                        stroke_width=self.ray_stroke_width,
                    )
                    self.add(segment)

    def _trace_single_ray(self, start_point, direction):
        """
        Trace un seul rayon à travers tous les éléments optiques.

        Returns
        -------
        list of np.ndarray
            Liste des points du parcours du rayon
        """
        path = [start_point.copy()]
        current_pos = start_point.copy()
        current_dir = direction.copy()

        for element in self.optical_elements:
            # Chercher l'intersection avec l'élément
            intersection = element.intersect_3d(current_pos, current_dir)

            if intersection is None:
                # Pas d'intersection, prolonger le rayon
                current_pos = current_pos + self.max_length * current_dir
                path.append(current_pos)
                break

            # Ajouter le point d'intersection
            path.append(intersection)

            # Propager le rayon à travers l'élément
            new_direction, continues = element.propagate_ray_3d(
                current_pos, current_dir, intersection
            )

            if not continues:
                # Rayon arrêté
                break

            # Continuer avec la nouvelle direction
            current_pos = intersection.copy()
            current_dir = new_direction.copy()
        else:
            # Si on a traversé tous les éléments, prolonger le dernier segment
            final_pos = current_pos + self.max_length * current_dir
            path.append(final_pos)

        return path
