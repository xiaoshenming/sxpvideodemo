from manim import *
import re
import shutil

BG = '#1C1C1C'
PRIMARY = '#58C4DD'
SECONDARY = '#83C167'
ACCENT = '#FFFF00'
MUTED = '#888888'
CJK_FONT = 'Noto Sans CJK SC'
LATEX_AVAILABLE = shutil.which("latex") is not None

class SXPGlobalConfig:
    BG = BG
    PRIMARY = PRIMARY
    SECONDARY = SECONDARY
    ACCENT = ACCENT
    MUTED = MUTED
    CJK_FONT = CJK_FONT
    TEXT_SLOTS = {
        'title': 'top',
        'main': 'left',
        'visual': 'right',
        'sub': 'bottom',
    }
    LAYOUT_TEMPLATES = {
        'split_explain_visual': ('left', 'right'),
        'full_screen_geometry': ('full',),
        'rearrangement_proof': ('full', 'bottom'),
        'recap_board': ('top', 'full', 'bottom'),
    }
    VOICEOVER = {
        'reserve': 0.2,
        'min_run_time': 0.4,
        'max_run_time': 1.2,
    }

class SXPBaseScene(Scene):
    def setup(self):
        self.setup_layout()

    def setup_layout(self):
        self.sxp_theme = SXPGlobalConfig
        self.camera.background_color = self.sxp_theme.BG
        self.full_canvas = {'center': ORIGIN, 'width': 12.0, 'height': 6.6}
        self.left_canvas = {'center': LEFT * 3.2, 'width': 5.8, 'height': 6.0}
        self.right_canvas = {'center': RIGHT * 3.2, 'width': 5.8, 'height': 6.0}
        self.top_canvas = {'center': UP * 1.8, 'width': 11.0, 'height': 2.7}
        self.bottom_canvas = {'center': DOWN * 1.6, 'width': 11.0, 'height': 3.0}
        self.text_slots = self.sxp_theme.TEXT_SLOTS
        self.layout_templates = self.sxp_theme.LAYOUT_TEMPLATES

    def layout_canvas(self, area='full'):
        mapping = {
            'full': self.full_canvas,
            'left': self.left_canvas,
            'right': self.right_canvas,
            'top': self.top_canvas,
            'bottom': self.bottom_canvas,
        }
        return mapping.get(area, self.full_canvas)

    def layout_template(self, name):
        return self.layout_templates.get(name, self.layout_templates['full_screen_geometry'])

    def slot_area(self, slot):
        return self.text_slots.get(slot, 'full')

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

    def plain_formula_text(self, label):
        text = str(label)
        text = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"\1/\2", text)
        text = re.sub(r"\\(?:dfrac|tfrac)\{([^{}]+)\}\{([^{}]+)\}", r"\1/\2", text)
        text = re.sub(r"\\sqrt\{([^{}]+)\}", r"sqrt(\1)", text)
        text = re.sub(r"\\(?:mathrm|operatorname|text)\{([^{}]+)\}", r"\1", text)
        text = re.sub(r"\^\{([^{}]+)\}", r"^\1", text)
        text = re.sub(r"_\{([^{}]+)\}", r"_\1", text)
        replacements = {
            r"\Delta": "Δ",
            r"\theta": "θ",
            r"\alpha": "α",
            r"\beta": "β",
            r"\pi": "π",
            r"\perp": "⊥",
            r"\parallel": "∥",
            r"\left": "",
            r"\right": "",
            r"\,": " ",
            r"\;": " ",
            r"\:": " ",
            r"\quad": " ",
            r"\qquad": "  ",
            r"\sin": "sin",
            r"\cos": "cos",
            r"\tan": "tan",
            r"\log": "log",
            r"\ln": "ln",
            r"\angle": "∠",
            r"^\circ": "°",
            r"\circ": "°",
            r"\degree": "°",
            r"\to": "→",
            r"\rightarrow": "→",
            r"\leftarrow": "←",
            r"\Rightarrow": "⇒",
            r"\implies": "⇒",
            r"\leq": "≤",
            r"\geq": "≥",
            r"\neq": "≠",
            r"\approx": "≈",
            r"\cdot": "×",
            r"\times": "×",
            r"\div": "÷",
            r"\pm": "±",
            r"\infty": "∞",
            "^2": "²",
            "^3": "³",
            "{": "",
            "}": "",
        }
        for source, target in replacements.items():
            text = text.replace(source, target)
        return text

    def safe_formula(self, label, area="full", font_size=34, color=None, max_width=None, max_height=None, move=True):
        if LATEX_AVAILABLE:
            formula = MathTex(label, font_size=font_size, color=color or ACCENT)
        else:
            formula = Text(
                self.plain_formula_text(label),
                font_size=font_size,
                color=color or ACCENT,
                font=CJK_FONT,
            )
        self.fit_to_canvas(formula, area=area, max_width=max_width, max_height=max_height, move=move)
        return formula

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

    def show_slot_text(self, content, slot='main', font_size=34, color=None, max_width=None, move=True):
        return self.safe_text_box(
            content,
            area=self.slot_area(slot),
            font_size=font_size,
            color=color,
            max_width=max_width,
            move=move,
        )

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
        title = self.show_slot_text(text, slot='title', font_size=42, color=color)
        title.set_weight(BOLD)
        return title

    def area_card_pattern(self, label, side_length, color, opacity=0.20):
        square = Square(side_length=side_length, color=color)
        square.set_fill(color, opacity=opacity)
        label_mob = self.safe_formula(label, font_size=28, color=color, move=False)
        label_mob.move_to(square.get_center())
        return VGroup(square, label_mob)

    def focus_frame_pattern(self, target, color=ACCENT, buff=0.16):
        return SurroundingRectangle(target, color=color, buff=buff)

    def rearrangement_arrow_pattern(self, start_mob, end_mob, color=ACCENT):
        return Arrow(start=start_mob.get_right(), end=end_mob.get_left(), buff=0.24, color=color)

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

