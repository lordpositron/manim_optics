manim_optics.optics_3d
======================

.. py:module:: manim_optics.optics_3d

.. autoapi-nested-parse::

   Module pour les éléments optiques en 3D avec support des rotations complètes.

   Classes principales :
   - OpticalElement3D : Base pour tous les éléments optiques 3D
   - ThinLens3D : Lentille mince en 3D avec deux modes d'affichage
   - RayBundle3D : Faisceau de rayons en 3D



Classes
-------

.. autoapisummary::

   manim_optics.optics_3d.OpticalElement3D
   manim_optics.optics_3d.ThinLens3D
   manim_optics.optics_3d.RayBundle3D


Module Contents
---------------

.. py:class:: OpticalElement3D(position=ORIGIN, normal_vector=UP, **kwargs)

   Bases: :py:obj:`manim.VGroup`


   Classe de base pour tous les éléments optiques 3D.

   Gère un plan optique dans l'espace 3D avec position et orientation arbitraires.
   Le plan est défini par un point et un vecteur normal.

   :param position: Point de référence sur le plan optique (centre) [x, y, z]
   :type position: np.ndarray
   :param normal_vector: Vecteur normal au plan optique [nx, ny, nz]
                         Par défaut UP = [0, 1, 0] (plan horizontal)
   :type normal_vector: np.ndarray
   :param \*\*kwargs: Arguments supplémentaires pour VGroup


   .. py:attribute:: position


   .. py:attribute:: normal


   .. py:method:: intersect_3d(ray_start, ray_direction)

      Calcule l'intersection entre un rayon et le plan optique.

      Équation du plan : (P - P0) · n = 0
      Équation du rayon : P = R0 + t*d
      Solution : t = (P0 - R0) · n / (d · n)

      :param ray_start: Point de départ du rayon [x, y, z]
      :type ray_start: np.ndarray
      :param ray_direction: Direction du rayon (normalisée) [dx, dy, dz]
      :type ray_direction: np.ndarray

      :returns: Point d'intersection [x, y, z] ou None si pas d'intersection
      :rtype: np.ndarray or None



   .. py:method:: get_optical_plane_position()

      Retourne la position du plan optique (centre).



   .. py:method:: get_normal_vector()

      Retourne le vecteur normal au plan optique.



   .. py:method:: propagate_ray_3d(ray_start, ray_direction, intersection_point)
      :abstractmethod:


      Propage un rayon à travers l'élément optique.
      À redéfinir dans les sous-classes.

      :param ray_start: Point de départ du rayon
      :type ray_start: np.ndarray
      :param ray_direction: Direction du rayon avant interaction
      :type ray_direction: np.ndarray
      :param intersection_point: Point d'intersection avec l'élément
      :type intersection_point: np.ndarray

      :returns: (nouvelle_direction, continue)
                nouvelle_direction : direction après interaction
                continue : True si le rayon continue, False s'il est arrêté
      :rtype: tuple(np.ndarray, bool)



