import os

from manim import *
from numpy._core import cos


class question_BC(ThreeDScene):
    def construct(self):
        # self.next_section(skip_animations=True)
        eq1 = Tex("$f(x)=\\frac{1}{x+2}$", font_size=36).shift(UP * 3.3 + RIGHT * 2.55)
        question_bc = (
            VGroup(
                Tex(
                    r"Consider the graph of the function $f$ given by $\hspace{1.71cm}$, as shown",
                    font_size=36,
                ),
                Tex(
                    r"in the figure. Let $R$ be the region bounded by the graph of $f$, the x- and",
                    font_size=36,
                ),
                Tex(r"y-axes, the vertical line x=k, where $k\geq 0.$", font_size=36),
            )
            .arrange(DOWN, aligned_edge=LEFT)
            .to_edge(UP)
        )
        self.play(Write(question_bc), Write(eq1))
        self.wait(2)

        axes = ThreeDAxes(
            x_range=[0, 5, 1],
            y_range=[0, 1.1, 1],
            z_range=[0, 1.1, 1],
            x_length=7,
            y_length=7,
            z_length=7,
        )
        axes.add_coordinates()
        axes.shift(DOWN * 0.7).scale(0.7)
        self.play(Write(axes), FadeOut(axes.z_axis), run_time=2)

        graph = axes.plot(
            lambda x: 1 / (x + 2), color="GREEN", discontinuities=[-2], dt=0.1
        )
        graphR = axes.plot(
            lambda x: 1 / (x + 2),
            color="RED",
            discontinuities=[-2],
            dt=0.1,
            x_range=[0, 1],
        )
        graphS = axes.plot(
            lambda x: 1 / (x + 2),
            color="GREEN",
            discontinuities=[-2],
            dt=0.1,
            x_range=[1, 5],
        )

        k_tracker = ValueTracker(1)

        line = always_redraw(
            lambda: axes.get_vertical_line(
                axes.c2p(k_tracker.get_value(), 1.1, 0),
                color=YELLOW,
                line_func=Arrow,
                line_config={"buff": 0},
            )
        )
        line_label = always_redraw(
            lambda: Tex("$x=k$", color=YELLOW).next_to(line, RIGHT, buff=0.1)
        )

        areaR = always_redraw(
            lambda: axes.get_area(
                graph, x_range=[0, k_tracker.get_value()], color="RED", opacity=0.6
            )
        )
        areaS = always_redraw(
            lambda: axes.get_area(
                graph,
                x_range=[k_tracker.get_value(), 5],
                color="GREEN",
                opacity=0.6,
            )
        )
        labelR = Tex("$R$", color=RED)
        labelS = Tex("$S$", color=GREEN)

        always_redraw(lambda: labelR.move_to(areaR.get_center()).shift(DOWN * 0.7))
        always_redraw(lambda: labelS.move_to(areaR).shift(RIGHT * 2 + DOWN * 0.7))

        graphGroup = VGroup(
            axes, graph, areaR, areaS, labelR, labelS, line_label, graphR, graphS
        )

        self.play(Create(graph), Create(line), Write(line_label))
        self.play(Create(areaR), Create(areaS))
        self.play(Write(labelR), Write(labelS))
        self.play(k_tracker.animate.set_value(3))
        self.wait(0.3)
        self.play(k_tracker.animate.set_value(1))
        self.wait(2)

        labelR.clear_updaters()
        labelS.clear_updaters()
        areaR.clear_updaters()
        areaS.clear_updaters()
        line_label.clear_updaters()
        self.play(
            FadeOut(question_bc),
            graphGroup.animate.scale(0.67).to_corner(UR).shift(DOWN),
            eq1.animate.to_edge(UR).set_color(BLUE),
        )

        self.wait(2)

        # Part A
        part_a = Tex(r"(a) Find the area of $R$ in terms of $k$.", font_size=40)
        part_a.shift(LEFT * 0.5)
        self.play(Write(part_a))
        self.play(part_a.animate.to_corner(UL))
        part_a_0 = Tex(r"$$A_{R}=\int_0^k f(x)dx$$", font_size=36, color=PURPLE_A)
        self.play(Write(part_a_0))
        self.play(part_a_0.animate.to_edge(UP, buff=1.4))
        self.wait()

        part_a_1 = Tex(r"$$=\int_0^k \frac{1}{x+2}dx$$", font_size=36, color=PURPLE_A)

        part_a_1.next_to(part_a_0, DOWN, buff=0.5)
        self.play(Write(part_a_1))
        self.wait()

        part_a_2 = Tex(r"$$=\left[\ln(x+2)\right]_0^k$$", font_size=36, color=PURPLE_A)
        part_a_2.next_to(part_a_1, DOWN, buff=0.5)
        self.play(Write(part_a_2))
        self.wait()

        part_a_3 = Tex(r"$$=\ln(k+2)-\ln(2)$$", font_size=36, color=PURPLE_A)
        part_a_3.next_to(part_a_2, DOWN, buff=0.5)
        self.play(Write(part_a_3))
        self.wait()

        part_a_box = SurroundingRectangle(part_a_3, color=WHITE, buff=0.2)
        self.play(Create(part_a_box))

        self.wait(2)
        part_a_group = VGroup(
            part_a, part_a_0, part_a_1, part_a_2, part_a_3, part_a_box
        )
        self.play(FadeOut(part_a_group))
        self.wait(2)

        self.play(
            graphGroup.animate.scale(1.7).move_to(ORIGIN).shift(DOWN * 0.1),
            FadeOut(eq1),
        )

        # Part B
        part_b = (
            VGroup(
                Tex(
                    r"$\text{(b) Find the volume of the solid generated when }R\text{ is revolved}$",
                    font_size=36,
                ),
                Tex(r"$\text{around the x-axis in terms of }k.$", font_size=36),
            )
            .arrange(DOWN, aligned_edge=LEFT)
            .to_edge(UL)
        )
        self.play(Write(part_b))
        rotating_surface_r = Surface(
            lambda u, v: axes.c2p(u, 1 / (u + 2) * np.cos(v), 1 / (u + 2) * np.sin(v)),
            u_range=[0, 1],
            v_range=[0, TAU],
            checkerboard_colors=[RED, RED],
            fill_opacity=0.5,
            resolution=(10, 10),
        )

        self.play(
            Rotate(graphR, axis=RIGHT, angle=TAU, about_point=axes.c2p(0, 0, 0)),
            Rotate(areaR, axis=RIGHT, angle=TAU, about_point=axes.c2p(0, 0, 0)),
            run_time=1,
            rate_func=linear,
        )
        self.play(
            Rotate(graphR, axis=RIGHT, angle=PI, about_point=axes.c2p(0, 0, 0)),
            Rotate(areaR, axis=RIGHT, angle=PI, about_point=axes.c2p(0, 0, 0)),
            FadeIn(rotating_surface_r),
            run_time=0.5,
            rate_func=linear,
        )
        self.play(
            Rotate(graphR, axis=RIGHT, angle=3 * PI, about_point=axes.c2p(0, 0, 0)),
            Rotate(areaR, axis=RIGHT, angle=3 * PI, about_point=axes.c2p(0, 0, 0)),
            run_time=1.5,
            rate_func=linear,
        )
        self.wait()

        self.wait()
        x_val = ValueTracker(0)

        def func(x):
            return 1 / (x + 2)

        circle_graph = always_redraw(
            lambda: ParametricFunction(
                lambda t: axes.c2p(
                    x_val.get_value(),
                    func(x_val.get_value()) * np.cos(t),
                    func(x_val.get_value()) * np.sin(t),
                ),
                t_range=[0, 2 * PI],
                color=YELLOW,
                stroke_width=5,
            )
        )

        self.play(FadeIn(circle_graph))
        self.play(x_val.animate.set_value(1))
        self.play(x_val.animate.set_value(0.5))
        circle_graph.clear_updaters()

        graphGroup_b = VGroup(
            axes,
            graph,
            areaR,
            areaS,
            labelR,
            labelS,
            line_label,
            graphR,
            graphS,
            circle_graph,
            rotating_surface_r,
        )

        self.play(graphGroup_b.animate.scale(0.5).to_corner(UR).shift(DOWN))

        circle_diagram = Circle(radius=1.4, color=YELLOW)
        self.play(Transform(circle_graph, circle_diagram))
        radius_line = Line(
            start=circle_diagram.get_center(),
            end=circle_diagram.point_at_angle(40 * DEGREES),
            color=YELLOW,
        )
        radius_label = (
            Tex("$r$").next_to(radius_line, LEFT).shift(UP * 0.3 + RIGHT * 0.6)
        )
        self.play(Create(radius_line), Write(radius_label))

        part_b_0 = Tex(r"$$A=\pi \cdot r^2$$", color=PURPLE_A)
        part_b_0.next_to(circle_diagram, DOWN, buff=0.5)
        self.play(Write(part_b_0))
        part_b_1 = Tex(r"$$r=f(x)=\frac{1}{x+2}$$", color=PURPLE_A).next_to(
            part_b_0, DOWN, buff=0.2
        )
        self.play(Write(part_b_1))

        b_group_0 = VGroup(radius_line, circle_diagram, radius_label, circle_graph)

        part_b_2 = Tex(r"$$A=\pi\cdot\frac{1}{(x+2)^2}$$", font_size=36, color=PURPLE_A)
        part_b_3 = Tex(
            r"$$V_R=\int_0^k A(x)dx=\pi\int_0^k \frac{1}{(x+2)^2}dx$$",
            font_size=36,
            color=PURPLE_A,
        )
        part_b_3.next_to(part_b_2, DOWN, buff=0.5)

        self.play(
            FadeOut(b_group_0),
            part_b_0.animate.to_edge(UL, buff=2),
        )
        self.play(part_b_1.animate.next_to(part_b_0, DOWN))
        self.wait()
        part_b_2.next_to(part_b_1, DOWN, buff=0.5)
        self.play(Write(part_b_2))
        part_b_3.next_to(part_b_2, DOWN, buff=0.5)
        self.play(Write(part_b_3))
        self.wait()

        self.play(
            FadeOut(part_b_0),
            FadeOut(part_b_1),
            FadeOut(part_b_2),
            part_b_3.animate.to_edge(UL, buff=2),
        )

        self.wait()

        part_b_4 = Tex(
            r"$$=-\pi\left[\frac{1}{x+2}\right]^k_0$$",
            font_size=36,
            color=PURPLE_A,
        )
        part_b_4.next_to(part_b_3, DOWN, buff=0.5)
        self.play(Write(part_b_4))
        self.wait()

        part_b_5 = Tex(
            r"$$=-\pi \left( \frac{1}{k+2} - \frac{1}{2} \right)$$",
            font_size=36,
            color=PURPLE_A,
        )
        part_b_5.next_to(part_b_4, DOWN, buff=0.5)
        self.play(Write(part_b_5))
        self.wait()

        part_b_6 = Tex(
            r"$$=\frac{\pi}{2} - \frac{\pi}{k+2}$$",
            font_size=36,
            color=PURPLE_A,
        )
        part_b_6.next_to(part_b_5, DOWN, buff=0.5)
        self.play(Write(part_b_6))
        self.wait()

        part_b_box = SurroundingRectangle(part_b_6, color=WHITE, buff=0.2)
        self.play(Create(part_b_box))

        self.wait(2)

        self.play(
            FadeOut(part_b_3),
            FadeOut(part_b_4),
            FadeOut(part_b_5),
            FadeOut(part_b_6),
            FadeOut(part_b_box),
            FadeOut(part_b),
        )

        # Part C

        graphGroup_c1 = VGroup(
            axes,
            graph,
            areaR,
            areaS,
            labelR,
            labelS,
            line_label,
            graphR,
            graphS,
            rotating_surface_r,
        )
        self.play(
            graphGroup_c1.animate.scale(1.7).move_to(ORIGIN).shift(DOWN * 1.5),
            FadeOut(eq1),
        )

        part_c = Tex(
            r"\begin{minipage}{17cm}(c) Let $S$ be the unbounded region in the first quadrant to the right of the vertical line $x = k$ and below the graph of $f$, as shown in the figure. Find all values of $k$ such that the volume of the solid generated when $S$ is revolved about the x-axis is equal to the volume of the solid found in part (b).\end{minipage}",
            font_size=30,
        ).to_corner(UL)

        self.play(Write(part_c), play_time=2)
        rotating_surface_s = Surface(
            lambda u, v: axes.c2p(u, 1 / (u + 2) * np.cos(v), 1 / (u + 2) * np.sin(v)),
            u_range=[1, 5],
            v_range=[0, TAU],
            checkerboard_colors=[GREEN, GREEN],
            fill_opacity=0.5,
            resolution=(10, 10),
        )

        self.play(
            Rotate(graphS, axis=RIGHT, angle=TAU, about_point=axes.c2p(0, 0, 0)),
            Rotate(areaS, axis=RIGHT, angle=TAU, about_point=axes.c2p(0, 0, 0)),
            run_time=1,
            rate_func=linear,
        )
        self.play(
            Rotate(graphS, axis=RIGHT, angle=PI, about_point=axes.c2p(0, 0, 0)),
            Rotate(areaS, axis=RIGHT, angle=PI, about_point=axes.c2p(0, 0, 0)),
            FadeIn(rotating_surface_s),
            run_time=0.5,
            rate_func=linear,
        )
        self.play(
            Rotate(graphS, axis=RIGHT, angle=3 * PI, about_point=axes.c2p(0, 0, 0)),
            Rotate(areaS, axis=RIGHT, angle=3 * PI, about_point=axes.c2p(0, 0, 0)),
            run_time=1.5,
            rate_func=linear,
        )
        self.wait()

        self.wait()
        x_val_c = ValueTracker(1)

        circle_graph_c = always_redraw(
            lambda: ParametricFunction(
                lambda t: axes.c2p(
                    x_val_c.get_value(),
                    func(x_val_c.get_value()) * np.cos(t),
                    func(x_val_c.get_value()) * np.sin(t),
                ),
                t_range=[0, 2 * PI],
                color=YELLOW,
                stroke_width=5,
            )
        )

        self.play(FadeIn(circle_graph_c))
        self.play(x_val_c.animate.set_value(5))
        self.play(x_val_c.animate.set_value(1.5))
        circle_graph_c.clear_updaters()

        graphGroup_c2 = VGroup(
            axes,
            graph,
            areaR,
            areaS,
            labelR,
            labelS,
            line_label,
            graphR,
            graphS,
            rotating_surface_r,
            rotating_surface_s,
            circle_graph_c,
        )

        self.play(graphGroup_c2.animate.scale(0.5).to_corner(UR).shift(DOWN))

        self.play(Transform(circle_graph_c, circle_diagram))
        radius_line_c = Line(
            start=circle_diagram.get_center(),
            end=circle_diagram.point_at_angle(40 * DEGREES),
            color=YELLOW,
        )
        radius_label_c = (
            Tex("$r$").next_to(radius_line, LEFT).shift(UP * 0.3 + RIGHT * 0.6)
        )
        self.play(Create(radius_line_c), Write(radius_label_c))

        part_c_0 = Tex(r"$$A=\pi \cdot r^2$$", color=PURPLE_A)
        part_c_0.next_to(circle_diagram, DOWN, buff=0.5)

        self.play(Write(part_c_0))

        part_c_1 = Tex(r"$$r=f(x)=\frac{1}{x+2}$$", color=PURPLE_A).next_to(
            part_c_0, DOWN, buff=0.2
        )
        self.play(Write(part_c_1))

        c_group_0 = VGroup(
            radius_line_c, circle_diagram, radius_label_c, circle_graph_c
        )

        part_c_2 = Tex(r"$$A=\pi\cdot\frac{1}{(x+2)^2}$$", font_size=36, color=PURPLE_A)
        part_c_3 = Tex(
            r"$$V_S=\int_k^\infty A(x)dx=\pi\int_k^\infty \frac{1}{(x+2)^2}dx$$",
            font_size=36,
            color=PURPLE_A,
        )
        part_c_3.next_to(part_c_2, DOWN, buff=0.5)

        self.play(
            FadeOut(c_group_0),
            part_c_0.animate.to_edge(UL, buff=2),
        )
        self.play(part_c_1.animate.next_to(part_c_0, DOWN))
        self.wait()
        part_c_2.next_to(part_c_1, DOWN, buff=0.5)
        self.play(Write(part_c_2))

        part_c_3.next_to(part_c_2, DOWN, buff=0.5).shift(RIGHT)
        self.play(Write(part_c_3))
        self.wait()

        self.play(
            FadeOut(part_c_0),
            FadeOut(part_c_1),
            FadeOut(part_c_2),
            part_c_3.animate.to_edge(UL, buff=2),
        )

        part_c_4 = Tex(
            r"$$=\pi \lim_{t\to \infty} \int_k^t \frac{1}{(x+2)^2}=\pi \lim_{t\to\infty}\left[ \frac{-1}{x+2} \right]_k^t$$",
            font_size=36,
            color=PURPLE_A,
        )

        part_c_4.next_to(part_c_3, DOWN, buff=0.5).shift(RIGHT)
        self.play(Write(part_c_4))
        self.wait()

        part_c_5 = Tex(
            r"$$=\pi \lim_{t\to\infty}\left[ \frac{-1}{t+2} \right]+\frac{\pi}{k+2}$$",
            font_size=36,
            color=PURPLE_A,
        )

        part_c_5.next_to(part_c_4, DOWN, buff=0.5)
        self.play(Write(part_c_5))
        self.wait()

        part_c_6 = Tex(
            r"$$=\frac{\pi}{k+2}$$",
            font_size=36,
            color=PURPLE_A,
        )

        part_c_6.next_to(part_c_5, DOWN, buff=0.5)
        self.play(Write(part_c_6))
        self.wait()

        self.play(
            FadeOut(part_c_3),
            FadeOut(part_c_4),
            FadeOut(part_c_5),
            part_c_6.animate.to_edge(UL, buff=2),
        )

        part_c_7 = Tex(r"$$V_S$$", font_size=36, color=PURPLE_A).move_to(part_c_6, LEFT)

        self.play(Write(part_c_7), part_c_6.animate.shift(RIGHT * 0.5))
        self.wait(2)

        part_c_8 = Tex(
            r"$$V_S = V_R$$",
            font_size=36,
            color=PURPLE_A,
        )

        part_c_8.next_to(part_c_7, DOWN, buff=0.5).shift(RIGHT)
        self.play(Write(part_c_8))
        self.wait()

        part_c_9 = Tex(
            r"$$\frac{\pi}{k+2} = \frac{\pi}{2} - \frac{\pi}{k+2}$$",
            font_size=36,
            color=PURPLE_A,
        )

        part_c_9.next_to(part_c_8, DOWN, buff=0.5).shift(RIGHT)
        self.play(Write(part_c_9))
        self.wait()

        part_c_10 = Tex(
            r"$$\frac{1}{k+2} = \frac{1}{2} - \frac{1}{k+2}$$",
            font_size=36,
            color=PURPLE_A,
        )

        part_c_10.next_to(part_c_9, DOWN, buff=0.5)
        self.play(Write(part_c_10))
        self.wait()

        part_c_11 = Tex(
            r"$$\frac{2}{k+2} = \frac{1}{2}$$",
            font_size=36,
            color=PURPLE_A,
        )

        part_c_11.next_to(part_c_10, DOWN, buff=0.5)
        self.play(Write(part_c_11))
        self.wait()

        self.play(
            FadeOut(part_c_6),
            FadeOut(part_c_7),
            FadeOut(part_c_8),
            FadeOut(part_c_9),
            FadeOut(part_c_10),
            part_c_11.animate.to_edge(UL, buff=2),
        )

        part_c_12 = Tex(
            r"$$\frac{k+2}{2} = 2$$",
            font_size=36,
            color=PURPLE_A,
        )

        part_c_12.next_to(part_c_11, DOWN, buff=0.5)
        self.play(Write(part_c_12))
        self.wait()

        part_c_13 = Tex(
            r"$$k = 2$$",
            font_size=36,
            color=PURPLE_A,
        )

        part_c_13.next_to(part_c_12, DOWN, buff=0.5)
        self.play(Write(part_c_13))
        self.wait()

        part_c_box = SurroundingRectangle(part_c_13, color=WHITE, buff=0.2)

        self.play(Create(part_c_box))

        self.wait(2)