class BaseConfigScene(SXPBaseScene):
    pass

    def cinematic_backdrop(self):
        box = self.layout_canvas('full')
        lines = VGroup()
        for offset in [-3.0, -1.5, 0.0, 1.5, 3.0]:
            horizontal = Line(start=LEFT * float(box['width']) / 2 + UP * offset, end=RIGHT * float(box['width']) / 2 + UP * offset, color=MUTED)
            vertical = Line(start=UP * float(box['height']) / 2 + RIGHT * offset, end=DOWN * float(box['height']) / 2 + RIGHT * offset, color=MUTED)
            lines.add(horizontal, vertical)
        lines.set_opacity(0.12)
        lines.set_z_index(-5)
        self.fit_to_canvas(lines, area='full', move=False)
        return lines

    def pythagoras_triangle(self, fill_color=PRIMARY, fill_opacity=0.54):
        A = ORIGIN + LEFT * 0.95 + DOWN * 0.68
        B = A + RIGHT * 1.9
        C = A + UP * 1.42
        body = Polygon(A, B, C, color=fill_color)
        body.set_fill(fill_color, opacity=fill_opacity)
        body.set_stroke(fill_color, width=3, opacity=1.0)
        leg_a = Line(start=A, end=B, color=PRIMARY)
        leg_b = Line(start=A, end=C, color=SECONDARY)
        hypotenuse = Line(start=B, end=C, color=ACCENT)
        right_angle = Square(side_length=0.22, color=ACCENT)
        right_angle.move_to(A + RIGHT * 0.11 + UP * 0.11)
        right_angle.set_fill(ACCENT, opacity=0.20)
        return VGroup(body, leg_a, leg_b, hypotenuse, right_angle)

    def pythagoras_labeled_triangle(self, area="full"):
        tri = self.pythagoras_triangle(fill_color=PRIMARY)
        brace_a = Brace(tri[1], DOWN, color=PRIMARY)
        brace_b = Brace(tri[2], LEFT, color=SECONDARY)
        label_a = Text('a', font_size=26, color=PRIMARY, font=CJK_FONT)
        label_b = Text('b', font_size=26, color=SECONDARY, font=CJK_FONT)
        label_c = Text('c', font_size=26, color=ACCENT, font=CJK_FONT)
        label_a.next_to(brace_a, DOWN, buff=0.08)
        label_b.next_to(brace_b, LEFT, buff=0.08)
        label_c.next_to(tri[3], RIGHT, buff=0.12)
        frame = self.focus_frame_pattern(tri, color=ACCENT, buff=0.18)
        group = self.safe_group(tri, brace_a, brace_b, label_a, label_b, label_c, frame, area=area, move=False)
        return group

    def pythagoras_arrangement(self, mode="c_square"):
        proof_area = self.layout_template('rearrangement_proof')[0]
        colors = [PRIMARY, SECONDARY, ACCENT, '#A78BFA']
        shifts = [UP * 1.12 + LEFT * 1.18, UP * 1.12 + RIGHT * 1.18, DOWN * 1.12 + RIGHT * 1.18, DOWN * 1.12 + LEFT * 1.18]
        rotations = [0, PI / 2, PI, -PI / 2]
        triangles = VGroup()
        for index in range(4):
            tri = self.pythagoras_triangle(fill_color=colors[index])
            tri.rotate(rotations[index])
            tri.move_to(shifts[index])
            triangles.add(tri)
        triangles.set_z_index(2)
        if mode == "ab_squares":
            a_card = self.area_card_pattern(r"a^2", 1.55, PRIMARY, opacity=0.20)
            a_card.move_to(LEFT * 0.92 + DOWN * 0.05)
            b_card = self.area_card_pattern(r"b^2", 1.15, SECONDARY, opacity=0.22)
            b_card.move_to(RIGHT * 1.05 + UP * 0.22)
            areas = VGroup(a_card, b_card)
        else:
            areas = self.area_card_pattern(r"c^2", 1.75, ACCENT, opacity=0.18)
            areas[0].rotate(PI / 4)
        frame = self.focus_frame_pattern(VGroup(triangles, areas), color=MUTED, buff=0.22)
        frame.set_opacity(0.18)
        return self.safe_group(triangles, areas, frame, area=proof_area, max_width=7.4, max_height=4.8, move=False)

    def pythagoras_formula(self, area="bottom"):
        formula = self.safe_formula(r"a^2 + b^2 = c^2", area=area, font_size=34, color=ACCENT, max_width=5.6, max_height=1.0, move=False)
        self.fit_to_canvas(formula, area=area, max_width=5.6, max_height=1.0, move=False)
        return formula

