
from manim import *
import numpy as np
import time

class MonteCarlo2D(ThreeDScene):

    def construct(self):
        
        start_time = time.time()

        num_of_points = 3

        opening_text = Text('Monte Carlo Simulations are a broad class of computational algorithms \nthat rely on repeated random sampling to obtain numerical results.',font_size=30)
        opening_text1 = Text('The underlying concept is to use randomness to solve problems \n that might be deterministic in principle.',font_size=30)
        

        circle = Circle(radius=2)
        square = Square(side_length=4, color=BLUE_C).move_to(circle)
        
        explanation = Paragraph('First, we begin with a circle\n inscribed within a square', font_size=30, alignment='center').next_to(circle, UP*3)
        explanation_1 = Paragraph('We are interested in the ratio\n of the areas of the circle and square', font_size=30, alignment='center').next_to(circle, UP*3) 
        explanation_2 = MathTex(r'\text{Next, we simplify and solve for } \pi').next_to(circle, UP*3)    
        explanation_3 = Paragraph('Now we can use a Monte Carlo Simulation\n to approximate the areas of the shapes \n by randomly plotting points within the square',font_size=30, alignment='center').next_to(circle,UP*2) 
        explanation_4 = MathTex(r'\text{Evaluating the full expression allows us to approximate } \pi!').next_to(circle, UP*3)
        explanation_5 = Paragraph('The more points we plot \n the more accurate our approximation becomes!', font_size=30, alignment='center').next_to(circle,UP*3)
        promo = Paragraph('If you enjoyed this video and would like your own custom math animation. \n Email me at jacob@lynncode.com for a free quote!', font_size=30, alignment='center')
        promo[1][9:27].set_color(YELLOW)

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

        tex1 = MathTex(r'\left(\frac{\text {area of circle}}{\text {area of square}}\right)=', r'\frac{\pi r^{2}}{',r'(2 r)^{2}}')
        # tex1.next_to(square, buff=LARGE_BUFF,aligned_edge=UP)
        tex1.shift(RIGHT*3)
        tex2 = MathTex(r'\left(\frac{\text {area of circle}}{\text {area of square}}\right)=', r'\frac{\pi r^{2}}{',r'4 r^{2}}')
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
        
        def gen_2d_points():
            circle_count = 0
            square_count = 0
            
            for i in range(num_of_points):
                ith_position = positions_2d[i, :]
                ith_color = RED
                dist_from_origin = np.linalg.norm(ith_position - ORIGIN)
                if dist_from_origin > circle.radius:
                    ith_color = BLUE
                if i and ith_color == RED:
                    circle_count += 1
                elif i:
                    square_count += 1
                ratio = i if not i else circle_count/(square_count + circle_count) 

                dots_2d.add(Dot(radius=DEFAULT_SMALL_DOT_RADIUS,
                                point=ith_position, 
                                color=ith_color))

                all_values.add(VGroup(Integer(circle_count, color=RED),
                                      Integer(circle_count, color=RED),
                                      Integer(square_count, color=BLUE),
                                      DecimalNumber(4 * ratio, num_decimal_places=4, color=YELLOW)))
            return (dots_2d, all_values)

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

        self.play(shapes.animate.shift(LEFT*3),
                    line_group.animate.shift(LEFT*3))                                
        self.play(FadeOut(explanation_1))
        # self.add_fixed_in_frame_mobjects(tex1)
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
        points, values = gen_2d_points()

        initial_nums = MathTex(r'\left(\,\frac{\qquad0\qquad}{0\,\,\,\,+\,\,\,0}\,\right) 0.0000').next_to(cdot)
        initial_nums[0][1].set_color(RED)
        initial_nums[0][3].set_color(RED)
        initial_nums[0][5].set_color(BLUE)
        initial_nums[0][7:].set_color(YELLOW).shift(RIGHT*0.6)

        for i in range(num_of_points):
            values[i][0].move_to(initial_nums[0][1])
            values[i][1].move_to(initial_nums[0][3])
            values[i][2].move_to(initial_nums[0][5])
            values[i][3].move_to(initial_nums[0][7:])

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
        a = AnimationGroup(FadeOut(initial_nums[0][1], initial_nums[0][3], initial_nums[0][5], initial_nums[0][7:], run_time=0.1),
                                ShowIncreasingSubsets(points.shift(LEFT*3)),
                                ShowSubmobjectsOneByOne(values), run_time=10)
        self.play(LaggedStart(a, Write(explanation_5), lag_ratio=0.3))

        self.wait(2)
        # self.play(FadeOut(explanation_5, nums, cdot,  tex1[0][-1] ))

        points_and_shapes = AnimationGroup(points.animate.shift(RIGHT*3),
                                           shapes.animate.shift(RIGHT*3))

        self.play(LaggedStart(FadeOut(
            explanation_5,
            initial_nums[0][0],  # Left parenthesis and fraction bar
            initial_nums[0][2],  # Plus symbol
            initial_nums[0][4],  # Right parenthesis
            initial_nums[0][6],  # Approximation symbol
            cdot,                # Multiplication dot
            values[-1],
            tex1[2][0],
            tex1[0][-1],         # Pi symbol
            ), 
            points_and_shapes, 
            FadeOut(points),lag_ratio=0.6),          
        run_time=2)

        # self.play(FadeOut(points))

        # mobjects_not_fading = VGroup(points, shapes)
        # self.play(FadeOut(self.mobjects - mobjects_not_fading))
  
        self.wait()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"\033[94mRender time: {elapsed_time:.2f} seconds")

