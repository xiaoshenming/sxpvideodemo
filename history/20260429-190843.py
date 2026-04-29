from manim import *

BG = '#1C1C1C'
PRIMARY = '#58C4DD'
SECONDARY = '#83C167'
ACCENT = '#FFFF00'
MUTED = '#888888'
CJK_FONT = 'Noto Sans CJK SC'

class BaseConfigScene(Scene):
    def setup(self):
        self.setup_layout()

    def setup_layout(self):
        self.camera.background_color = BG
        self.full_canvas = {'center': ORIGIN, 'width': 12.0, 'height': 6.6}
        self.left_canvas = {'center': LEFT * 3.2, 'width': 5.8, 'height': 6.0}
        self.right_canvas = {'center': RIGHT * 3.2, 'width': 5.8, 'height': 6.0}
        self.top_canvas = {'center': UP * 1.8, 'width': 11.0, 'height': 2.7}
        self.bottom_canvas = {'center': DOWN * 1.6, 'width': 11.0, 'height': 3.0}

    def layout_canvas(self, area='full'):
        mapping = {
            'full': self.full_canvas,
            'left': self.left_canvas,
            'right': self.right_canvas,
            'top': self.top_canvas,
            'bottom': self.bottom_canvas,
        }
        return mapping.get(area, self.full_canvas)

    def fit_to_canvas(self, mob, area="full", max_width=None, max_height=None, move=True):
        box = self.layout_canvas(area)
        width = min(float(max_width), float(box['width'])) if max_width is not None else float(box['width'])
        height = min(float(max_height), float(box['height'])) if max_height is not None else float(box['height'])
        if mob.width > width:
            mob.scale_to_fit_width(width)
        if mob.height > height:
            mob.scale_to_fit_height(height)
        if move:
            mob.move_to(box['center'])
        return mob

    def safe_text_box(self, content, area="full", font_size=34, color=None, max_width=None, move=True):
        box = self.layout_canvas(area)
        text = Text(content, font_size=font_size, color=color or PRIMARY, font=CJK_FONT)
        width = min(float(max_width), float(box['width'])) if max_width is not None else float(box['width'])
        if text.width > width:
            text.scale_to_fit_width(width)
        if text.height > box['height']:
            text.scale_to_fit_height(box['height'])
        if move:
            text.move_to(box['center'])
        return text

    def safe_group(self, *mobjects, area="full", direction=None, buff=0.3, max_width=None, max_height=None, move=True):
        group = VGroup(*mobjects)
        if direction is not None:
            group.arrange(direction, buff=buff)
        self.fit_to_canvas(group, area=area, max_width=max_width, max_height=max_height, move=move)
        return group

    def clear_scene(self, run_time=0.6):
        targets = list(self.mobjects)
        if targets:
            self.play(*(FadeOut(mob) for mob in targets), run_time=run_time)

    def title_text(self, text: str, color=PRIMARY):
        title = self.safe_text_box(text, area='top', font_size=42, color=color)
        title.set_weight(BOLD)
        return title

    def emphasize_current(self, target, color=ACCENT, style="circumscribe"):
        if style == "flash":
            return Flash(target, color=color, line_length=0.18, num_lines=8, run_time=0.35)
        if style == "indicate":
            return Indicate(target, color=color, scale_factor=1.06, run_time=0.35)
        return Circumscribe(target, color=color, run_time=0.45)

    def dim_others(self, keep=None, targets=None, opacity=0.35):
        keep_group = VGroup()
        if keep is not None:
            if isinstance(keep, (list, tuple, VGroup)):
                keep_group.add(*keep)
            else:
                keep_group.add(keep)
        candidates = list(targets) if targets is not None else list(self.mobjects)
        return [
            mob.animate.set_opacity(opacity)
            for mob in candidates
            if mob not in keep_group
        ]

    def restore_opacity(self, targets, opacity=1.0):
        if not isinstance(targets, (list, tuple, VGroup)):
            targets = [targets]
        return [mob.animate.set_opacity(opacity) for mob in targets]

    def pythagoras_diagram(self, area="full", max_width=None, max_height=None, move=True):
        A = ORIGIN + LEFT * 1.8 + DOWN * 1.0
        B = A + RIGHT * 3.6
        C = A + UP * 2.7
        triangle = Polygon(A, B, C, color=PRIMARY)
        triangle.set_fill(PRIMARY, opacity=0.10)
        leg_a = Line(start=A, end=B, color=PRIMARY)
        leg_b = Line(start=A, end=C, color=SECONDARY)
        hypotenuse = Line(start=B, end=C, color=ACCENT)
        right_angle = Square(side_length=0.34, color=ACCENT)
        right_angle.move_to(A + RIGHT * 0.17 + UP * 0.17)
        right_angle.set_fill(ACCENT, opacity=0.18)
        label_a = Text('a', font_size=24, color=WHITE, font=CJK_FONT)
        label_a.next_to(leg_a, DOWN, buff=0.12)
        label_b = Text('b', font_size=24, color=WHITE, font=CJK_FONT)
        label_b.next_to(leg_b, LEFT, buff=0.12)
        label_c = Text('c', font_size=24, color=ACCENT, font=CJK_FONT)
        label_c.next_to(hypotenuse, RIGHT, buff=0.12)
        formula = Text('a^2 + b^2 = c^2', font_size=28, color=ACCENT, font=CJK_FONT)
        formula.next_to(triangle, RIGHT, buff=0.55)
        diagram = VGroup(triangle, leg_a, leg_b, hypotenuse, right_angle, label_a, label_b, label_c, formula)
        self.fit_to_canvas(diagram, area=area, max_width=max_width, max_height=max_height, move=move)
        return diagram