class Scene_01_Hook(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('先不写公式，只看这个直角三角形的面积会留下什么线索。', duration=8.0)
        backdrop = self.cinematic_backdrop()
        self.add(backdrop)
        title = self.title_text('Hook')
        title.to_edge(UP, buff=0.45)
        question = self.safe_text_box('先看面积，不急着背公式。', area="top", font_size=26, color=SECONDARY, max_width=6.8)
        question.next_to(title, DOWN, buff=0.32)
        tri = self.pythagoras_labeled_triangle(area="full")
        tri.move_to(DOWN * 0.35)
        arrow = Arrow(start=question.get_bottom(), end=tri.get_top(), buff=0.18, color=ACCENT)
        content = self.safe_group(question, tri, arrow, area="full", move=False)
        self.fit_to_canvas(content, area="full", max_width=8.4, max_height=5.2, move=True)
        self.play(Write(title), run_time=1.0)
        self.wait(0.6)
        self.play(FadeIn(question, shift=DOWN * 0.2), Create(arrow), run_time=1.1)
        self.wait(0.6)
        self.play(Create(tri), run_time=1.5)
        self.wait(1.5)
        focus_anims = self.dim_others(keep=tri, targets=content)
        focus_anims.append(self.emphasize_current(tri))
        self.play(*focus_anims, run_time=1.0)
        self.wait(1.5)
        self.play(*self.restore_opacity(content), run_time=0.6)
        self.wait(0.4)
        self.clear_scene(run_time=0.6)
        self.wait(0.3)

class Scene_02_FourTrianglesBuild(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('四个三角形完全一样，它们怎么摆，面积总量都不会变。', duration=8.6)
        backdrop = self.cinematic_backdrop()
        self.add(backdrop)
        title = self.title_text('FourTrianglesBuild')
        title.to_edge(UP, buff=0.45)
        layout = self.pythagoras_arrangement(mode="c_square")
        layout.move_to(DOWN * 0.25)
        triangles = layout[0]
        caption = self.safe_text_box('四个全等三角形：演员不变，只换站位。', area="bottom", font_size=25, color=WHITE, max_width=7.2)
        caption.next_to(layout, DOWN, buff=0.32)
        scene_group = self.safe_group(layout, caption, area="full", move=False)
        self.fit_to_canvas(scene_group, area="full", max_width=8.6, max_height=5.5, move=True)
        self.play(Write(title), run_time=1.0)
        self.wait(0.5)
        self.play(LaggedStart(FadeIn(triangles[0], shift=UP * 0.15), FadeIn(triangles[1], shift=UP * 0.15), FadeIn(triangles[2], shift=UP * 0.15), FadeIn(triangles[3], shift=UP * 0.15), lag_ratio=0.16), run_time=2.2)
        self.wait(1.5)
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.9)
        self.wait(0.6)
        focus_anims = self.dim_others(keep=triangles, targets=scene_group)
        focus_anims.append(self.emphasize_current(triangles))
        self.play(*focus_anims, run_time=1.0)
        self.wait(1.5)
        self.play(*self.restore_opacity(scene_group), run_time=0.6)
        self.wait(0.4)
        self.clear_scene(run_time=0.6)
        self.wait(0.3)

class Scene_03_TwoArrangements(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('把同样的四个三角形重新摆放，空出来的形状变了，但总面积没有变。', duration=8.6)
        backdrop = self.cinematic_backdrop()
        self.add(backdrop)
        title = self.title_text('TwoArrangements')
        title.to_edge(UP, buff=0.45)
        layout_a = self.pythagoras_arrangement(mode="c_square")
        layout_b = self.pythagoras_arrangement(mode="ab_squares")
        layout_a.move_to(DOWN * 0.15)
        layout_b.move_to(DOWN * 0.15)
        label_a = self.safe_text_box('拼法一：中间留下 c^2', area="bottom", font_size=24, color=ACCENT, max_width=7.2)
        label_b = self.safe_text_box('拼法二：留下 a^2 和 b^2', area="bottom", font_size=24, color=SECONDARY, max_width=7.2)
        label_a.next_to(layout_a, DOWN, buff=0.28)
        label_b.next_to(layout_b, DOWN, buff=0.28)
        self.play(Write(title), run_time=1.0)
        self.wait(0.5)
        self.play(FadeIn(layout_a), FadeIn(label_a), run_time=1.2)
        self.wait(1.5)
        start_triangles = layout_a[0]
        target_triangles = layout_b[0]
        area_cards = layout_a[1]
        target_areas = layout_b[1]
        start_triangles.generate_target()
        for index, target in enumerate(target_triangles):
            start_triangles.target[index].move_to(target.get_center())
            start_triangles.target[index].rotate((index + 1) * PI / 2)
        self.play(MoveToTarget(start_triangles, path_arc=PI / 5), ReplacementTransform(area_cards, target_areas), ReplacementTransform(layout_a[2], layout_b[2]), ReplacementTransform(label_a, label_b), run_time=2.8)
        self.wait(1.5)
        self.play(self.emphasize_current(layout_b[1]), run_time=0.8)
        self.wait(1.5)
        self.clear_scene(run_time=0.6)
        self.wait(0.3)

class Scene_04_AhaMoment(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('这就是关键时刻：三角形没有变，变的只是空白区域的样子。', duration=8.6)
        backdrop = self.cinematic_backdrop()
        self.add(backdrop)
        title = self.title_text('AhaMoment')
        title.to_edge(UP, buff=0.45)
        layout = self.pythagoras_arrangement(mode="ab_squares")
        layout.move_to(DOWN * 0.15)
        invariant = self.safe_text_box('四个三角形没有变，空白面积必须相等。', area="bottom", font_size=26, color=ACCENT, max_width=7.4)
        invariant.next_to(layout, DOWN, buff=0.32)
        frame = self.focus_frame_pattern(layout[1], color=ACCENT, buff=0.16)
        scene_group = self.safe_group(layout, invariant, frame, area="full", move=False)
        self.fit_to_canvas(scene_group, area="full", max_width=8.6, max_height=5.4, move=True)
        self.play(Write(title), run_time=1.0)
        self.wait(0.5)
        self.play(FadeIn(layout), run_time=1.2)
        self.wait(0.6)
        focus_anims = self.dim_others(keep=layout[1], targets=scene_group)
        focus_anims.append(Create(frame))
        focus_anims.append(self.emphasize_current(layout[1]))
        self.play(*focus_anims, run_time=1.1)
        self.wait(2.0)
        self.play(FadeIn(invariant, shift=UP * 0.15), run_time=0.9)
        self.wait(1.5)
        self.play(*self.restore_opacity(scene_group), run_time=0.6)
        self.wait(0.4)
        self.clear_scene(run_time=0.6)
        self.wait(0.3)

class Scene_05_FormulaEarned(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('两个小方形的面积合起来，正好等于斜边上的大方形。', duration=8.6)
        backdrop = self.cinematic_backdrop()
        self.add(backdrop)
        title = self.title_text('FormulaEarned')
        title.to_edge(UP, buff=0.45)
        ab_layout = self.pythagoras_arrangement(mode="ab_squares")
        c_layout = self.pythagoras_arrangement(mode="c_square")
        ab_layout.move_to(LEFT * 2.15 + DOWN * 0.15)
        c_layout.move_to(RIGHT * 2.15 + DOWN * 0.15)
        formula = self.pythagoras_formula(area="bottom")
        formula.next_to(VGroup(ab_layout, c_layout), DOWN, buff=0.45)
        merge_arrow = self.rearrangement_arrow_pattern(ab_layout, c_layout)
        proof_group = self.safe_group(ab_layout, c_layout, formula, merge_arrow, area="full", move=False)
        self.fit_to_canvas(proof_group, area="full", max_width=9.2, max_height=5.4, move=True)
        self.play(Write(title), run_time=1.0)
        self.wait(0.5)
        self.play(FadeIn(ab_layout), Create(merge_arrow), run_time=1.2)
        self.wait(0.8)
        self.play(TransformMatchingShapes(ab_layout.copy(), c_layout), run_time=2.0)
        self.wait(1.5)
        self.play(Write(formula), self.emphasize_current(c_layout[1]), run_time=1.2)
        self.wait(2.0)
        self.clear_scene(run_time=0.6)
        self.wait(0.3)

class Scene_06_Recap(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('记住这条路：先看面积守恒，再得到勾股公式。', duration=8.6)
        backdrop = self.cinematic_backdrop()
        self.add(backdrop)
        title = self.title_text('Recap')
        title.to_edge(UP, buff=0.45)
        left = self.pythagoras_arrangement(mode="ab_squares")
        right = self.pythagoras_arrangement(mode="c_square")
        left.scale(0.72).move_to(LEFT * 2.8 + DOWN * 0.15)
        right.scale(0.72).move_to(RIGHT * 2.8 + DOWN * 0.15)
        formula = self.pythagoras_formula(area="bottom")
        formula.next_to(VGroup(left, right), DOWN, buff=0.36)
        recap = self.safe_text_box('复盘：同样四个三角形，空白面积从 a^2+b^2 变成 c^2。', area="top", font_size=24, color=WHITE, max_width=8.4)
        recap.next_to(title, DOWN, buff=0.28)
        arrow = self.rearrangement_arrow_pattern(left, right)
        final_group = self.safe_group(recap, left, right, arrow, formula, area="full", move=False)
        self.fit_to_canvas(final_group, area="full", max_width=9.5, max_height=5.5, move=True)
        self.play(Write(title), FadeIn(recap, shift=DOWN * 0.12), run_time=1.1)
        self.wait(0.6)
        self.play(FadeIn(left), Create(arrow), FadeIn(right), run_time=1.4)
        self.wait(1.5)
        self.play(Write(formula), self.emphasize_current(formula), run_time=1.1)
        self.wait(2.0)
        self.clear_scene(run_time=0.6)
        self.wait(0.3)

# END