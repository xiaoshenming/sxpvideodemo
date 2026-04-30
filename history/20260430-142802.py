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

class Scene_01_EntryPoint(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('先看这个流程从哪里被触发，以及最后要交付什么结果。', duration=7.0)
        # Layout: 横屏 16:9; goal: 先定位触发事件、参与角色和目标输出。
        title = self.title_text('EntryPoint')
        title.to_edge(UP, buff=0.6)
        goal = self.safe_text_box('先定位触发事件、参与角色和目标输出。', area="full", font_size=24, color=SECONDARY, max_width=8.4)
        goal.next_to(title, DOWN, buff=0.5)
        box = RoundedRectangle(width=9.5, height=3.8, corner_radius=0.25, color=PRIMARY)
        box.set_stroke(PRIMARY, opacity=0.8).set_fill(PRIMARY, opacity=0.08)
        visual = self.safe_text_box('入口事件卡片进入 process_flow swimlane，左右分别放角色和输出，用 Arrow 标出第一跳。', area="full", font_size=22, color=WHITE, max_width=8.7)
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

class Scene_02_FlowSegments(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('流程拆成节点之后，每一步的责任和等待点就能被单独检查。', duration=8.6)
        # Layout: 横屏 16:9; goal: 把主流程拆成可检查的连续节点，避免一团文字。
        title = self.title_text('FlowSegments')
        title.to_edge(UP, buff=0.6)
        goal = self.safe_text_box('把主流程拆成可检查的连续节点，避免一团文字。', area="full", font_size=24, color=SECONDARY, max_width=8.4)
        goal.next_to(title, DOWN, buff=0.5)
        box = RoundedRectangle(width=9.5, height=3.8, corner_radius=0.25, color=PRIMARY)
        box.set_stroke(PRIMARY, opacity=0.8).set_fill(PRIMARY, opacity=0.08)
        visual = self.safe_text_box('用 process_flow 横向节点串展示接收、处理、等待和升级；当前节点高亮，已完成节点降透明度。', area="full", font_size=22, color=WHITE, max_width=8.7)
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

class Scene_03_StateTransition(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('真正要看的是状态为什么切换，以及哪个条件会把它带到异常分支。', duration=8.6)
        # Layout: 横屏 16:9; goal: 解释关键状态如何被条件触发，而不是只背状态名。
        title = self.title_text('StateTransition')
        title.to_edge(UP, buff=0.6)
        goal = self.safe_text_box('解释关键状态如何被条件触发，而不是只背状态名。', area="full", font_size=24, color=SECONDARY, max_width=8.4)
        goal.next_to(title, DOWN, buff=0.5)
        box = RoundedRectangle(width=9.5, height=3.8, corner_radius=0.25, color=PRIMARY)
        box.set_stroke(PRIMARY, opacity=0.8).set_fill(PRIMARY, opacity=0.08)
        visual = self.safe_text_box('把待处理、处理中、超时、已升级画成 state_transition 图；触发条件贴在箭头旁，异常路径用 ACCENT 强调。', area="full", font_size=22, color=WHITE, max_width=8.7)
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

class Scene_04_RiskRecap(BaseConfigScene):
    def construct(self):
        self.setup_layout()
        self.add_subcaption('最后把可迁移的检查顺序留下：入口、节点、状态、风险和输出。', duration=8.0)
        # Layout: 横屏 16:9; goal: 把风险点、兜底动作和最终输出收束成可迁移检查清单。
        title = self.title_text('RiskRecap')
        title.to_edge(UP, buff=0.6)
        goal = self.safe_text_box('把风险点、兜底动作和最终输出收束成可迁移检查清单。', area="full", font_size=24, color=SECONDARY, max_width=8.4)
        goal.next_to(title, DOWN, buff=0.5)
        box = RoundedRectangle(width=9.5, height=3.8, corner_radius=0.25, color=PRIMARY)
        box.set_stroke(PRIMARY, opacity=0.8).set_fill(PRIMARY, opacity=0.08)
        visual = self.safe_text_box('左侧保留简化 process_flow，右侧显示风险阈值、重试/升级动作和最终输出。', area="full", font_size=22, color=WHITE, max_width=8.7)
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