"""
Test for CenteredSystem - Principal planes optical system
==========================================================
"""

from manim import *
from manim_optics import CenteredSystem, DynamicRay


class TestCenteredSystemBasic(Scene):
    """Basic test of CenteredSystem with a few rays."""
    
    def construct(self):
        # Create a centered system
        system = CenteredSystem(
            h_position=-1.5,
            h_prime_position=1.5,
            focal_length=3.0,
            height=4.0,
            show_labels=True,
            show_focal_points=True,
        )
        
        # Animate appearance
        self.play(system.create_animation(run_time=2.0))
        self.wait(0.5)
        
        # Create some test rays
        rays = []
        
        # Ray 1: Parallel to axis (should pass through F')
        ray1 = DynamicRay(
            start_point=np.array([-6.0, 0.5, 0.0]),
            direction=RIGHT,
            optical_elements=[system],
            color=RED,
            ray_length=12.0,
        )
        rays.append(ray1)
        
        # Ray 2: Through optical center
        ray2 = DynamicRay(
            start_point=np.array([-6.0, 1.0, 0.0]),
            direction=RIGHT,
            optical_elements=[system],
            color=YELLOW,
            ray_length=12.0,
        )
        rays.append(ray2)
        
        # Ray 3: Converging toward F
        ray3 = DynamicRay(
            start_point=np.array([-6.0, -0.5, 0.0]),
            direction=RIGHT,
            optical_elements=[system],
            color=GREEN,
            ray_length=12.0,
        )
        rays.append(ray3)
        
        # Add rays
        self.play(*[Create(ray) for ray in rays])
        self.wait(2)
        
        # Test toggling labels
        self.play(Flash(system.h_label, color=YELLOW))
        system.toggle_labels(False)
        self.wait(0.5)
        system.toggle_labels(True)
        self.wait(1)
        
        # Fade out
        self.play(
            system.fade_out_animation(),
            *[FadeOut(ray) for ray in rays]
        )
        self.wait()


class TestCenteredSystemRayTracing(Scene):
    """Test ray tracing through the centered system."""
    
    def construct(self):
        # Create centered system
        system = CenteredSystem(
            h_position=-2.0,
            h_prime_position=2.0,
            focal_length=4.0,
            height=5.0,
            show_labels=True,
            show_focal_points=True,
            boundary_color=BLUE_C,
        )
        
        self.add(system)
        self.wait(0.5)
        
        # Create a fan of rays
        num_rays = 7
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK]
        
        rays = []
        for i, color in enumerate(colors[:num_rays]):
            y_offset = -2.0 + i * (4.0 / (num_rays - 1))
            
            ray = DynamicRay(
                start_point=np.array([-7.0, y_offset, 0.0]),
                direction=RIGHT,
                optical_elements=[system],
                color=color,
                ray_length=15.0,
                stroke_width=2,
            )
            rays.append(ray)
        
        # Animate rays appearing
        self.play(
            *[Create(ray, run_time=1.5) for ray in rays],
            lag_ratio=0.1
        )
        self.wait(2)
        
        # Highlight principal planes
        self.play(
            system.h_plane.animate.set_color(YELLOW),
            system.h_prime_plane.animate.set_color(YELLOW),
            run_time=0.5
        )
        self.wait(1)
        
        # Return to original color
        self.play(
            system.h_plane.animate.set_color(WHITE),
            system.h_prime_plane.animate.set_color(WHITE),
            run_time=0.5
        )
        self.wait(2)


