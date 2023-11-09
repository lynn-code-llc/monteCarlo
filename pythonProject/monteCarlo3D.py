
from manim import *
import numpy as np

class MonteCarlo(ThreeDScene):

    def construct(self):

        num_of_points = 200

        circle = Circle(radius=2)
        square = Square(side_length=4, color=BLUE_C).move_to(circle)
        
        explanation = Paragraph('Next lets extend our analysis into the 3rd dimension!', font_size=30, alignment='center').next_to(circle, UP*3)
        explanation_1 = Paragraph('Now we are interested in the ratio\n of the volumes of a sphere and a cube', font_size=30, alignment='center').next_to(circle, UP*3) 
        explanation_2 = MathTex(r'\text{Once again, we simplify and solve for } \pi').next_to(circle, UP*3)    
        explanation_3 = Paragraph('Now we can use a Monte Carlo Simulation\n to approximate the volumes of the shapes \n by randomly plotting points within the cube',font_size=30, alignment='center').next_to(circle,UP*2) 
        explanation_4 = MathTex(r'\text{Evaluating the full expression allows us to approximate } \pi!').next_to(circle, UP*3)
        explanation_5 = Paragraph('The more points we plot \n the more accurate our approximation becomes!', font_size=30, alignment='center').next_to(circle,UP*3)

        radius = Line(circle.get_center(), circle.get_edge_center(RIGHT))
        radius_copy = radius.copy()
        r = MathTex('r').next_to(radius, UP)
        ref_line = Line(circle.get_edge_center(DOWN), circle.get_corner(DR)).shift(DOWN*MED_SMALL_BUFF)
        reverse_line = Line(circle.get_edge_center(DOWN), circle.get_corner(DL)).shift(DOWN*MED_SMALL_BUFF)
        two_r = MathTex('2r').move_to(circle.get_edge_center(DOWN)).shift(DOWN*MED_LARGE_BUFF)

        line_group = VGroup(radius,r,ref_line,reverse_line,two_r)
        approx_equal = MathTex(r'\approx')

        sphere = Sphere(radius=2, fill_opacity=0.1).set_color(RED).rotate(90 * DEGREES, axis=RIGHT, about_point=ORIGIN)
        cube = Cube(side_length=4, fill_opacity=0.1, stroke_width=1, stroke_color=BLUE_C)

        shapes = VGroup(circle, square)

        tex1 = MathTex(r'\left(\frac{\text {area of sphere}}{\text {area of cube}}\right)=', r'\frac{\pi r^{3}}{',r'(2 r)^{3}}')
        # tex1.next_to(square, buff=LARGE_BUFF,aligned_edge=UP)
        tex1.shift(RIGHT*3)
        tex2 = MathTex(r'\left(\frac{\text {area of sphere}}{\text {area of cube}}\right)=', r'\frac{\pi r^{3}}{',r'8 r^{3}}')
        black_square = Square(0.6, 
                                color=BLACK,         
                               fill_opacity=1).next_to(tex1, RIGHT)
        cdot = MathTex('\cdot').next_to(tex1,LEFT, buff=SMALL_BUFF)
        tex2.move_to(tex1)
        line1 = Line(tex1[1][2].get_corner(UR), tex1[1][1].get_corner(DL), color=YELLOW)
        line2 = Line(tex2[-1].get_corner(UR), tex2[-1][1].get_corner(DL), color=YELLOW)
        
        
        zeros = np.zeros((num_of_points, 1))
        positions_2d = square.side_length * np.random.random_sample((num_of_points, 2)) - square.side_length / 2
        positions_2d = np.append(positions_2d, zeros, axis=1)
        dots_2d = VGroup()
        all_values = VGroup()
        
        positions_3d = square.side_length * np.random.random_sample((num_of_points, 3)) - square.side_length / 2
        dots_3d = VGroup()

        def gen_3d_points():
            for i in range(num_of_points): 
                ith_position = positions_3d[i, :]
                ith_color = RED
                dist_from_origin = np.linalg.norm(ith_position - ORIGIN)
                if dist_from_origin > circle.radius:
                    ith_color = BLUE
                dots_3d.add(Dot3D(radius=DEFAULT_SMALL_DOT_RADIUS, point=ith_position, color=ith_color))
            return dots_3d

        self.play(Write(explanation))
        self.play(Create(shapes))
        
        self.wait()
        self.play(FadeOut(explanation))
        self.play(Succession(Create(radius),
                                FadeIn(r)))
        self.play(Succession(TransformFromCopy(radius,ref_line),
                                Create(reverse_line),
                                FadeIn(two_r)))
        self.wait()
        self.play(Write(explanation_1))
        self.wait(0.5)

        self.move_camera(phi=-30 * DEGREES, theta=-160 * DEGREES, gamma=-90 * DEGREES) 
        self.play(Create(sphere))
        self.play(GrowFromCenter(cube[0]),
                   GrowFromCenter(cube[1]),            
                   GrowFromCenter(cube[2]),
                   GrowFromCenter(cube[3]),
                   GrowFromCenter(cube[4]),
                   GrowFromCenter(cube[5]))
        self.add_fixed_in_frame_mobjects(tex1)
        self.remove(tex1)
        
        self.move_camera(zoom=0.9,frame_center=[3,0.7,-1.5]) 
        # self.play(cube.animate.shift(OUT*3*LEFT))

        # self.play(cube.animate.shift(OUT * LEFT * 20))
        self.play(Write(tex1))
        self.wait()
        self.play(Write(explanation_2))
        self.wait()
        self.play(FadeOut(explanation_2))
        self.play(Indicate(tex1[2][0]),Indicate(tex1[2][3:]),run_time=2)

        self.add(black_square)      

        self.play(Transform(tex1[2][1], tex2[2][0]),
                 Transform(tex1[2:],tex2[2:]))
        self.wait(0.5)
        self.play(Create(line1),Create(line2))
        self.wait(0.5)
        self.play(FadeOut(line1,line2, tex1[1][1:3], tex1[2][2:], r, two_r, radius, ref_line, reverse_line),
                            black_square.animate.shift(LEFT*0.75))
        self.wait(0.5)

        self.play(LaggedStart(tex1[2][0].animate.next_to(cdot, LEFT, buff=SMALL_BUFF),
                            FadeIn(cdot),
                            tex1[1][0].animate.next_to(tex1[0],RIGHT, buff=SMALL_BUFF),
                            FadeOut(tex1[1][3], black_square)), run_time=2)
        self.wait()
        nums = MathTex(r'\left(\frac{\text {pts in circle}}{\text {total pts in square}}\right)',                                                            
                            font_size=48).next_to(cdot, buff=SMALL_BUFF)
        nums[0][1:12].set_color(RED)
        nums[0][13:-1].set_color_by_gradient(RED,BLUE)
        self.wait(0.5)
        self.play(Write(explanation_3))
        self.wait(2)
        self.play(FadeOut(explanation_3))
        self.play(FadeOut(tex1[0][0:-1]), FadeIn(nums),
                    Transform(tex1[0][-1], (approx_equal.next_to(nums, buff=SMALL_BUFF))),
                    tex1[1][0].animate.next_to(approx_equal))

        self.wait(2)
        initial_nums = MathTex(r'\left(\,\frac{\qquad0\qquad}{0\,\,\,\,+\,\,\,0}\,\right) 0.0000').next_to(cdot)
        initial_nums[0][1].set_color(RED)
        initial_nums[0][3].set_color(RED)
        initial_nums[0][5].set_color(BLUE)
        initial_nums[0][7:].set_color(YELLOW).shift(RIGHT*0.6)

        self.play(ReplacementTransform(nums[0][0], initial_nums[0][0]),
                  ReplacementTransform(nums[0][1:12], initial_nums[0][1]),
                  ReplacementTransform(nums[0][12], initial_nums[0][2]),
                  ReplacementTransform(nums[0][13:21], initial_nums[0][3]),
                  ReplacementTransform(nums[0][21:-1], initial_nums[0][5]),
                  ReplacementTransform(nums[0][-1], initial_nums[0][6]),
                  ReplacementTransform(tex1[1][0], initial_nums[0][7:]),
                  FadeIn(initial_nums[0][4]),
                  cdot.animate.shift(RIGHT * 0.07),
                  tex1[0][-1].animate.next_to(initial_nums[0][6]),
                  ) 
        self.wait()
        self.play(Write(explanation_4))
        self.wait()

        self.play(FadeOut(explanation_4))

        self.wait()
        self.play(FadeOut(*self.mobjects))
        self.wait()
        self.play(Rotate(square, 45, axis=UP))

        # self.play(ShowIncreasingSubsets(gen_3d_points().shift(LEFT*2)), run_time=5)
        self.wait()