.. py:class:: ThinLens3D(focal_length=3.0, aperture_radius=2.0, position=ORIGIN, normal_vector=UP, display_mode='simple', thickness=0.2, R1=5.0, R2=5.0, color=BLUE_E, opacity=0.6, show_focal_points=False, **kwargs)

   Bases: :py:obj:`OpticalElement3D`


   Lentille mince en 3D avec support des rotations complètes.

   Implémente l'approximation de la lentille mince en 3D avec deux modes d'affichage :
   - Mode 'simple' : cercle 3D symbolique
   - Mode 'detailed' : surfaces biconvexes réalistes

   :param focal_length: Distance focale de la lentille (positive pour convergente)
   :type focal_length: float
   :param aperture_radius: Rayon d'ouverture de la lentille
   :type aperture_radius: float
   :param position: Position du centre de la lentille [x, y, z]
   :type position: np.ndarray
   :param normal_vector: Vecteur normal au plan de la lentille
   :type normal_vector: np.ndarray
   :param display_mode: 'simple' pour un cercle, 'detailed' pour les surfaces
   :type display_mode: str
   :param thickness: Épaisseur au centre (pour mode detailed)
   :type thickness: float
   :param R1: Rayons de courbure des faces (pour mode detailed)
   :type R1: float
   :param R2: Rayons de courbure des faces (pour mode detailed)
   :type R2: float
   :param color: Couleur de la lentille
   :type color: Color
   :param opacity: Opacité de la lentille
   :type opacity: float
   :param show_focal_points: Afficher les points focaux
   :type show_focal_points: bool
   :param \*\*kwargs: Arguments supplémentaires pour VGroup


   .. py:attribute:: focal_length
      :value: 3.0



   .. py:attribute:: focal_length_tracker


   .. py:attribute:: aperture_radius
      :value: 2.0



   .. py:attribute:: aperture_radius_tracker


   .. py:attribute:: position


   .. py:attribute:: position_x_tracker


   .. py:attribute:: position_y_tracker


   .. py:attribute:: position_z_tracker


   .. py:attribute:: normal


   .. py:attribute:: normal_x_tracker


   .. py:attribute:: normal_y_tracker


   .. py:attribute:: normal_z_tracker


   .. py:attribute:: display_mode
      :value: 'simple'



   .. py:attribute:: thickness
      :value: 0.2



   .. py:attribute:: R1
      :value: 5.0



   .. py:attribute:: R2
      :value: 5.0



   .. py:attribute:: lens_color


   .. py:attribute:: lens_opacity
      :value: 0.6



   .. py:attribute:: show_focal_points
      :value: False



   .. py:method:: animate_focal_length(new_focal_length, run_time=2.0, **kwargs)

      Anime un changement de distance focale.

      :param new_focal_length: Nouvelle distance focale cible
      :type new_focal_length: float
      :param run_time: Durée de l'animation
      :type run_time: float
      :param \*\*kwargs: Arguments supplémentaires pour l'animation

      :returns: Animation qui change la distance focale
      :rtype: Animation



   .. py:method:: set_focal_length(focal_length)

      Définit la distance focale immédiatement sans animation.



   .. py:method:: animate_aperture_radius(new_radius, run_time=2.0, **kwargs)

      Anime un changement de rayon d'ouverture.

      :param new_radius: Nouveau rayon d'ouverture
      :type new_radius: float
      :param run_time: Durée de l'animation
      :type run_time: float
      :param \*\*kwargs: Arguments supplémentaires pour l'animation

      :returns: Animation qui change le rayon d'ouverture
      :rtype: Animation



   .. py:method:: set_aperture_radius(radius)

      Définit le rayon d'ouverture immédiatement sans animation.



   .. py:method:: animate_position(new_position, run_time=2.0, **kwargs)

      Anime un changement de position 3D.

      :param new_position: Nouvelle position [x, y, z]
      :type new_position: np.ndarray
      :param run_time: Durée de l'animation
      :type run_time: float
      :param \*\*kwargs: Arguments supplémentaires pour l'animation

      :returns: Groupe d'animations pour x, y et z
      :rtype: AnimationGroup



   .. py:method:: set_position_3d(position)

      Définit la position 3D immédiatement sans animation.



   .. py:method:: animate_normal_vector(new_normal, run_time=2.0, **kwargs)

      Anime un changement d'orientation (vecteur normal).

      :param new_normal: Nouveau vecteur normal [nx, ny, nz]
      :type new_normal: np.ndarray
      :param run_time: Durée de l'animation
      :type run_time: float
      :param \*\*kwargs: Arguments supplémentaires pour l'animation

      :returns: Groupe d'animations pour les composantes du vecteur normal
      :rtype: AnimationGroup



   .. py:method:: set_normal_vector(normal)

      Définit le vecteur normal immédiatement sans animation.



   .. py:method:: propagate_ray_3d(ray_start, ray_direction, intersection_point)

      Propage un rayon à travers la lentille mince en 3D.

      Utilise la formule de la lentille mince en décomposant le rayon
      dans le repère local de la lentille.

      :param ray_start: Point de départ du rayon
      :type ray_start: np.ndarray
      :param ray_direction: Direction du rayon avant la lentille
      :type ray_direction: np.ndarray
      :param intersection_point: Point d'intersection avec la lentille
      :type intersection_point: np.ndarray

      :returns: (nouvelle_direction, True) - le rayon continue toujours
      :rtype: tuple(np.ndarray, bool)



.. py:class:: RayBundle3D(start_points, direction_vector, optical_elements=None, max_length=20.0, color=YELLOW, stroke_width=2, auto_update=True, **kwargs)

   Bases: :py:obj:`manim.VGroup`


   Faisceau de rayons en 3D qui interagissent avec des éléments optiques 3D.

   Trace plusieurs rayons depuis des points de départ différents avec la même
   direction initiale, et les propage à travers une séquence d'éléments optiques.

   :param start_points: Liste des points de départ des rayons [x, y, z]
   :type start_points: list of np.ndarray
   :param direction_vector: Direction initiale commune à tous les rayons [dx, dy, dz]
   :type direction_vector: np.ndarray
   :param optical_elements: Liste des éléments optiques à traverser (dans l'ordre)
   :type optical_elements: list of OpticalElement3D
   :param max_length: Longueur maximale d'un segment de rayon
   :type max_length: float
   :param color: Couleur des rayons
   :type color: Color
   :param stroke_width: Épaisseur des rayons
   :type stroke_width: float
   :param auto_update: Si True, les rayons se recalculent automatiquement à chaque frame
                       quand les éléments optiques bougent (défaut: True)
   :type auto_update: bool
   :param \*\*kwargs: Arguments supplémentaires pour VGroup


   .. py:attribute:: start_points


   .. py:attribute:: direction


   .. py:attribute:: optical_elements
      :value: []



   .. py:attribute:: max_length
      :value: 20.0



   .. py:attribute:: ray_color


   .. py:attribute:: ray_stroke_width
      :value: 2



   .. py:attribute:: auto_update
      :value: True