class MonteCarlo3D(ThreeDScene):

    def construct(self):

        num_of_points = 5

        circle = Circle(radius=2)
        square = Square(side_length=4, color=BLUE_C).move_to(circle)
        
        explanation = Paragraph('Next lets extend our analysis into the 3rd dimension!', font_size=30, alignment='center').next_to(circle, UP*3)
        explanation_1 = Paragraph('Now we are interested in the ratio\n of the volumes of a sphere and a cube', font_size=30, alignment='center').next_to(circle, UP*3) 
        explanation_2 = MathTex(r'\text{Once again, we simplify and solve for } \pi').next_to(circle, UP*3)    
        explanation_3 = Paragraph('Now we can use a Monte Carlo Simulation\n to approximate the volumes of the shapes \n by randomly plotting points within the cube',font_size=30, alignment='center').next_to(circle,UP*2) 
        explanation_4 = MathTex(r'\text{Evaluating the full expression allows us to approximate } \pi!').next_to(circle, UP*3)
        explanation_5 = Paragraph('The more points we plot \n the more accurate our approximation becomes!', font_size=30, alignment='center').next_to(circle,UP*3)

        vol_over_vol_text = MathTex(r'\left(\frac{\text {volume of sphere}}{\text {volume of cube}}\right)=').shift(RIGHT*3.2)
        vol_over_vol_num = MathTex(r'\frac{4}{3}\pi r^3').shift(RIGHT*3.2)
        vol_over_vol_den = MathTex(r'(2r)^{3}')

        vol_over_vol_text = MathTex(r'\left(\frac{\text {volume of sphere}}{\text {volume of cube}}\right)=')
        vol_over_vol_num = MathTex(r'\frac{4}{3}\pi r^3').next_to(vol_over_vol_text).shift(UP*0.65)
        vol_over_vol_den = MathTex(r'(2r)^{3}').next_to(vol_over_vol_num, DOWN)
        frac_line = Line(vol_over_vol_den.get_corner(UR), vol_over_vol_den.get_corner(UL)).shift(UP*0.1).set_opacity(0.65)

        eq = VGroup(vol_over_vol_num, vol_over_vol_den,vol_over_vol_text, frac_line).shift(RIGHT*3.2)

        cdot = MathTex('\cdot').next_to(vol_over_vol_text,LEFT, buff=SMALL_BUFF)
        initial_nums_all_zeros = MathTex(r'\left(\,\frac{\qquad0\qquad}{0\,\,\,\,+\,\,\,0}\,\right) 0.0000').next_to(cdot, RIGHT)
        pts_over_pts = MathTex(r'\left(\frac{\text {pts in sphere}}{\text {total pts in cube}}\right)',                                                            
                            font_size=48).next_to(cdot, buff=SMALL_BUFF)
        vol_over_vol_simplified = MathTex(r'\left(\frac{\text {volume of sphere}}{\text {volume of cube}}\right)=', r'\frac{\pi r^{3}}{',r'8 r^{3}}').move_to(vol_over_vol_text)
        
        r_cancel_num = Line(vol_over_vol_text[1][2].get_corner(UR), vol_over_vol_text[1][1].get_corner(DL), color=YELLOW)
        r_cancel_den = Line(vol_over_vol_simplified[-1].get_corner(UR), vol_over_vol_simplified[-1][1].get_corner(DL), color=YELLOW)
        black_square = Square(0.6, 
                            color=BLACK,         
                            fill_opacity=1).next_to(vol_over_vol_text, RIGHT)
        
        self.add_fixed_in_frame_mobjects(vol_over_vol_text, cdot, initial_nums_all_zeros, pts_over_pts, explanation, explanation_2, explanation_3, explanation_4, r_cancel_num, r_cancel_den, black_square)
        self.remove(vol_over_vol_text, cdot, initial_nums_all_zeros, pts_over_pts, explanation,explanation_2,explanation_3,explanation_4, r_cancel_num, r_cancel_den,  black_square)
        
        radius = Line(circle.get_center(), circle.get_edge_center(RIGHT))
        r = MathTex('r').next_to(radius, UP)
        ref_line = Line(circle.get_edge_center(DOWN), circle.get_corner(DR)).shift(DOWN*MED_SMALL_BUFF)
        reverse_line = Line(circle.get_edge_center(DOWN), circle.get_corner(DL)).shift(DOWN*MED_SMALL_BUFF)
        two_r = MathTex('2r').move_to(circle.get_edge_center(DOWN)).shift(DOWN*MED_LARGE_BUFF)

        radius_copy = radius.copy()
        line_group = VGroup(radius,r,ref_line,reverse_line,two_r)

        sphere = Sphere(radius=2, fill_opacity=0.1).set_color(RED).rotate(90 * DEGREES, axis=RIGHT, about_point=ORIGIN)
        cube = Cube(side_length=4, fill_opacity=0.1, stroke_width=1, stroke_color=BLUE_C)

        shapes = VGroup(circle, square)

        # tex1.next_to(square, buff=LARGE_BUFF,aligned_edge=UP)
        # vol_over_vol.shift(RIGHT*3)
        # black_square = Square(0.6, 
        #                         color=BLACK,         
        #                     fill_opacity=1).next_to(vol_over_vol, RIGHT)
        # vol_over_vol_simplified.move_to(vol_over_vol)

        # zeros = np.zeros((num_of_points, 1))
        positions_3d = square.side_length * np.random.random_sample((num_of_points, 3)) - square.side_length / 2
        # positions_3d = np.append(positions_3d, zeros, axis=1)
        
        dots_3d = VGroup()
        all_values = VGroup()

        def gen_3d_points():
            sphere_count = 0
            cube_count = 0

            for i in range(num_of_points): 
                ith_position = positions_3d[i, :]
                ith_color = RED
                dist_from_origin = np.linalg.norm(ith_position - ORIGIN)
                if dist_from_origin > circle.radius:
                    ith_color = BLUE
                if i and ith_color == RED:
                    sphere_count += 1
                elif i:
                    cube_count += 1
                ratio = sphere_count / (cube_count + sphere_count) if (cube_count + sphere_count) > 0 else 0

                dots_3d.add(Dot3D(radius=DEFAULT_SMALL_DOT_RADIUS,
                                point=ith_position, 
                                color=ith_color))

                all_values.add(VGroup(Integer(sphere_count, color=RED),
                                      Integer(sphere_count, color=RED),
                                      Integer(cube_count, color=BLUE),
                                      DecimalNumber(8 * ratio, num_decimal_places=4, color=YELLOW)))
            return (dots_3d, all_values)

        
        self.add(shapes)
        self.play(Write(explanation))
                
        self.wait()
        self.play(FadeOut(explanation))
        self.play(Succession(Create(radius),
                                FadeIn(r)))
        self.play(Succession(TransformFromCopy(radius,ref_line),
                                Create(reverse_line),
                                FadeIn(two_r)))
        self.wait()
        self.play(Write(explanation_1))
        self.wait()
        self.play(FadeOut(explanation_1))

        # self.move_camera(phi=-30 * DEGREES, theta=-160 * DEGREES, gamma=-90 * DEGREES) 
        self.move_camera(phi=-40 * DEGREES, theta=-160 * DEGREES, gamma=-80 * DEGREES) 
        
        self.play(Create(sphere))
        self.play(GrowFromCenter(cube[0]),
                GrowFromCenter(cube[1]),            
                GrowFromCenter(cube[2]),
                GrowFromCenter(cube[3]),
                GrowFromCenter(cube[4]),
                GrowFromCenter(cube[5]))
        # self.add_fixed_in_frame_mobjects(vol_over_vol,explanation,explanation_2,explanation_3,explanation_4, line1, line2, cdot)
        # self.remove(vol_over_vol, explanation,explanation_2,explanation_3,explanation_4, line1, line2, cdot)
        self.wait()
        self.move_camera(zoom=0.9,frame_center=[4.5,1.5,-1.5]) #x=4,y=0.7
        # self.play(cube.animate.shift(OUT*3*LEFT))


        # self.play(cube.animate.shift(OUT * LEFT * 20))
        self.play(Write(vol_over_vol_text))
        self.wait()
        self.play(Write(explanation_2))
        self.wait()
        self.play(FadeOut(explanation_2))
        self.play(Indicate(vol_over_vol_text[2][0]),Indicate(vol_over_vol_text[2][3:]),run_time=2)

        # self.add_fixed_in_frame_mobjects(black_square)
        # self.remove(black_square)      

        self.play(Transform(vol_over_vol_text[2][1], vol_over_vol_simplified[2][0]),
                Transform(vol_over_vol_text[2:],vol_over_vol_simplified[2:]))
        self.wait(0.5)
        self.play(Create(r_cancel_num),Create(r_cancel_den))
        self.wait(0.5)
        self.play(FadeOut(r_cancel_num,r_cancel_den, vol_over_vol_text[1][1:3], vol_over_vol_text[2][2:], r, two_r, radius, ref_line, reverse_line),
                            black_square.animate.shift(LEFT*0.75))
        self.wait(0.5)

        # Animate 8 vol_over_vol[2][0] to left side of equation.
        # Fade in cdot
        # Animate pi (vol_over_vol[1][0]) to right of equation
        self.play(LaggedStart(vol_over_vol_text[2][0].animate.next_to(cdot, LEFT, buff=SMALL_BUFF),
                            FadeIn(cdot),
                            vol_over_vol_text[1][0].animate.next_to(vol_over_vol_text[0],RIGHT, buff=MED_SMALL_BUFF),
                            LaggedStart(FadeOut(vol_over_vol_text[1][3]),
                                        FadeOut(black_square), run_time=2, lag_ratio=1)
                            ), runtime=2)
                            
  
        self.wait()
        pts_over_pts[0][1:12].set_color(RED)
        pts_over_pts[0][13:-1].set_color_by_gradient(RED,BLUE)
        self.wait(0.5)
        self.play(Write(explanation_3))
        self.wait(2)
        self.play(FadeOut(explanation_3))
        # self.add_fixed_in_frame_mobjects(pts_over_pts.shift(RIGHT))
        # self.add_fixed_in_frame_mobjects(approx_equal.next_to(pts_over_pts, buff=SMALL_BUFF))
        # self.remove(pts_over_pts, approx_equal)


        approx = MathTex(r'\approx')
        self.add_fixed_in_frame_mobjects(approx.next_to(pts_over_pts))
        self.remove(approx)
        # self.remove(approx)
        
        # # THIS IS WHERE I AM GOING WRONG
        # self.play(FadeOut(vol_over_vol[0]),
        #           FadeIn(pts_over_pts),
        #         #   vol_over_vol[1][0].animate.next_to(vol_over_vol[0][-1]),
        #           FadeIn(approx)
        #          )
        
   
        self.play(ReplacementTransform(vol_over_vol_text[0][0],pts_over_pts[0][0]),
                  ReplacementTransform(vol_over_vol_text[0][1:15], pts_over_pts[0][1:12]),
                  ReplacementTransform(vol_over_vol_text[0][15], pts_over_pts[0][12]),
                  ReplacementTransform(vol_over_vol_text[0][16:28], pts_over_pts[0][13:27]),
                  ReplacementTransform(vol_over_vol_text[0][28], pts_over_pts[0][27]),
                  )

        self.wait(2)

        initial_nums_all_zeros[0][1].set_color(RED)
        initial_nums_all_zeros[0][3].set_color(RED)
        initial_nums_all_zeros[0][5].set_color(BLUE)
        initial_nums_all_zeros[0][7:].set_color(YELLOW).shift(RIGHT*0.6)

        # self.add_fixed_in_frame_mobjects(initial_nums_all_zeros.shift(RIGHT))
        # self.remove(initial_nums_all_zeros)

        self.play(ReplacementTransform(pts_over_pts[0][0], initial_nums_all_zeros[0][0]),
                ReplacementTransform(pts_over_pts[0][1:12], initial_nums_all_zeros[0][1]),
                ReplacementTransform(pts_over_pts[0][12], initial_nums_all_zeros[0][2]),
                ReplacementTransform(pts_over_pts[0][13:21], initial_nums_all_zeros[0][3]),
                ReplacementTransform(pts_over_pts[0][21:-1], initial_nums_all_zeros[0][5]),
                ReplacementTransform(pts_over_pts[0][-1], initial_nums_all_zeros[0][6]),
                FadeOut(vol_over_vol_text[1][0]),
                FadeOut(vol_over_vol_text[0][29]),
                FadeIn(approx.next_to(initial_nums_all_zeros[0][7], LEFT, buff=MED_SMALL_BUFF)),
                FadeIn(initial_nums_all_zeros[0][7:]),
                FadeIn(initial_nums_all_zeros[0][4]),
                cdot.animate.next_to(initial_nums_all_zeros, LEFT, buff=SMALL_BUFF*1.7),
                vol_over_vol_text[2][0].animate.next_to(cdot, LEFT, buff=SMALL_BUFF),
                # vol_over_vol[0][-1].animate.next_to(initial_nums_all_zeros[0][6]),
                )
        
        self.play(Write(explanation_4))
        self.wait()

        self.play(FadeOut(explanation_4))

        points3d, values3d = gen_3d_points()

        for i in range(num_of_points):
            values3d[i][0].move_to(initial_nums_all_zeros[0][1])
            values3d[i][1].move_to(initial_nums_all_zeros[0][3])
            values3d[i][2].move_to(initial_nums_all_zeros[0][5])
            values3d[i][3].move_to(initial_nums_all_zeros[0][7:])  

        self.add_fixed_in_frame_mobjects(values3d)
        self.remove(values3d)

        a = AnimationGroup(FadeOut(initial_nums_all_zeros[0][1], initial_nums_all_zeros[0][3], initial_nums_all_zeros[0][5], initial_nums_all_zeros[0][7:], run_time=0.1),
                                ShowIncreasingSubsets(points3d),
                                ShowSubmobjectsOneByOne(values3d), run_time=10)
        
        self.play(LaggedStart(a, Write(explanation_5), lag_ratio=0.3))

        self.wait()
        self.play(FadeOut(*self.mobjects))
        self.wait()

        
        # self.play(ShowIncreasingSubsets(gen_3d_points().shift(LEFT*2)
        self.wait()

class CombinedScene(ThreeDScene):
        def construct(self):
            MonteCarlo2D.construct(self)
            MonteCarlo3D.construct(self)

CombinedScene().render()