class Scene_01_Hook(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('今天我们用直观动画理解：勾股定理几何证明', duration=7.0)
        # Layout: 横屏 16:9; goal: 用一个具体问题激发好奇心，避免直接堆公式。
        title = self.title_text('Hook')
        title.to_edge(UP, buff=0.6)
        goal = self.safe_text_box('用一个具体问题激发好奇心，避免直接堆公式。', area="full", font_size=24, color=SECONDARY, max_width=8.4)
        goal.next_to(title, DOWN, buff=0.5)
        box = RoundedRectangle(width=9.5, height=3.8, corner_radius=0.25, color=PRIMARY)
        box.set_stroke(PRIMARY, opacity=0.8).set_fill(PRIMARY, opacity=0.08)
        visual = self.pythagoras_diagram(area="full", max_width=8.7, max_height=3.3, move=False)
        visual.move_to(box.get_center())
        dot = Dot(color=ACCENT).scale(1.2).next_to(box, LEFT, buff=0.5)
        arrow = Arrow(start=dot.get_right(), end=box.get_left(), buff=0.15, color=ACCENT)
        content_group = self.safe_group(box, visual, dot, arrow, area="full", move=False)
        self.play(Write(title), run_time=1.2)
        self.wait(0.6)
        self.play(FadeIn(goal, shift=DOWN * 0.2), run_time=1.0)
        self.wait(0.6)
        self.play(Create(box), GrowFromCenter(dot), Create(arrow), run_time=1.4)
        self.wait(0.4)
        self.play(FadeIn(visual), run_time=1.0)
        self.wait(1.5)
        self.clear_scene(run_time=0.6)
        self.wait(0.3)

class Scene_02_GeometryFirst(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('先看形状如何变化，再问为什么它必然成立。', duration=8.6)
        # Layout: 横屏 16:9; goal: 先建立几何/画面直觉，再进入符号表达。
        title = self.title_text('GeometryFirst')
        title.to_edge(UP, buff=0.6)
        goal = self.safe_text_box('先建立几何/画面直觉，再进入符号表达。', area="full", font_size=24, color=SECONDARY, max_width=8.4)
        goal.next_to(title, DOWN, buff=0.5)
        box = RoundedRectangle(width=9.5, height=3.8, corner_radius=0.25, color=PRIMARY)
        box.set_stroke(PRIMARY, opacity=0.8).set_fill(PRIMARY, opacity=0.08)
        visual = self.pythagoras_diagram(area="full", max_width=8.7, max_height=3.3, move=False)
        visual.move_to(box.get_center())
        dot = Dot(color=ACCENT).scale(1.2).next_to(box, LEFT, buff=0.5)
        arrow = Arrow(start=dot.get_right(), end=box.get_left(), buff=0.15, color=ACCENT)
        content_group = self.safe_group(box, visual, dot, arrow, area="full", move=False)
        self.play(Write(title), run_time=1.2)
        self.wait(0.6)
        self.play(FadeIn(goal, shift=DOWN * 0.2), run_time=1.0)
        self.wait(0.6)
        self.play(Create(box), GrowFromCenter(dot), Create(arrow), run_time=1.4)
        self.wait(0.4)
        self.play(FadeIn(visual), run_time=1.0)
        self.wait(1.5)
        self.clear_scene(run_time=0.6)
        self.wait(0.3)

class Scene_03_AhaMoment(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('关键不是记住结论，而是看见不变量。', duration=8.6)
        # Layout: 横屏 16:9; goal: 制造 aha moment，把直觉连接到数学结构。
        title = self.title_text('AhaMoment')
        title.to_edge(UP, buff=0.6)
        goal = self.safe_text_box('制造 aha moment，把直觉连接到数学结构。', area="full", font_size=24, color=SECONDARY, max_width=8.4)
        goal.next_to(title, DOWN, buff=0.5)
        box = RoundedRectangle(width=9.5, height=3.8, corner_radius=0.25, color=PRIMARY)
        box.set_stroke(PRIMARY, opacity=0.8).set_fill(PRIMARY, opacity=0.08)
        visual = self.pythagoras_diagram(area="full", max_width=8.7, max_height=3.3, move=False)
        visual.move_to(box.get_center())
        dot = Dot(color=ACCENT).scale(1.2).next_to(box, LEFT, buff=0.5)
        arrow = Arrow(start=dot.get_right(), end=box.get_left(), buff=0.15, color=ACCENT)
        content_group = self.safe_group(box, visual, dot, arrow, area="full", move=False)
        self.play(Write(title), run_time=1.2)
        self.wait(0.6)
        self.play(FadeIn(goal, shift=DOWN * 0.2), run_time=1.0)
        self.wait(0.6)
        self.play(Create(box), GrowFromCenter(dot), Create(arrow), run_time=1.4)
        self.wait(0.4)
        self.play(FadeIn(visual), run_time=1.0)
        self.wait(1.5)
        self.clear_scene(run_time=0.6)
        self.wait(0.3)

# END