class question_AB(Scene):
    def construct(self):
        self.next_section(skip_animations=True)
        x_pi_dict = {
            -2 * PI: r"$-2\pi$",
            # -PI: r"$\hspace{1cm}$",
            # PI: r"$\hspace{1cm}$",
            # 2 * PI: r"$\hspace{1cm}$",
            # 3 * PI: r"$\hspace{1cm}$",
            4 * PI: r"$4\pi$",
        }

        y_pi_dict = {
            # -PI: r"$\hspace{1cm}$",
            # PI: r"$\hspace{1cm}$",
            2
            * PI: r"$2\pi$",
        }

        axes = Axes(
            x_range=[-2 * PI - 3 * PI / 4, 4 * PI + PI * 3 / 4, PI],
            y_range=[-PI / 2, 3 * PI, PI],
            x_length=15,
            y_length=7,
        )

        axes.add_coordinates(x_pi_dict, y_pi_dict)
        axes.shift(DOWN * 0.7).scale(0.7)
        question_AB = Tex(
            r"\begin{minipage}{12cm}Let $g$ be piecewise-linear function defined on $[-2\pi, 4\pi]$ whose graph is given below, and let $\hspace{3.3cm}$. (AB 2011 Form B Question 6)\end{minipage}",
            font_size=36,
        ).to_corner(UL)
        function_f = (
            Tex(
                r"$f(x)=g(x)-\cos\left(\frac{x}{2}\right)$",
                font_size=36,
            )
            .move_to(question_AB, DOWN)
            .shift(DOWN * 0.05 + LEFT * 2.2)
        )

        self.play(
            Write(axes),
            LaggedStart(
                Write(question_AB), Write(function_f), lag_ratio=0.5, run_time=2
            ),
            run_time=2,
        )

        graph1 = axes.plot(
            lambda x: x + 2 * PI,
            color="RED",
            x_range=[-2 * PI, 0],
        )

        graph2 = axes.plot(
            lambda x: -(1 / 2) * x + 2 * PI,
            color="RED",
            x_range=[0, 4 * PI],
        )

        graph_g_label = Tex("$g(x)$", color="RED").move_to(graph2).shift(RIGHT * 1 + UP)

        self.play(Create(graph1))
        self.play(Create(graph2), Write(graph_g_label))

        graph_group1 = VGroup(graph1, graph2, axes)
        question_AB_info = VGroup(graph1, graph2, axes, function_f, graph_g_label)

        self.play(
            FadeOut(question_AB),
            graph_group1.animate.scale(0.4).to_corner(UR).shift(DOWN),
            function_f.animate.to_corner(UR).set_color(BLUE),
            graph_g_label.animate.to_corner(UR).shift(DOWN * 1.5 + LEFT * 0.5),
        )

        self.wait()

        # Part A
        part_a = Tex(
            r"\begin{minipage}{8cm}(a) Find $\int_{-2\pi}^{4\pi} f(x)dx.$ Show the computations that lead to your answer.\end{minipage}",
            font_size=36,
        ).to_corner(UL)

        self.play(Write(part_a))

        part_a_0 = Tex(
            r"$$\int_{-2\pi}^{4\pi} f(x)dx =\int_{-2\pi}^{4\pi} g(x) - \cos\left(\frac{x}{2}\right)dx$$",
            font_size=30,
            color="TEAL",
        ).next_to(part_a, DOWN)
        self.play(Write(part_a_0))
        self.wait()

        # Part A

        part_a_1 = (
            Tex(
                "$$=$$",
                font_size=30,
                color="TEAL",
            )
            .next_to(part_a_0, DOWN, buff=0.5)
            .shift(LEFT)
        )

        part_a_2 = Tex(
            r"$$\int_{-2\pi}^{4\pi} g(x) dx$$",
            font_size=30,
            color="TEAL",
        ).next_to(part_a_1, RIGHT)
        part_a_3 = Tex(
            r"$$- \int_{-2\pi}^{4\pi} \cos\left(\frac{x}{2}\right) dx$$",
            font_size=30,
            color="TEAL",
        ).next_to(part_a_2, RIGHT)
        self.play(Succession(Write(part_a_1), Write(part_a_2), Write(part_a_3)))
        part_a_box_0 = SurroundingRectangle(part_a_2, color=TEAL_B, buff=0.1)
        self.play(Create(part_a_box_0))
        g_integral_group = VGroup(part_a_2, part_a_box_0)

        self.play(
            FadeOut(part_a_0),
            FadeOut(part_a_1),
            FadeOut(part_a_3),
            g_integral_group.animate.next_to(part_a, DOWN).shift(LEFT * 3),
        )
        part_a_4 = (
            Tex(
                "represents the area bounded by $g$ and the x-axis",
                font_size=30,
                color=TEAL,
            )
            .next_to(part_a_2, RIGHT)
            .shift(LEFT * 0.1)
        )

        self.play(FadeOut(part_a_box_0), Write(part_a_4))

        g_area = VGroup(
            axes.get_area(graph1, x_range=[-2 * PI, 0], color=GREEN, opacity=0.7),
            axes.get_area(graph2, x_range=[0, 4 * PI], color=GREEN, opacity=0.7),
        )
        self.play(Create(g_area))

        part_a_5 = Tex(
            r"$$A=\frac{1}{2}bh$$",
            font_size=30,
            color=TEAL,
        ).next_to(part_a_2, DOWN, buff=0.5)
        self.play(Write(part_a_5))

        self.wait()

        # TODO add animations of where the base and height values come from, using the graph
        g_graph_height = axes.get_vertical_line(
            axes.c2p(0, 2 * PI, 0), color=RED, line_func=Line
        )
        g_graph_height.set_stroke(width=8)

        g_graph_base = axes.plot(lambda x: 0, color="RED", x_range=[-2 * PI, 4 * PI])
        g_graph_base.set_stroke(width=8)

        self.play(Create(g_graph_height), Create(g_graph_base))

        g_graph_base_label = MathTex(
            r"\mathbf{b=6\pi}", font_size=30, color=RED
        ).next_to(g_graph_base, DOWN)
        g_graph_height_label = (
            MathTex(r"\mathbf{h=2\pi}", font_size=30, color=RED)
            .next_to(g_graph_height, UP)
            .shift(RIGHT * 0.6 + DOWN * 0.2)
        )

        self.play(Write(g_graph_height_label), Write(g_graph_base_label))

        part_a_6 = Tex(
            r"$$A=\frac{1}{2}\cdot 2\pi \cdot 6\pi$$", font_size=30, color=TEAL
        ).next_to(part_a_5, DOWN, buff=0.5)

        self.play(Write(part_a_6))

        part_a_7 = (
            Tex(r"$$=6\pi ^2$$", font_size=30, color=TEAL)
            .next_to(part_a_6, RIGHT)
            .shift(LEFT * 0.15)
        )
        self.play(Write(part_a_7))

        self.wait()

        self.play(
            FadeOut(part_a_4),
            FadeOut(part_a_5),
            FadeOut(part_a_6),
            FadeOut(g_area),
            FadeOut(g_graph_base),
            FadeOut(g_graph_height),
            FadeOut(g_graph_height_label),
            FadeOut(g_graph_base_label),
            part_a_7.animate.next_to(part_a_2).shift(LEFT * 0.1),
        )

        part_a_8 = (
            MathTex(
                r"\int_{-2\pi}^{4\pi} g(x)dx - \int_{-2\pi}^{4\pi} \cos\left(\frac{x}{2}\right)dx &= 6\pi^2- \\",
                r"&= 6\pi ^2",
                font_size=30,
                color=TEAL,
            )
            .next_to(part_a_7, DOWN, buff=0.5)
            .shift(RIGHT)
        )
        part_a_9 = (
            Tex(
                r"$$\int_{-2\pi}^{4\pi} \cos\left(\frac{x}{2}\right)dx$$",
                font_size=30,
                color=TEAL,
            )
            .next_to(part_a_8, RIGHT)
            .shift(UP * 0.2 + LEFT * 0.2)
        )

        part_a_10 = part_a_9.copy()

        self.play(LaggedStart(Write(part_a_8[0]), Write(part_a_9), lag_ratio=0.8))

        self.play(
            part_a_10.animate.shift(DOWN + RIGHT * 2).scale(0.8).set_color(ORANGE)
        )
        part_a_11 = Tex(
            r"$$ \implies \int_{-2\pi}^{4\pi} \pm \sqrt{\frac{1+\cos x}{2}} dx$$",
            font_size=24,
            color=ORANGE,
        ).next_to(part_a_10, RIGHT)
        self.wait()
        self.play(Write(part_a_11))
        part_a_11_cross = Cross(part_a_11, stroke_color=RED)
        self.play(Create(part_a_11_cross))
        self.wait()
        self.play(FadeOut(part_a_11), FadeOut(part_a_11_cross))
        part_a_12 = (
            MathTex(
                r"\text{Let } u &=\frac{x}{2} \\",
                r"du &= \frac{1}{2} dx \\",
                r"dx &= 2du",
                font_size=24,
                color=ORANGE,
            )
            .next_to(part_a_10, RIGHT)
            .shift(RIGHT)
        )
        self.play(Write(part_a_12[0]))
        self.wait(0.5)
        self.play(Write(part_a_12[1]))
        self.wait(0.5)
        self.play(Write(part_a_12[2]))
        self.wait()

        part_a_13 = MobjectTable(
            [
                [
                    Tex(r"$4\pi$", font_size=24, color=ORANGE),
                    Tex(r"$2\pi$", font_size=24, color=ORANGE),
                ],
                [
                    Tex(r"$-2\pi$", font_size=24, color=ORANGE),
                    Tex(r"$-\pi$", font_size=24, color=ORANGE),
                ],
            ],
            col_labels=[
                Tex("$x$", font_size=24, color=ORANGE),
                Tex("$u$", font_size=24, color=ORANGE),
            ],
            h_buff=0.4,  # Shrinks the horizontal size of each box
            v_buff=0.3,
        ).next_to(part_a_12, DOWN)
        part_a_13.get_horizontal_lines().set_color(ORANGE).set_stroke(width=1.5)
        part_a_13.get_vertical_lines().set_color(ORANGE).set_stroke(width=1.5)
        self.play(Create(part_a_13))
        self.wait()

        part_a_14 = MathTex(
            r" &=2\int_{-\pi}^{2\pi} \cos(u) du  \\",
            r" &= 2[\sin(u)]_{-\pi}^{2\pi} \\",
            r" &= 2\sin(2\pi)-2\sin(-\pi) \\",
            r" &=0",
            font_size=24,
            color=ORANGE,
        ).next_to(part_a_10, DOWN)
        self.play(Write(part_a_14[0]))
        self.wait()
        self.play(Write(part_a_14[1]))
        self.wait()
        self.play(Write(part_a_14[2]))
        self.wait()
        self.play(Write(part_a_14[3]))
        self.wait()

        part_a_15 = (
            Tex("$0$", color=ORANGE, font_size=30)
            .next_to(part_a_8, RIGHT)
            .shift(UP * 0.2 + LEFT * 0.1)
        )
        self.play(Transform(part_a_9, part_a_15))
        self.wait()
        self.play(Write(part_a_8[1]))
        part_a_final_box = SurroundingRectangle(part_a_8[1], color=WHITE, buff=0.2)
        self.play(Create(part_a_final_box))
        self.wait()

        part_a_fade = VGroup(
            part_a,
            part_a_2,
            part_a_7,
            part_a_8,
            part_a_9,
            part_a_10,
            # part_a_11 is already faded out
            part_a_12,
            part_a_13,
            part_a_14,
            part_a_15,
            part_a_final_box,
        )

        self.play(FadeOut(part_a_fade), FadeOut(question_AB_info))

        # Part A: Cos graph verification

        verify_f_integral = Tex(
            r"$$\text{Verify } \int_{-2\pi}^{4\pi} \cos\left(\frac{x}{2}\right)dx$$",
            font_size=40,
        ).to_corner(UL)

        x_pi_dict_2 = {
            -2 * PI: r"$-2\pi$",
            # -PI: r"$\hspace{1cm}$",
            # PI: r"$\hspace{1cm}$",
            # 2 * PI: r"$\hspace{1cm}$",
            # 3 * PI: r"$\hspace{1cm}$",
            4 * PI: r"$4\pi$",
        }
        y_dict_2 = {-1: r"$-1$", 1: r"$1$"}

        axes2 = Axes(
            x_range=[-2 * PI - 3 * PI / 4, 4 * PI + PI * 3 / 4, PI],
            y_range=[-1.5, 1.5, 1],
            x_length=15,
            y_length=7,
        )

        axes2.add_coordinates(x_pi_dict_2, y_dict_2)
        axes2.shift(DOWN * 0.7).scale(0.7)

        graph_cos = axes2.plot(
            lambda x: cos(x / 2),
            color="BLUE",
            x_range=[-2 * PI - 3 * PI / 4, 4 * PI + PI * 3 / 4],
        )

        self.play(Write(axes2), Write(verify_f_integral))
        self.play(Create(graph_cos))

        line_2pi = always_redraw(
            lambda: DashedLine(
                start=axes2.c2p(-2 * PI, -1.5, 0),
                end=axes2.c2p(-2 * PI, 1.5, 0),
                color=YELLOW,
            )
        )
        line_4pi = always_redraw(
            lambda: DashedLine(
                start=axes2.c2p(4 * PI, -1.5, 0),
                end=axes2.c2p(4 * PI, 1.5, 0),
                color=YELLOW,
            )
        )
        self.play(Create(line_4pi), Create(line_2pi), run_time=1)

        cos_area_1 = axes2.get_area(
            graph_cos, x_range=[-2 * PI, -PI], color="RED_E", opacity=0.8
        )
        label_cos_area_1 = (
            Text("-", color="RED", weight="HEAVY")
            .move_to(cos_area_1.get_center())
            .shift(LEFT * 0.3)
        )

        cos_area_2 = axes2.get_area(
            graph_cos, x_range=[-PI, PI], color="GREEN_E", opacity=0.8
        )
        label_cos_area_2 = Text("+", color="GREEN", weight="HEAVY").move_to(
            cos_area_2.get_center()
        )

        cos_area_3 = axes2.get_area(
            graph_cos, x_range=[PI, 3 * PI], color="RED_E", opacity=0.8
        )
        label_cos_area_3 = Text("-", color="RED", weight="HEAVY").move_to(
            cos_area_3.get_center()
        )

        cos_area_4 = axes2.get_area(
            graph_cos, x_range=[3 * PI, 4 * PI], color="GREEN_E", opacity=0.8
        )
        label_cos_area_4 = (
            Text("+", color="GREEN", weight="HEAVY")
            .move_to(cos_area_4.get_center())
            .shift(RIGHT * 0.3)
        )
        # self.next_section(skip_animations=True)

        cos_area_group = VGroup(cos_area_1, cos_area_2, cos_area_3, cos_area_4)
        cos_label_group = VGroup(
            label_cos_area_1, label_cos_area_2, label_cos_area_3, label_cos_area_4
        )
        cos_group_1 = VGroup(cos_area_1, label_cos_area_1)
        cos_group_2 = VGroup(cos_area_2, label_cos_area_2)
        cos_group_3 = VGroup(cos_area_3, label_cos_area_3)
        cos_group_4 = VGroup(cos_area_4, label_cos_area_4)

        self.play(Create(cos_area_group))
        self.play(Write(cos_label_group), FadeOut(verify_f_integral))
        self.play(
            LaggedStart(
                cos_group_2.animate.shift(LEFT + UP * 2.75),
                cos_group_3.animate.shift(UP * 4.32),
                lag_ratio=0.3,
                run_time=1,
            )
        )
        self.play(
            cos_group_3.animate.shift(LEFT * 1.8),  # First, move it completely
            cos_group_2.animate.shift(RIGHT * 2),
        )
        cos_zero_0 = Tex("$0$").move_to(cos_group_2).scale(0.0001)

        self.play(
            cos_group_3.animate.scale(0),  # First, move it completely
            cos_group_2.animate.scale(0),
            cos_zero_0.animate.scale(10000),
        )
        self.play(FadeOut(cos_zero_0))

        self.play(
            cos_group_4.animate.shift(
                LEFT * 4 + UP * 2.75
            ),  # First, move it completely
            cos_group_1.animate.shift(RIGHT * 3.2 + UP * 4.3),
        )
        cos_zero_1 = Tex("$0$").move_to(cos_group_2).scale(0.0001)

        self.play(
            cos_group_1.animate.scale(0),  # First, move it completely
            cos_group_4.animate.scale(0),
            cos_zero_1.animate.scale(10000),
        )
        self.play(FadeOut(cos_zero_1))

        cos_area_eq = Tex(r"$\therefore A=0$").to_edge(UP).shift(LEFT)
        self.play(Write(cos_area_eq))

        self.wait()
        self.play(FadeOut(line_2pi, line_4pi, graph_cos, axes2, cos_area_eq))
        self.wait()

        # Part B

        part_b = Tex(
            r"\begin{minipage}{8cm}(b) Find all x-values in the open interval $(-2\pi,4\pi)$  for which $f$ has a critical point.\end{minipage}",
            font_size=36,
        ).to_corner(UL)
        self.play(LaggedStart(Write(part_b), FadeIn(question_AB_info)))

        part_b_0 = (
            MarkupText(
                f"Critical points are when the derivative is <u>undefined</u> <i>or</i> <u>0</u>.",
                font_size=24,
                color=TEAL,
            )
            .to_corner(UL)
            .shift(DOWN)
        )
        self.play(Write(part_b_0))

        part_b_1 = (
            MathTex(
                r"f(x)&=g(x)-\cos\left(\frac{x}{2}\right) \\",
                r"f'(x)&=g'(x)+\frac{1}{2}\sin\left(\frac{x}{2}\right) \\",
                r"f'(x)&=\begin{cases} 1 + \frac{1}{2}\sin\left(\frac{x}{2}\right) & -2\pi < x < 0 \\ -\frac{1}{2} + \frac{1}{2}\sin\left(\frac{x}{2}\right) & 0 < x < 4\pi \end{cases}",
                font_size=30,
                color=TEAL,
            )
            .to_corner(UL)
            .shift(DOWN * 1.5)
        )
        self.play(Write(part_b_1[0]))
        self.play(Write(part_b_1[1]))
        part_b_2 = (
            Tex(r"$\underline{\text{Slopes of } g:}$", font_size=30)
            .next_to(question_AB_info, DOWN)
            .shift(LEFT * 1.5)
        )
        self.play(Write(part_b_2))
        part_b_3 = (
            Tex(
                r"$\underline{-2\pi < x < 0: } \text{  }m=\frac{2\pi-0}{0-(-2\pi)}=1$",
                font_size=30,
            )
            .next_to(part_b_2, DOWN)
            .shift(RIGHT * 1.3)
        )
        self.play(Write(part_b_3))

        part_b_4 = (
            Tex(
                r"$\underline{0 < x < 4\pi: } \text{  }m=\frac{0-2\pi}{4\pi-0}=-\frac{1}{2}$",
                font_size=30,
            )
            .next_to(part_b_3, DOWN)
            .shift(LEFT * 0.2)
        )
        self.play(Write(part_b_4))
        self.wait()

        g_prime = MathTex(
            r"g'(x) = \begin{cases} 1 & -2\pi < x < 0 \\ -\frac{1}{2} & 0 < x < 4\pi \end{cases}",
            font_size=30,
            color=TEAL,
        ).next_to(part_b_4, DOWN)
        self.play(Write(g_prime))

        self.wait()
        self.play(Write(part_b_1[2]))

        self.wait()
        self.play(
            FadeOut(part_b_1[0]),
            part_b_1[2].animate.shift(UP * 1.5),
            FadeOut(part_b_1[1]),
            FadeOut(part_b_2),
            FadeOut(part_b_3),
            FadeOut(part_b_4),
            FadeOut(g_prime),
        )

        part_b_5 = (
            Tex(r"\underline{Case 1: $f'$ is undefined}", font_size=30)
            .to_corner(UL)
            .shift(DOWN * 3)
        )
        self.play(Write(part_b_5))
        part_b_6 = (
            Tex(
                r"$g'$ is undefined at $x=0$ because $g$ has a cusp at that point.",
                color=TEAL,
                font_size=30,
            )
            .to_corner(UL)
            .shift(DOWN * 3.5)
        )
        self.play(Write(part_b_6))
        part_b_7 = (
            Tex(
                r"$\therefore$ $f'$ is also undefined at $x=0$, so $f$ has a critical point at $x=0$.",
                color=TEAL,
                font_size=30,
            )
            .to_corner(UL)
            .shift(DOWN * 4)
        )
        self.play(Write(part_b_7))
        self.wait()

        part_b_8 = (
            Tex(r"\underline{Alternatively}:", color=TEAL, font_size=30)
            .to_corner(UL)
            .shift(DOWN * 4.5)
        )
        self.play(Write(part_b_8))
        self.wait()

        part_b_9 = (
            MathTex(
                r"\lim_{x\to 0^-} f'(x) = \lim_{x\to 0^-} g'(x)+\frac{1}{2}\sin\left(\frac{x}{2}\right)",
                r"=\lim_{x\to 0^-} 1 + \frac{1}{2}\sin\left(\frac{x}{2}\right) = 1",
                color=TEAL,
                font_size=24,
            )
            .to_corner(UL)
            .shift(DOWN * 4.9)
        )
        self.play(Write(part_b_9[0]))
        self.wait(0.5)
        self.play(Write(part_b_9[1]))

        part_b_10 = (
            MathTex(
                r"\lim_{x\to 0^+} f'(x) = \lim_{x\to 0^+} g'(x)+\frac{1}{2}\sin\left(\frac{x}{2}\right)",
                r"=\lim_{x\to 0^+} -\frac{1}{2} + \frac{1}{2}\sin\left(\frac{x}{2}\right) = -\frac{1}{2}",
                color=TEAL,
                font_size=24,
            )
            .to_corner(UL)
            .shift(DOWN * 5.5)
        )
        self.play(Write(part_b_10[0]))
        self.wait(0.5)
        self.play(Write(part_b_10[1]))
        self.wait()
        part_b_11 = (
            MathTex(
                r"&\text{Since }f \text{ is continuous at } x=0 \text{ and} \lim_{x\to 0^-}f'(x) \neq \lim_{x\to 0^+}f'(x) \text{, } f'(0) \text{ is undefined so } f \\ &\text{ has a critical point there.}",
                font_size=30,
                color=TEAL,
            )
            .to_corner(UL)
            .shift(DOWN * 6.3)
        )
        self.play(Write(part_b_11))

        self.play(
            FadeOut(part_b_5),
            FadeOut(part_b_6),
            FadeOut(part_b_7),
            FadeOut(part_b_8),
            FadeOut(part_b_9),
            FadeOut(part_b_10),
            FadeOut(part_b_11),
        )

        part_b_12 = (
            Tex(r"\underline{Case 2: $f'$ is equal to 0}", font_size=30)
            .to_corner(UL)
            .shift(DOWN * 2.5)
        )
        self.play(Write(part_b_12))

        part_b_13 = (
            Tex(
                r"Check \underline{both} parts of the piecewise function!", font_size=30
            )
            .to_corner(UL)
            .shift(DOWN * 3)
        )
        self.play(Write(part_b_13))
        part_b_14 = (
            Tex(r"$-2\pi<x<0:$", font_size=30, color=TEAL)
            .to_corner(UL)
            .shift(DOWN * 3.5)
        )
        self.play(Write(part_b_14))
        part_b_15 = (
            MathTex(
                r"&f'(x)=1+\frac{1}{2} \sin\left(\frac{x}{2}\right)\text{, which is never equal} \\ & \text{to zero}.",
                font_size=30,
                color=TEAL,
            )
            .to_corner(UL)
            .shift(DOWN * 4)
        )
        self.play(Write(part_b_15))
        self.wait()

        part_b_16 = (
            Tex(r"$0<x<4\pi:$", font_size=30, color=TEAL)
            .to_corner(UL)
            .shift(DOWN * 3.2 + RIGHT * 7)
        )
        self.play(Write(part_b_16))
        part_b_17 = (
            MathTex(
                r"f'(x)=-\frac{1}{2}+\frac{1}{2} \sin\left(\frac{x}{2}\right)&=0 \\",
                r"\sin\left(\frac{x}{2}\right)&=1 \\",
                r"\frac{x}{2} = \frac{\pi}{2} + 2\pi n, n\in \mathbb{Z} \\",
                r"x = \pi + 4\pi n, n\in \mathbb{Z} \\",
                color=TEAL,
                font_size=30,
            )
            .to_corner(UL)
            .shift(DOWN * 3.6 + RIGHT * 7)
        )
        self.play(Write(part_b_17[0]))
        self.wait()
        self.play(Write(part_b_17[1]))
        self.wait()
        self.play(Write(part_b_17[2]))
        self.wait()
        self.play(Write(part_b_17[3]))
        part_b_18 = (
            Tex(
                r"$\text{The only solution in the given interval is } x=\pi.$",
                color=TEAL,
                font_size=30,
            )
            .next_to(part_b_17, DOWN)
            .shift(LEFT * 2)
        )
        self.play(Write(part_b_18))
        self.wait(1.5)

        self.play(
            FadeOut(part_b_12),
            FadeOut(part_b_13),
            FadeOut(part_b_14),
            FadeOut(part_b_15),
            FadeOut(part_b_16),
            FadeOut(part_b_17),
            FadeOut(part_b_18),
        )

        self.next_section(skip_animations=False)

        part_b_18 = (
            Tex(
                r"\begin{minipage}{8cm}$f$ has a critical point at $x=0$ because $f'$ is undefined at that point and another critical point at $x=\pi$ because $f'$ is $0$.\end{minipage}",
                color=TEAL,
                font_size=30,
            )
            .to_corner(UL)
            .shift(DOWN * 2.8)
        )
        self.play(Write(part_b_18))
        part_b_final_box = SurroundingRectangle(part_b_18, color=WHITE, buff=0.2)
        self.play(Create(part_b_final_box))

        self.wait()

        part_c = MathTex(
            r"\text{Let }h(x)=\int_0^{3x} g(t) dt",
            r"\text{ Find } h'(-\frac{\pi}{3})",
            color=WHITE,
            font_size=36,
        ).to_corner(UL)
        self.play(Write(part_c[0]))
        self.play(Write(part_c[1]))

        part_c_0 = (
            Tex(r"Let $G(x)$ be the antiderivative of $g(x)$").to_corner(UL).shift(DOWN)
        )
        part_c_1 = Tex(r"Thus, $h(x)=G(3x)-G(0)$").to_corner(UL).shift(DOWN * 1.5)
        self.play(Write(part_c_0))
        self.play(Write(part_c_1))


if __name__ == "__main__":
    os.system("manim -pqm main.py")
