from manim import *

class PythagoreanTheoremProof(Scene):
    def construct(self):
        # Define side lengths
        a = 3
        b = 4
        c = 5

        # Create right-angled triangle
        triangle = Polygon(
            [0, 0, 0],
            [a, 0, 0],
            [a, b, 0],
            color=BLUE,
            fill_opacity=0.5
        )

        # Create squares
        square_a = Square(side_length=a, color=RED, fill_opacity=0.5).next_to(triangle, LEFT, buff=0)
        square_b = Square(side_length=b, color=GREEN, fill_opacity=0.5).next_to(triangle, UP, buff=0)
        square_c = Square(side_length=c, color=YELLOW, fill_opacity=0.5).next_to(triangle, RIGHT, buff=0).next_to(triangle, DOWN, buff=0)


        # Add labels
        label_a = MathTex("a").next_to(square_a, LEFT)
        label_b = MathTex("b").next_to(square_b, UP)
        label_c = MathTex("c").next_to(square_c, RIGHT)
        a_squared = MathTex("a^2").move_to(square_a.get_center())
        b_squared = MathTex("b^2").move_to(square_b.get_center())
        c_squared = MathTex("c^2").move_to(square_c.get_center())


        # Show initial setup
        self.play(Create(triangle), Create(square_a), Create(square_b), Create(square_c), Write(label_a), Write(label_b), Write(label_c))
        self.wait(1)
        self.play(Write(a_squared), Write(b_squared), Write(c_squared))
        self.wait(1)


        #Rearrangement - This part is simplified and doesn't show actual cutting and rearranging for simplicity.  A more complex solution would be needed for a true visual cut and paste.

        #This section shows the result of rearranging the smaller squares visually, without showing the cutting and rearranging process itself.  This is to simplify the animation.
        
        self.play(FadeOut(square_a), FadeOut(square_b))
        #To accurately represent the rearrangement, you'd need to decompose the smaller squares into smaller shapes and move those individually
        rearranged_squares = Rectangle(height=c, width=c, color=YELLOW, fill_opacity=0.5).move_to(square_c.get_center()) #This just creates a visually identical yellow square.  It does not show the rearrangement process.
        self.play(Create(rearranged_squares))
        self.wait(1)


        # Final equation
        equation = MathTex("a^2 + b^2 = c^2").scale(1.5).to_edge(DOWN)
        self.play(Write(equation))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])