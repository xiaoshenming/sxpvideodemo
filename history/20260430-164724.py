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
        self.slot_mobjects = {}
        self.narration_timeline = []
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

    def show_text(self, content, slot_name, font_size=36, color=None):
        slot_key = str(slot_name)
        text = self.safe_text_box(
            content,
            area=self.slot_area(slot_key),
            font_size=font_size,
            color=color,
            move=True,
        )
        previous = self.slot_mobjects.get(slot_key)
        self.slot_mobjects[slot_key] = text
        if previous is None:
            return FadeIn(text, shift=UP * 0.12)
        return ReplacementTransform(previous, text)

    def restore_text(self, slot_name, content, font_size=36, color=None):
        return self.show_text(content, slot_name, font_size=font_size, color=color)

    def narration_timing_hook(self, text, duration, scene_name="", record_only=False):
        record = {'scene': scene_name, 'text': text, 'duration': duration, 'record_only': record_only}
        self.narration_timeline.append(record)
        if not record_only:
            self.add_subcaption(text, duration=duration)
        return record

    def compose_visual_pattern(self, *mobjects, area="full", direction=None, buff=0.3, max_width=None, max_height=None, move=True):
        return self.safe_group(
            *mobjects,
            area=area,
            direction=direction,
            buff=buff,
            max_width=max_width,
            max_height=max_height,
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

    def pattern_node(self, label, color=PRIMARY):
        text = (str(label).replace('_', ' ') or 'step')[:28]
        body = RoundedRectangle(width=2.2, height=0.72, corner_radius=0.16, color=color)
        body.set_fill(color, opacity=0.12)
        caption = Text(text, font_size=20, color=WHITE, font=CJK_FONT)
        if caption.width > 1.85:
            caption.scale_to_fit_width(1.85)
        caption.move_to(body.get_center())
        return VGroup(body, caption)

    def connector_arrow_pattern(self, start_mob, end_mob, color=ACCENT):
        return Arrow(start=start_mob.get_right(), end=end_mob.get_left(), buff=0.15, color=color)

    def flow_diagram_pattern(self, title, labels, area="full", max_width=None, max_height=None, move=True):
        clean_labels = [str(item).strip() for item in labels if str(item).strip()]
        if not clean_labels:
            clean_labels = ['input', 'process', 'output']
        palette = [PRIMARY, SECONDARY, ACCENT]
        nodes = VGroup()
        for index, label in enumerate(clean_labels[:3]):
            nodes.add(self.pattern_node(label, color=palette[index % len(palette)]))
        nodes.arrange(RIGHT, buff=0.65)
        arrows = VGroup()
        for index in range(max(0, len(nodes) - 1)):
            arrows.add(self.connector_arrow_pattern(nodes[index], nodes[index + 1]))
        heading = Text(str(title), font_size=24, color=SECONDARY, font=CJK_FONT)
        if heading.width > 4.2:
            heading.scale_to_fit_width(4.2)
        diagram = VGroup(heading, VGroup(nodes, arrows)).arrange(DOWN, buff=0.35)
        self.fit_to_canvas(diagram, area=area, max_width=max_width, max_height=max_height, move=move)
        return diagram

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

class BaseCinemaScene(SXPBaseScene):
    pass

class BaseConfigScene(SXPBaseScene):
    pass

    def process_flow_pattern(self, labels, area="full", active_index=0, max_width=None, move=True):
        cleaned = [str(label).strip() for label in labels if str(label).strip()]
        if not cleaned:
            cleaned = ['入口', '处理', '输出']
        nodes = VGroup()
        for index, label in enumerate(cleaned):
            color = ACCENT if index == active_index else PRIMARY
            card = RoundedRectangle(width=1.65, height=0.72, corner_radius=0.14, color=color)
            card.set_fill(color, opacity=0.16 if index == active_index else 0.08)
            label_mob = Text(label, font_size=22, color=WHITE, font=CJK_FONT)
            if label_mob.width > 1.32:
                label_mob.scale_to_fit_width(1.32)
            node = VGroup(card, label_mob)
            nodes.add(node)
        nodes.arrange(RIGHT, buff=0.36)
        arrows = VGroup()
        for index in range(len(nodes) - 1):
            arrows.add(
                Arrow(
                    start=nodes[index].get_right(),
                    end=nodes[index + 1].get_left(),
                    buff=0.12,
                    color=SECONDARY,
                )
            )
        flow = VGroup(nodes, arrows)
        self.fit_to_canvas(flow, area=area, max_width=max_width, max_height=2.4, move=move)
        return flow

class Scene_01_Hook(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('今天我们先从一个看得见的问题开始。', duration=7.0)
        self.narration_timing_hook('今天我们先从一个看得见的问题开始。', duration=7.0, scene_name='Hook', record_only=True)
        self.add_subcaption('先明确这一段的目标: 用一个具体问题激发好奇心，避免直接堆公式。', duration=2.3)
        self.narration_timing_hook('先明确这一段的目标: 用一个具体问题激发好奇心，避免直接堆公式。', duration=2.3, scene_name='Hook', record_only=True)
        self.add_subcaption('再看画面设计: safe_text_box 提出问题，flow_diagram_pattern 建立现象、变量、目标三点关系。', duration=2.3)
        self.narration_timing_hook('再看画面设计: safe_text_box 提出问题，flow_diagram_pattern 建立现象、变量、目标三点关系。', duration=2.3, scene_name='Hook', record_only=True)
        # Layout: 横屏 16:9; goal: 用一个具体问题激发好奇心，避免直接堆公式。
        title = self.title_text('Hook')
        title.to_edge(UP, buff=0.6)
        goal = self.safe_text_box('用一个具体问题激发好奇心，避免直接堆公式。', area="full", font_size=24, color=SECONDARY, max_width=8.4)
        goal.next_to(title, DOWN, buff=0.5)
        box = RoundedRectangle(width=9.5, height=3.8, corner_radius=0.25, color=PRIMARY)
        box.set_stroke(PRIMARY, opacity=0.8).set_fill(PRIMARY, opacity=0.08)
        visual = self.process_flow_pattern(labels=['入口', '处理', '等待', '输出'], area="full", active_index=0, max_width=8.7, move=False)
        visual.move_to(box.get_center())
        dot = Dot(color=ACCENT).scale(1.2).next_to(box, LEFT, buff=0.5)
        arrow = Arrow(start=dot.get_right(), end=box.get_left(), buff=0.15, color=ACCENT)
        content_group = self.compose_visual_pattern(box, visual, dot, arrow, area="full", move=False)
        self.play(Write(title), run_time=1.2)
        self.wait(0.6)
        self.play(FadeIn(goal, shift=DOWN * 0.2), run_time=1.0)
        self.wait(0.6)
        self.play(Create(box), GrowFromCenter(dot), Create(arrow), run_time=1.4)
        self.wait(0.4)
        self.play(FadeIn(visual), run_time=1.0)
        self.wait(1.5)
        focus_anims = self.dim_others(keep=visual, targets=content_group)
        focus_anims.append(self.emphasize_current(visual))
        self.play(*focus_anims, run_time=0.8)
        self.wait(0.4)
        self.play(Indicate(arrow), run_time=0.7)
        self.wait(0.3)
        self.play(*self.restore_opacity(content_group), run_time=0.6)
        self.wait(0.4)
        self.clear_scene(run_time=0.6)
        self.wait(0.3)

class Scene_02_GeometryFirst(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('先看形状如何变化，再问为什么它必然成立。', duration=8.6)
        self.narration_timing_hook('先看形状如何变化，再问为什么它必然成立。', duration=8.6, scene_name='GeometryFirst', record_only=True)
        self.add_subcaption('先明确这一段的目标: 先建立几何/画面直觉，再进入符号表达。', duration=2.1)
        self.narration_timing_hook('先明确这一段的目标: 先建立几何/画面直觉，再进入符号表达。', duration=2.1, scene_name='GeometryFirst', record_only=True)
        self.add_subcaption('再看画面设计: safe_group 组合图形、箭头和关键对象，用 transition path 展示变化方向。', duration=2.1)
        self.narration_timing_hook('再看画面设计: safe_group 组合图形、箭头和关键对象，用 transition path 展示变化方向。', duration=2.1, scene_name='GeometryFirst', record_only=True)
        self.add_subcaption('这一步的关键是: 先建立几何/画面直觉，再进入符号表达。', duration=2.1)
        self.narration_timing_hook('这一步的关键是: 先建立几何/画面直觉，再进入符号表达。', duration=2.1, scene_name='GeometryFirst', record_only=True)
        # Layout: 横屏 16:9; goal: 先建立几何/画面直觉，再进入符号表达。
        title = self.title_text('GeometryFirst')
        title.to_edge(UP, buff=0.6)
        goal = self.safe_text_box('先建立几何/画面直觉，再进入符号表达。', area="full", font_size=24, color=SECONDARY, max_width=8.4)
        goal.next_to(title, DOWN, buff=0.5)
        box = RoundedRectangle(width=9.5, height=3.8, corner_radius=0.25, color=PRIMARY)
        box.set_stroke(PRIMARY, opacity=0.8).set_fill(PRIMARY, opacity=0.08)
        visual = self.process_flow_pattern(labels=['待处理', '处理中', '超时', '已升级'], area="full", active_index=2, max_width=8.7, move=False)
        visual.move_to(box.get_center())
        dot = Dot(color=ACCENT).scale(1.2).next_to(box, LEFT, buff=0.5)
        arrow = Arrow(start=dot.get_right(), end=box.get_left(), buff=0.15, color=ACCENT)
        content_group = self.compose_visual_pattern(box, visual, dot, arrow, area="full", move=False)
        self.play(Write(title), run_time=1.2)
        self.wait(0.6)
        self.play(FadeIn(goal, shift=DOWN * 0.2), run_time=1.0)
        self.wait(0.6)
        self.play(Create(box), GrowFromCenter(dot), Create(arrow), run_time=1.4)
        self.wait(0.4)
        self.play(FadeIn(visual), run_time=1.0)
        self.wait(1.5)
        focus_anims = self.dim_others(keep=visual, targets=content_group)
        focus_anims.append(self.emphasize_current(visual))
        self.play(*focus_anims, run_time=0.8)
        self.wait(0.4)
        self.play(Indicate(arrow), run_time=0.7)
        self.wait(0.3)
        self.play(*self.restore_opacity(content_group), run_time=0.6)
        self.wait(0.4)
        self.clear_scene(run_time=0.6)
        self.wait(0.3)

class Scene_03_AhaMoment(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('关键不是记住结论，而是看见不变量。', duration=8.6)
        self.narration_timing_hook('关键不是记住结论，而是看见不变量。', duration=8.6, scene_name='AhaMoment', record_only=True)
        self.add_subcaption('先明确这一段的目标: 制造 aha moment，把直觉连接到数学结构。', duration=2.1)
        self.narration_timing_hook('先明确这一段的目标: 制造 aha moment，把直觉连接到数学结构。', duration=2.1, scene_name='AhaMoment', record_only=True)
        self.add_subcaption('再看画面设计: 用高亮、Brace、箭头强调结构不变量。', duration=2.1)
        self.narration_timing_hook('再看画面设计: 用高亮、Brace、箭头强调结构不变量。', duration=2.1, scene_name='AhaMoment', record_only=True)
        self.add_subcaption('这一步的关键是: 制造 aha moment，把直觉连接到数学结构。', duration=2.1)
        self.narration_timing_hook('这一步的关键是: 制造 aha moment，把直觉连接到数学结构。', duration=2.1, scene_name='AhaMoment', record_only=True)
        # Layout: 横屏 16:9; goal: 制造 aha moment，把直觉连接到数学结构。
        title = self.title_text('AhaMoment')
        title.to_edge(UP, buff=0.6)
        goal = self.safe_text_box('制造 aha moment，把直觉连接到数学结构。', area="full", font_size=24, color=SECONDARY, max_width=8.4)
        goal.next_to(title, DOWN, buff=0.5)
        box = RoundedRectangle(width=9.5, height=3.8, corner_radius=0.25, color=PRIMARY)
        box.set_stroke(PRIMARY, opacity=0.8).set_fill(PRIMARY, opacity=0.08)
        visual = self.process_flow_pattern(labels=['待处理', '处理中', '超时', '已升级'], area="full", active_index=0, max_width=8.7, move=False)
        visual.move_to(box.get_center())
        dot = Dot(color=ACCENT).scale(1.2).next_to(box, LEFT, buff=0.5)
        arrow = Arrow(start=dot.get_right(), end=box.get_left(), buff=0.15, color=ACCENT)
        content_group = self.compose_visual_pattern(box, visual, dot, arrow, area="full", move=False)
        self.play(Write(title), run_time=1.2)
        self.wait(0.6)
        self.play(FadeIn(goal, shift=DOWN * 0.2), run_time=1.0)
        self.wait(0.6)
        self.play(Create(box), GrowFromCenter(dot), Create(arrow), run_time=1.4)
        self.wait(0.4)
        self.play(FadeIn(visual), run_time=1.0)
        self.wait(1.5)
        focus_anims = self.dim_others(keep=visual, targets=content_group)
        focus_anims.append(self.emphasize_current(visual))
        self.play(*focus_anims, run_time=0.8)
        self.wait(0.4)
        self.play(Indicate(arrow), run_time=0.7)
        self.wait(0.3)
        self.play(*self.restore_opacity(content_group), run_time=0.6)
        self.wait(0.4)
        self.clear_scene(run_time=0.6)
        self.wait(0.3)

class Scene_04_ModelBuild(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('模型的价值，是把复杂现象拆成能观察的部件。', duration=8.6)
        self.narration_timing_hook('模型的价值，是把复杂现象拆成能观察的部件。', duration=8.6, scene_name='ModelBuild', record_only=True)
        self.add_subcaption('先明确这一段的目标: 把现象抽象成可复用的视觉模型。', duration=2.9)
        self.narration_timing_hook('先明确这一段的目标: 把现象抽象成可复用的视觉模型。', duration=2.9, scene_name='ModelBuild', record_only=True)
        self.add_subcaption('再看画面设计: 用 state_machine 节点标出输入、作用、输出，逐个 reveal 模型组件。', duration=2.9)
        self.narration_timing_hook('再看画面设计: 用 state_machine 节点标出输入、作用、输出，逐个 reveal 模型组件。', duration=2.9, scene_name='ModelBuild', record_only=True)
        # Layout: 横屏 16:9; goal: 把现象抽象成可复用的视觉模型。
        title = self.title_text('ModelBuild')
        title.to_edge(UP, buff=0.6)
        goal = self.safe_text_box('把现象抽象成可复用的视觉模型。', area="full", font_size=24, color=SECONDARY, max_width=8.4)
        goal.next_to(title, DOWN, buff=0.5)
        box = RoundedRectangle(width=9.5, height=3.8, corner_radius=0.25, color=PRIMARY)
        box.set_stroke(PRIMARY, opacity=0.8).set_fill(PRIMARY, opacity=0.08)
        visual = self.process_flow_pattern(labels=['待处理', '处理中', '超时', '已升级'], area="full", active_index=2, max_width=8.7, move=False)
        visual.move_to(box.get_center())
        dot = Dot(color=ACCENT).scale(1.2).next_to(box, LEFT, buff=0.5)
        arrow = Arrow(start=dot.get_right(), end=box.get_left(), buff=0.15, color=ACCENT)
        content_group = self.compose_visual_pattern(box, visual, dot, arrow, area="full", move=False)
        self.play(Write(title), run_time=1.2)
        self.wait(0.6)
        self.play(FadeIn(goal, shift=DOWN * 0.2), run_time=1.0)
        self.wait(0.6)
        self.play(Create(box), GrowFromCenter(dot), Create(arrow), run_time=1.4)
        self.wait(0.4)
        self.play(FadeIn(visual), run_time=1.0)
        self.wait(1.5)
        focus_anims = self.dim_others(keep=visual, targets=content_group)
        focus_anims.append(self.emphasize_current(visual))
        self.play(*focus_anims, run_time=0.8)
        self.wait(0.4)
        self.play(Indicate(arrow), run_time=0.7)
        self.wait(0.3)
        self.play(*self.restore_opacity(content_group), run_time=0.6)
        self.wait(0.4)
        self.clear_scene(run_time=0.6)
        self.wait(0.3)

class Scene_05_SymbolBridge(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('符号只是给刚才的画面命名，不是新的魔法。', duration=8.6)
        self.narration_timing_hook('符号只是给刚才的画面命名，不是新的魔法。', duration=8.6, scene_name='SymbolBridge', record_only=True)
        self.add_subcaption('先明确这一段的目标: 把视觉模型翻译成符号或关键词，但不让公式抢先。', duration=2.1)
        self.narration_timing_hook('先明确这一段的目标: 把视觉模型翻译成符号或关键词，但不让公式抢先。', duration=2.1, scene_name='SymbolBridge', record_only=True)
        self.add_subcaption('再看画面设计: 左侧保留模型，右侧用 safe_text_box 显示符号桥接和等量关系。', duration=2.1)
        self.narration_timing_hook('再看画面设计: 左侧保留模型，右侧用 safe_text_box 显示符号桥接和等量关系。', duration=2.1, scene_name='SymbolBridge', record_only=True)
        self.add_subcaption('这一步的关键是: 把视觉模型翻译成符号或关键词，但不让公式抢先。', duration=2.1)
        self.narration_timing_hook('这一步的关键是: 把视觉模型翻译成符号或关键词，但不让公式抢先。', duration=2.1, scene_name='SymbolBridge', record_only=True)
        # Layout: 横屏 16:9; goal: 把视觉模型翻译成符号或关键词，但不让公式抢先。
        title = self.title_text('SymbolBridge')
        title.to_edge(UP, buff=0.6)
        goal = self.safe_text_box('把视觉模型翻译成符号或关键词，但不让公式抢先。', area="full", font_size=24, color=SECONDARY, max_width=8.4)
        goal.next_to(title, DOWN, buff=0.5)
        box = RoundedRectangle(width=9.5, height=3.8, corner_radius=0.25, color=PRIMARY)
        box.set_stroke(PRIMARY, opacity=0.8).set_fill(PRIMARY, opacity=0.08)
        visual = self.process_flow_pattern(labels=['入口', '处理', '等待', '输出'], area="full", active_index=0, max_width=8.7, move=False)
        visual.move_to(box.get_center())
        dot = Dot(color=ACCENT).scale(1.2).next_to(box, LEFT, buff=0.5)
        arrow = Arrow(start=dot.get_right(), end=box.get_left(), buff=0.15, color=ACCENT)
        content_group = self.compose_visual_pattern(box, visual, dot, arrow, area="full", move=False)
        self.play(Write(title), run_time=1.2)
        self.wait(0.6)
        self.play(FadeIn(goal, shift=DOWN * 0.2), run_time=1.0)
        self.wait(0.6)
        self.play(Create(box), GrowFromCenter(dot), Create(arrow), run_time=1.4)
        self.wait(0.4)
        self.play(FadeIn(visual), run_time=1.0)
        self.wait(1.5)
        focus_anims = self.dim_others(keep=visual, targets=content_group)
        focus_anims.append(self.emphasize_current(visual))
        self.play(*focus_anims, run_time=0.8)
        self.wait(0.4)
        self.play(Indicate(arrow), run_time=0.7)
        self.wait(0.3)
        self.play(*self.restore_opacity(content_group), run_time=0.6)
        self.wait(0.4)
        self.clear_scene(run_time=0.6)
        self.wait(0.3)

class Scene_06_WorkedExample(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('现在做一个例题，看看模型能不能自己带我们走到结论。', duration=8.6)
        self.narration_timing_hook('现在做一个例题，看看模型能不能自己带我们走到结论。', duration=8.6, scene_name='WorkedExample', record_only=True)
        self.add_subcaption('先明确这一段的目标: 用一个例题检验模型是否真的能解决问题。', duration=2.1)
        self.narration_timing_hook('先明确这一段的目标: 用一个例题检验模型是否真的能解决问题。', duration=2.1, scene_name='WorkedExample', record_only=True)
        self.add_subcaption('再看画面设计: 例题卡片进入画面，模型节点逐步替换成题目里的具体量。', duration=2.1)
        self.narration_timing_hook('再看画面设计: 例题卡片进入画面，模型节点逐步替换成题目里的具体量。', duration=2.1, scene_name='WorkedExample', record_only=True)
        self.add_subcaption('这一步的关键是: 用一个例题检验模型是否真的能解决问题。', duration=2.1)
        self.narration_timing_hook('这一步的关键是: 用一个例题检验模型是否真的能解决问题。', duration=2.1, scene_name='WorkedExample', record_only=True)
        # Layout: 横屏 16:9; goal: 用一个例题检验模型是否真的能解决问题。
        title = self.title_text('WorkedExample')
        title.to_edge(UP, buff=0.6)
        goal = self.safe_text_box('用一个例题检验模型是否真的能解决问题。', area="full", font_size=24, color=SECONDARY, max_width=8.4)
        goal.next_to(title, DOWN, buff=0.5)
        box = RoundedRectangle(width=9.5, height=3.8, corner_radius=0.25, color=PRIMARY)
        box.set_stroke(PRIMARY, opacity=0.8).set_fill(PRIMARY, opacity=0.08)
        visual = self.process_flow_pattern(labels=['入口', '处理', '等待', '输出'], area="full", active_index=1, max_width=8.7, move=False)
        visual.move_to(box.get_center())
        dot = Dot(color=ACCENT).scale(1.2).next_to(box, LEFT, buff=0.5)
        arrow = Arrow(start=dot.get_right(), end=box.get_left(), buff=0.15, color=ACCENT)
        content_group = self.compose_visual_pattern(box, visual, dot, arrow, area="full", move=False)
        self.play(Write(title), run_time=1.2)
        self.wait(0.6)
        self.play(FadeIn(goal, shift=DOWN * 0.2), run_time=1.0)
        self.wait(0.6)
        self.play(Create(box), GrowFromCenter(dot), Create(arrow), run_time=1.4)
        self.wait(0.4)
        self.play(FadeIn(visual), run_time=1.0)
        self.wait(1.5)
        focus_anims = self.dim_others(keep=visual, targets=content_group)
        focus_anims.append(self.emphasize_current(visual))
        self.play(*focus_anims, run_time=0.8)
        self.wait(0.4)
        self.play(Indicate(arrow), run_time=0.7)
        self.wait(0.3)
        self.play(*self.restore_opacity(content_group), run_time=0.6)
        self.wait(0.4)
        self.clear_scene(run_time=0.6)
        self.wait(0.3)

class Scene_07_ContrastCase(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('再看一个对比情形，模型什么时候能用，什么时候会失效。', duration=8.6)
        self.narration_timing_hook('再看一个对比情形，模型什么时候能用，什么时候会失效。', duration=8.6, scene_name='ContrastCase', record_only=True)
        self.add_subcaption('先明确这一段的目标: 对比一个容易混淆的情况，说明模型边界。', duration=2.9)
        self.narration_timing_hook('先明确这一段的目标: 对比一个容易混淆的情况，说明模型边界。', duration=2.9, scene_name='ContrastCase', record_only=True)
        self.add_subcaption('再看画面设计: 两条路径并排展示，正确路径高亮，错误路径降透明度并用 Cross 标出。', duration=2.9)
        self.narration_timing_hook('再看画面设计: 两条路径并排展示，正确路径高亮，错误路径降透明度并用 Cross 标出。', duration=2.9, scene_name='ContrastCase', record_only=True)
        # Layout: 横屏 16:9; goal: 对比一个容易混淆的情况，说明模型边界。
        title = self.title_text('ContrastCase')
        title.to_edge(UP, buff=0.6)
        goal = self.safe_text_box('对比一个容易混淆的情况，说明模型边界。', area="full", font_size=24, color=SECONDARY, max_width=8.4)
        goal.next_to(title, DOWN, buff=0.5)
        box = RoundedRectangle(width=9.5, height=3.8, corner_radius=0.25, color=PRIMARY)
        box.set_stroke(PRIMARY, opacity=0.8).set_fill(PRIMARY, opacity=0.08)
        visual = self.process_flow_pattern(labels=['待处理', '处理中', '超时', '已升级'], area="full", active_index=0, max_width=8.7, move=False)
        visual.move_to(box.get_center())
        dot = Dot(color=ACCENT).scale(1.2).next_to(box, LEFT, buff=0.5)
        arrow = Arrow(start=dot.get_right(), end=box.get_left(), buff=0.15, color=ACCENT)
        content_group = self.compose_visual_pattern(box, visual, dot, arrow, area="full", move=False)
        self.play(Write(title), run_time=1.2)
        self.wait(0.6)
        self.play(FadeIn(goal, shift=DOWN * 0.2), run_time=1.0)
        self.wait(0.6)
        self.play(Create(box), GrowFromCenter(dot), Create(arrow), run_time=1.4)
        self.wait(0.4)
        self.play(FadeIn(visual), run_time=1.0)
        self.wait(1.5)
        focus_anims = self.dim_others(keep=visual, targets=content_group)
        focus_anims.append(self.emphasize_current(visual))
        self.play(*focus_anims, run_time=0.8)
        self.wait(0.4)
        self.play(Indicate(arrow), run_time=0.7)
        self.wait(0.3)
        self.play(*self.restore_opacity(content_group), run_time=0.6)
        self.wait(0.4)
        self.clear_scene(run_time=0.6)
        self.wait(0.3)

class Scene_08_CommonMistake(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('常见错误通常不是算错，而是看错了不变量。', duration=8.6)
        self.narration_timing_hook('常见错误通常不是算错，而是看错了不变量。', duration=8.6, scene_name='CommonMistake', record_only=True)
        self.add_subcaption('先明确这一段的目标: 指出最常见误区，并用画面解释为什么错。', duration=2.1)
        self.narration_timing_hook('先明确这一段的目标: 指出最常见误区，并用画面解释为什么错。', duration=2.1, scene_name='CommonMistake', record_only=True)
        self.add_subcaption('再看画面设计: 误区气泡出现后被 Cross 标记，再用 Arrow 回到正确的不变量。', duration=2.1)
        self.narration_timing_hook('再看画面设计: 误区气泡出现后被 Cross 标记，再用 Arrow 回到正确的不变量。', duration=2.1, scene_name='CommonMistake', record_only=True)
        self.add_subcaption('这一步的关键是: 指出最常见误区，并用画面解释为什么错。', duration=2.1)
        self.narration_timing_hook('这一步的关键是: 指出最常见误区，并用画面解释为什么错。', duration=2.1, scene_name='CommonMistake', record_only=True)
        # Layout: 横屏 16:9; goal: 指出最常见误区，并用画面解释为什么错。
        title = self.title_text('CommonMistake')
        title.to_edge(UP, buff=0.6)
        goal = self.safe_text_box('指出最常见误区，并用画面解释为什么错。', area="full", font_size=24, color=SECONDARY, max_width=8.4)
        goal.next_to(title, DOWN, buff=0.5)
        box = RoundedRectangle(width=9.5, height=3.8, corner_radius=0.25, color=PRIMARY)
        box.set_stroke(PRIMARY, opacity=0.8).set_fill(PRIMARY, opacity=0.08)
        visual = self.process_flow_pattern(labels=['入口', '处理', '等待', '输出'], area="full", active_index=0, max_width=8.7, move=False)
        visual.move_to(box.get_center())
        dot = Dot(color=ACCENT).scale(1.2).next_to(box, LEFT, buff=0.5)
        arrow = Arrow(start=dot.get_right(), end=box.get_left(), buff=0.15, color=ACCENT)
        content_group = self.compose_visual_pattern(box, visual, dot, arrow, area="full", move=False)
        self.play(Write(title), run_time=1.2)
        self.wait(0.6)
        self.play(FadeIn(goal, shift=DOWN * 0.2), run_time=1.0)
        self.wait(0.6)
        self.play(Create(box), GrowFromCenter(dot), Create(arrow), run_time=1.4)
        self.wait(0.4)
        self.play(FadeIn(visual), run_time=1.0)
        self.wait(1.5)
        focus_anims = self.dim_others(keep=visual, targets=content_group)
        focus_anims.append(self.emphasize_current(visual))
        self.play(*focus_anims, run_time=0.8)
        self.wait(0.4)
        self.play(Indicate(arrow), run_time=0.7)
        self.wait(0.3)
        self.play(*self.restore_opacity(content_group), run_time=0.6)
        self.wait(0.4)
        self.clear_scene(run_time=0.6)
        self.wait(0.3)

class Scene_09_ReflectionChallenge(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('暂停想一想：如果条件换掉，这个模型会怎样调整？', duration=8.6)
        self.narration_timing_hook('暂停想一想：如果条件换掉，这个模型会怎样调整？', duration=8.6, scene_name='ReflectionChallenge', record_only=True)
        self.add_subcaption('先明确这一段的目标: 给出互动思考，让观众暂停迁移到新问题。', duration=2.1)
        self.narration_timing_hook('先明确这一段的目标: 给出互动思考，让观众暂停迁移到新问题。', duration=2.1, scene_name='ReflectionChallenge', record_only=True)
        self.add_subcaption('再看画面设计: 思考题卡片、提示箭头和空白答案区依次出现，保留暂停节奏。', duration=2.1)
        self.narration_timing_hook('再看画面设计: 思考题卡片、提示箭头和空白答案区依次出现，保留暂停节奏。', duration=2.1, scene_name='ReflectionChallenge', record_only=True)
        self.add_subcaption('这一步的关键是: 给出互动思考，让观众暂停迁移到新问题。', duration=2.1)
        self.narration_timing_hook('这一步的关键是: 给出互动思考，让观众暂停迁移到新问题。', duration=2.1, scene_name='ReflectionChallenge', record_only=True)
        # Layout: 横屏 16:9; goal: 给出互动思考，让观众暂停迁移到新问题。
        title = self.title_text('ReflectionChallenge')
        title.to_edge(UP, buff=0.6)
        goal = self.safe_text_box('给出互动思考，让观众暂停迁移到新问题。', area="full", font_size=24, color=SECONDARY, max_width=8.4)
        goal.next_to(title, DOWN, buff=0.5)
        box = RoundedRectangle(width=9.5, height=3.8, corner_radius=0.25, color=PRIMARY)
        box.set_stroke(PRIMARY, opacity=0.8).set_fill(PRIMARY, opacity=0.08)
        visual = self.process_flow_pattern(labels=['入口', '处理', '等待', '输出'], area="full", active_index=0, max_width=8.7, move=False)
        visual.move_to(box.get_center())
        dot = Dot(color=ACCENT).scale(1.2).next_to(box, LEFT, buff=0.5)
        arrow = Arrow(start=dot.get_right(), end=box.get_left(), buff=0.15, color=ACCENT)
        content_group = self.compose_visual_pattern(box, visual, dot, arrow, area="full", move=False)
        self.play(Write(title), run_time=1.2)
        self.wait(0.6)
        self.play(FadeIn(goal, shift=DOWN * 0.2), run_time=1.0)
        self.wait(0.6)
        self.play(Create(box), GrowFromCenter(dot), Create(arrow), run_time=1.4)
        self.wait(0.4)
        self.play(FadeIn(visual), run_time=1.0)
        self.wait(1.5)
        focus_anims = self.dim_others(keep=visual, targets=content_group)
        focus_anims.append(self.emphasize_current(visual))
        self.play(*focus_anims, run_time=0.8)
        self.wait(0.4)
        self.play(Indicate(arrow), run_time=0.7)
        self.wait(0.3)
        self.play(*self.restore_opacity(content_group), run_time=0.6)
        self.wait(0.4)
        self.clear_scene(run_time=0.6)
        self.wait(0.3)

class Scene_10_Summary(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('最后把这条路径带走：先看模型，再桥接符号，最后用例题检验。', duration=8.6)
        self.narration_timing_hook('最后把这条路径带走：先看模型，再桥接符号，最后用例题检验。', duration=8.6, scene_name='Summary', record_only=True)
        self.add_subcaption('先明确这一段的目标: 总结并给出可迁移的理解方法。', duration=2.9)
        self.narration_timing_hook('先明确这一段的目标: 总结并给出可迁移的理解方法。', duration=2.9, scene_name='Summary', record_only=True)
        self.add_subcaption('再看画面设计: recap_board 依次收束问题、模型、例题、边界和思考题。', duration=2.9)
        self.narration_timing_hook('再看画面设计: recap_board 依次收束问题、模型、例题、边界和思考题。', duration=2.9, scene_name='Summary', record_only=True)
        # Layout: 横屏 16:9; goal: 总结并给出可迁移的理解方法。
        title = self.title_text('Summary')
        title.to_edge(UP, buff=0.6)
        goal = self.safe_text_box('总结并给出可迁移的理解方法。', area="full", font_size=24, color=SECONDARY, max_width=8.4)
        goal.next_to(title, DOWN, buff=0.5)
        box = RoundedRectangle(width=9.5, height=3.8, corner_radius=0.25, color=PRIMARY)
        box.set_stroke(PRIMARY, opacity=0.8).set_fill(PRIMARY, opacity=0.08)
        visual = self.process_flow_pattern(labels=['入口', '节点', '风险', '输出'], area="full", active_index=2, max_width=8.7, move=False)
        visual.move_to(box.get_center())
        dot = Dot(color=ACCENT).scale(1.2).next_to(box, LEFT, buff=0.5)
        arrow = Arrow(start=dot.get_right(), end=box.get_left(), buff=0.15, color=ACCENT)
        content_group = self.compose_visual_pattern(box, visual, dot, arrow, area="full", move=False)
        self.play(Write(title), run_time=1.2)
        self.wait(0.6)
        self.play(FadeIn(goal, shift=DOWN * 0.2), run_time=1.0)
        self.wait(0.6)
        self.play(Create(box), GrowFromCenter(dot), Create(arrow), run_time=1.4)
        self.wait(0.4)
        self.play(FadeIn(visual), run_time=1.0)
        self.wait(1.5)
        focus_anims = self.dim_others(keep=visual, targets=content_group)
        focus_anims.append(self.emphasize_current(visual))
        self.play(*focus_anims, run_time=0.8)
        self.wait(0.4)
        self.play(Indicate(arrow), run_time=0.7)
        self.wait(0.3)
        self.play(*self.restore_opacity(content_group), run_time=0.6)
        self.wait(0.4)
        self.clear_scene(run_time=0.6)
        self.wait(0.3)

# END