class TestCenteredSystemCustomBoundaries(Scene):
    """Test centered system with custom boundary curves."""
    
    def construct(self):
        # Define custom boundary points (top, bottom, radius) for each boundary
        # Left boundary: top point, bottom point, radius
        left_boundary = [
            np.array([-2.0, 2.5, 0.0]),   # top point
            np.array([-2.0, -2.5, 0.0]),  # bottom point
            3.5,                           # radius (negative in code makes it bulge left)
        ]
        
        # Right boundary: top point, bottom point, radius  
        right_boundary = [
            np.array([2.0, 2.5, 0.0]),    # top point
            np.array([2.0, -2.5, 0.0]),   # bottom point
            3.5,                           # radius (positive makes it bulge right)
        ]
        
        system = CenteredSystem(
            h_position=-1.0,
            h_prime_position=1.0,
            focal_length=2.5,
            height=5.0,
            left_boundary_points=left_boundary,
            right_boundary_points=right_boundary,
            show_labels=True,
            show_focal_points=True,
            boundary_color=TEAL,
            h_color=ORANGE,
        )
        
        self.play(system.create_animation(run_time=2.0))
        self.wait(1)
        
        # Create rays to test
        rays = []
        for i in range(5):
            y_pos = -1.5 + i * 0.75
            ray = DynamicRay(
                start_point=np.array([-6.0, y_pos, 0.0]),
                direction=RIGHT,
                optical_elements=[system],
                color=interpolate_color(BLUE, RED, i / 4),
                ray_length=12.0,
            )
            rays.append(ray)
        
        self.play(*[Create(ray) for ray in rays])
        self.wait(3)


class TestCenteredSystemHiddenSegments(Scene):
    """Test that ray segments between H and H' are properly hidden."""
    
    def construct(self):
        # Create system with visible planes
        system = CenteredSystem(
            h_position=-2.0,
            h_prime_position=2.0,
            focal_length=3.0,
            height=4.0,
            show_labels=True,
            show_focal_points=True,
            h_color=YELLOW,
            boundary_color=BLUE_C,
        )
        
        self.add(system)
        self.wait(0.5)
        
        # Create rays that clearly pass through the system
        rays = []
        colors = [RED, GREEN, BLUE, ORANGE, PURPLE]
        
        for i, color in enumerate(colors):
            y_offset = -1.5 + i * 0.75
            
            ray = DynamicRay(
                start_point=np.array([-6.0, y_offset, 0.0]),
                direction=RIGHT,
                optical_elements=[system],
                color=color,
                ray_length=12.0,
                stroke_width=3,
            )
            rays.append(ray)
        
        # Animate rays appearing
        self.play(*[Create(ray, run_time=1.5) for ray in rays])
        self.wait(2)
        
        # Highlight the region between H and H' where rays should be invisible
        highlight_region = Rectangle(
            width=abs(system.h_prime_position - system.h_position),
            height=system.system_height,
            stroke_color=YELLOW,
            stroke_width=4,
            fill_opacity=0.1,
            fill_color=YELLOW,
        )
        highlight_region.move_to([
            (system.h_position + system.h_prime_position) / 2,
            0,
            0
        ])
        
        self.play(FadeIn(highlight_region))
        self.wait(1)
        self.play(FadeOut(highlight_region))
        self.wait(2)


class TestCenteredSystemCurvature(Scene):
    """Test different boundary curvature values."""
    
    def construct(self):
        # Create systems with different curvatures side by side
        systems = []
        curvatures = [0.5, 0.7, 1.0, 1.5]
        colors = [RED, YELLOW, GREEN, BLUE]
        
        for i, (curv, col) in enumerate(zip(curvatures, colors)):
            system = CenteredSystem(
                h_position=-0.5 - i * 2.5,
                h_prime_position=0.5 - i * 2.5,
                focal_length=2.0,
                height=2.0,
                boundary_curvature=curv,
                show_labels=False,
                show_focal_points=False,
                boundary_color=col,
                h_color=col,
            )
            systems.append(system)
            
            # Add label for curvature value
            label = Text(f"c={curv}", font_size=20, color=col)
            label.next_to(system, DOWN, buff=0.3)
            systems.append(label)
        
        # Show all systems
        self.play(*[FadeIn(s) for s in systems])
        self.wait(2)
        
        # Add rays to each system to show optical behavior
        all_rays = []
        for i, system in enumerate([s for s in systems if isinstance(s, CenteredSystem)]):
            for j in range(3):
                y_pos = -0.6 + j * 0.6
                ray = DynamicRay(
                    start_point=np.array([system.h_position - 2.0, y_pos, 0.0]),
                    direction=RIGHT,
                    optical_elements=[system],
                    color=colors[i],
                    ray_length=5.0,
                    stroke_width=1.5,
                )
                all_rays.append(ray)
        
        self.play(*[Create(ray, run_time=1.5) for ray in all_rays])
        self.wait(3)
