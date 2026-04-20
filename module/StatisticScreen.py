import threading
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import pygame
import seaborn as sns

_GRAPH_KEYS = ["line_plot", "scatter_plot", "bar_plot", "table_plot", "box_plot"]
_GRAPH_LABELS = [
    "Reaction Time vs Score",
    "Session Time vs Inputs",
    "Action Frequency",
    "Success Rate Table",
    "Input Burst by Interval",
]

COL_BG = (0, 0, 0)
COL_TITLE = (200, 30, 30)
COL_TEXT = (180, 180, 180)
COL_SEL = (230, 230, 50)
COL_DIM = (80, 80, 80)


class StatisticScreen:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.done = False
        self.chosen = None

        sw, sh = screen.get_size()
        self.sw, self.sh = sw, sh

        self._index = 0

        try:
            self._font_title = pygame.font.Font(None, int(sh * 0.07))
            self._font_label = pygame.font.Font(None, int(sh * 0.04))
            self._font_hint = pygame.font.Font(None, int(sh * 0.032))
        except Exception:
            self._font_title = pygame.font.SysFont("arial", int(sh * 0.07))
            self._font_label = pygame.font.SysFont("arial", int(sh * 0.04))
            self._font_hint = pygame.font.SysFont("arial", int(sh * 0.032))

        Xlsx_path = Path.cwd() / "Data.xlsx"
        self._graphs_dir = Path.cwd() / "graphs"
        self._graphs_dir.mkdir(exist_ok=True)
        self._graph_surfaces = {}

        columns = [
            "Timestamp",
            "Session Time",
            "Event type",
            "Threat Name",
            "Aggro level",
            "Action",
            "Survived",
            "Score",
            "Input Count",
        ]

        self.df = pd.DataFrame(columns=columns)
        self._has_data = False
        self._animatronics = []
        self._active_filters = set()
        self._loading = False
        self.reset()
        if Xlsx_path.exists():
            self.df = pd.read_excel(Xlsx_path)
            self.__annoted_df()
            self._has_data = True
            self._animatronics = sorted(
                self.reaction_df["Threat Name"].dropna().unique().tolist()
            )
            self._active_filters = set(self._animatronics)
            self._loading = True
            threading.Thread(target=self._bg_generate_all, daemon=True).start()

    def _bg_generate_all(self):
        self._generate_all()
        self._loading = False

    def _filtered_reaction_df(self):
        if self._active_filters and self._animatronics:
            return self.reaction_df[
                self.reaction_df["Threat Name"].isin(self._active_filters)
            ]
        return self.reaction_df

    def _generate_all(self):
        filtered = self._filtered_reaction_df()
        self.line_plot(filtered)
        self.scatter_plot()
        self.bar_plot()
        self.table_plot(filtered)
        self.box_plot()

    def _regenerate_filtered(self):
        if self._loading:
            return
        filtered = self._filtered_reaction_df()
        self.line_plot(filtered)
        self.table_plot(filtered)
        self._graph_surfaces.pop("line_plot", None)
        self._graph_surfaces.pop("table_plot", None)

    def reset(self):
        self.done = False
        self.chosen = None
        self._index = 0
        self._back_rect = pygame.Rect(0, 0, 0, 0)
        self._arrow_left_rect = pygame.Rect(0, 0, 0, 0)
        self._arrow_right_rect = pygame.Rect(0, 0, 0, 0)
        self._filter_button_rects = []

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.done = True
                self.chosen = "Back"
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self._index = (self._index + 1) % len(_GRAPH_KEYS)
                self._graph_surfaces.clear()
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self._index = (self._index - 1) % len(_GRAPH_KEYS)
                self._graph_surfaces.clear()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._back_rect.collidepoint(event.pos):
                self.done = True
                self.chosen = "Back"
            elif self._arrow_left_rect.collidepoint(event.pos):
                self._index = (self._index - 1) % len(_GRAPH_KEYS)
                self._graph_surfaces.clear()
            elif self._arrow_right_rect.collidepoint(event.pos):
                self._index = (self._index + 1) % len(_GRAPH_KEYS)
                self._graph_surfaces.clear()
            else:
                for name, rect in self._filter_button_rects:
                    if rect.collidepoint(event.pos):
                        if name in self._active_filters:
                            if len(self._active_filters) > 1:
                                self._active_filters.discard(name)
                        else:
                            self._active_filters.add(name)
                        self._regenerate_filtered()
                        break

    def process(self):
        pass

    def render(self):
        screen = self.screen
        sw, sh = self.sw, self.sh
        screen.fill(COL_BG)

        # Title
        title_surf = self._font_title.render("STATISTICS", True, COL_TITLE)
        screen.blit(title_surf, (sw // 2 - title_surf.get_width() // 2, int(sh * 0.03)))

        # Filter toggle buttons
        self._filter_button_rects = []
        if self._animatronics:
            btn_w, btn_h = 100, 28
            btn_gap = 8
            total_w = (
                len(self._animatronics) * btn_w
                + (len(self._animatronics) - 1) * btn_gap
            )
            btn_start_x = sw // 2 - total_w // 2
            btn_y = int(sh * 0.10)
            for i, name in enumerate(self._animatronics):
                bx = btn_start_x + i * (btn_w + btn_gap)
                rect = pygame.Rect(bx, btn_y, btn_w, btn_h)
                active = name in self._active_filters
                bg_col = (160, 25, 25) if active else (30, 30, 30)
                border_col = COL_SEL if active else COL_DIM
                text_col = (255, 255, 255) if active else COL_DIM
                pygame.draw.rect(screen, bg_col, rect, border_radius=5)
                pygame.draw.rect(screen, border_col, rect, width=1, border_radius=5)
                lbl = self._font_hint.render(name, True, text_col)
                screen.blit(
                    lbl,
                    (
                        bx + btn_w // 2 - lbl.get_width() // 2,
                        btn_y + btn_h // 2 - lbl.get_height() // 2,
                    ),
                )
                self._filter_button_rects.append((name, rect))

        if self._loading:
            msg = self._font_label.render("Loading graphs...", True, COL_DIM)
            screen.blit(msg, (sw // 2 - msg.get_width() // 2, sh // 2 - msg.get_height() // 2))
        elif not self._has_data:
            msg = self._font_label.render(
                "No data yet — play a round first.", True, COL_TEXT
            )
            screen.blit(
                msg, (sw // 2 - msg.get_width() // 2, sh // 2 - msg.get_height() // 2)
            )
        else:
            # Graph area
            graph_rect = pygame.Rect(
                int(sw * 0.05), int(sh * 0.16), int(sw * 0.90), int(sh * 0.65)
            )
            key = _GRAPH_KEYS[self._index]
            self._render_graph(screen, key, graph_rect)

            # Graph label
            label = _GRAPH_LABELS[self._index]
            label_surf = self._font_label.render(label, True, COL_SEL)
            screen.blit(
                label_surf, (sw // 2 - label_surf.get_width() // 2, int(sh * 0.83))
            )

            # Page indicator  e.g.  2 / 5
            indicator = self._font_hint.render(
                f"{self._index + 1} / {len(_GRAPH_KEYS)}", True, COL_TEXT
            )
            screen.blit(
                indicator, (sw // 2 - indicator.get_width() // 2, int(sh * 0.88))
            )

        # Arrow buttons
        arrow_y = int(sh * 0.92)
        left_surf = self._font_label.render("< PREV", True, COL_TEXT)
        right_surf = self._font_label.render("NEXT >", True, COL_TEXT)
        left_x = int(sw * 0.15)
        right_x = int(sw * 0.85) - right_surf.get_width()
        screen.blit(left_surf, (left_x, arrow_y))
        screen.blit(right_surf, (right_x, arrow_y))
        self._arrow_left_rect = pygame.Rect(
            left_x, arrow_y, left_surf.get_width(), left_surf.get_height()
        )
        self._arrow_right_rect = pygame.Rect(
            right_x, arrow_y, right_surf.get_width(), right_surf.get_height()
        )

        # Back button
        back_surf = self._font_hint.render("[ ESC ] Back to Menu", True, COL_DIM)
        back_x = sw // 2 - back_surf.get_width() // 2
        back_y = int(sh * 0.96)
        screen.blit(back_surf, (back_x, back_y))
        self._back_rect = pygame.Rect(
            back_x, back_y, back_surf.get_width(), back_surf.get_height()
        )

    def __annoted_df(self):
        action_types = {"Door", "Mask", "TurnRight", "TurnLeft", "Submit", "PC"}
        session_indices = self.df.index[self.df["Event type"] == "Session"].tolist()
        session_indices.append(len(self.df))

        encounters = self.df[self.df["Event type"] == "Encounter"].copy()

        results = []
        for index in encounters.index:
            enc_time = self.df.at[index, "Timestamp"]
            next_session = next((s for s in session_indices if s > index), len(self.df))

            reaction = None
            next_action = None

            for j in range(index + 1, next_session):
                if self.df.at[j, "Event type"] in action_types:
                    reaction = (self.df.at[j, "Timestamp"] - enc_time).total_seconds()
                    next_action = self.df.at[j, "Event type"]
                    break

            results.append(
                {
                    "Threat Name": self.df.at[index, "Threat Name"],
                    "Session Time (s)": self.df.at[index, "Session Time"],
                    "Player Action": next_action,
                    "Reaction Time (s)": round(reaction, 3)
                    if reaction is not None
                    else None,
                    "Survived": self.df.at[index, "Survived"],
                    "Score": self.df.at[index, "Score"],
                }
            )

        self.reaction_df = pd.DataFrame(results)

    def _save_figure(self, name):
        path = self._graphs_dir / f"{name}.png"
        plt.savefig(path, dpi=100, bbox_inches="tight")
        plt.close()
        self._graph_surfaces.pop(name, None)

    def _render_graph(self, screen, name, dest):
        if name not in self._graph_surfaces:
            path = self._graphs_dir / f"{name}.png"
            if not path.exists():
                return
            self._graph_surfaces[name] = pygame.image.load(str(path)).convert()
        surf = self._graph_surfaces[name]
        scaled = pygame.transform.smoothscale(surf, (dest.width, dest.height))
        screen.blit(scaled, dest.topleft)

    def line_plot(self, df=None):
        fig, ax = plt.subplots(figsize=(10, 5))
        data = (df if df is not None else self.reaction_df).dropna()
        sns.lineplot(
            data=data,
            x="Score",
            y="Reaction Time (s)",
            hue="Survived",
            palette={1: "#2ecc71", 0: "#e74c3c"},
            marker="o",
            linewidth=2,
            markersize=7,
            ax=ax,
        )
        ax.set_xlim(0, 100)
        ax.set_xticks(range(0, 101, 10))
        ax.set_title(
            "Player Reaction Time vs Score", fontsize=14, fontweight="bold", pad=12
        )
        ax.set_xlabel("Score", fontsize=11)
        ax.set_ylabel("Reaction Time (s)", fontsize=11)
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, ["Died", "Survived"], title="Outcome", title_fontsize=10)
        sns.despine()
        plt.tight_layout()
        self._save_figure("line_plot")

    def scatter_plot(self):
        survive_df = self.df[self.df["Survived"].notna()].copy()
        q_low = survive_df["Session Time"].quantile(0.05)
        q_high = survive_df["Session Time"].quantile(0.95)
        survive_df = survive_df[survive_df["Session Time"].between(q_low, q_high)]
        survive_df["Outcome"] = survive_df["Survived"].map({1: "Survived", 0: "Died"})

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.scatterplot(
            data=survive_df,
            x="Session Time",
            y="Input Count",
            hue="Outcome",
            palette={"Survived": "#2ecc71", "Died": "#e74c3c"},
            alpha=0.75,
            edgecolor="white",
            linewidth=0.4,
            s=60,
            ax=ax,
        )
        ax.set_title(
            "Session Time vs Number of Inputs", fontsize=14, fontweight="bold", pad=12
        )
        ax.set_xlabel("Session Time (s)", fontsize=11)
        ax.set_ylabel("Input Count", fontsize=11)
        ax.grid(linestyle="--", alpha=0.4)
        ax.legend(title="Outcome", title_fontsize=10)
        sns.despine()
        plt.tight_layout()
        self._save_figure("scatter_plot")

    def bar_plot(self):
        action_types = {"Door", "Mask", "PC"}
        action_df = self.df[self.df["Event type"].isin(action_types)]

        fig, ax = plt.subplots(figsize=(10, 5))
        palette = sns.color_palette("muted", n_colors=len(action_types))
        sns.countplot(
            data=action_df,
            x="Event type",
            hue="Event type",
            order=sorted(action_types),
            palette=palette,
            legend=False,
            edgecolor="white",
            linewidth=0.8,
            ax=ax,
        )
        for bar in ax.patches:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.3,
                int(bar.get_height()),
                ha="center",
                va="bottom",
                fontsize=10,
            )
        ordered = sorted(action_types)
        ax.set_xticks(range(len(ordered)))
        ax.set_xticklabels(ordered, fontsize=10)
        ax.set_title("Action Type Frequency", fontsize=14, fontweight="bold", pad=12)
        ax.set_xlabel("Action Type", fontsize=11)
        ax.set_ylabel("Count", fontsize=11)
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        ax.set_axisbelow(True)
        sns.despine()
        plt.tight_layout()
        self._save_figure("bar_plot")

    def table_plot(self, df=None):
        source = df if df is not None else self.reaction_df
        table_df = (
            source.groupby("Threat Name")["Survived"]
            .apply(lambda x: f"{x.mean() * 100:.0f}%")
            .reset_index()
        )
        table_df.columns = ["Threat Name", "Success Rate"]

        fig, ax = plt.subplots(figsize=(6, max(2, len(table_df) * 0.55 + 1)))
        ax.axis("off")
        tbl = ax.table(
            cellText=table_df.values,
            colLabels=table_df.columns,
            loc="center",
            cellLoc="center",
        )
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(11)
        tbl.scale(1.4, 1.6)
        header_color = "#2c3e50"
        row_colors = ["#f0f0f0", "#ffffff"]
        for (row, col), cell in tbl.get_celld().items():
            cell.set_edgecolor("#cccccc")
            if row == 0:
                cell.set_facecolor(header_color)
                cell.set_text_props(color="white", fontweight="bold")
            else:
                cell.set_facecolor(row_colors[row % 2])
        ax.set_title(
            "Success Rate per Animatronic", fontsize=14, fontweight="bold", pad=16
        )
        plt.tight_layout()
        self._save_figure("table_plot")

    def box_plot(self):
        action_types = {"Door", "Mask", "TurnRight", "TurnLeft", "Submit", "PC"}
        action_df = self.df[self.df["Event type"].isin(action_types)].copy()
        action_df["Time Interval (s)"] = (
            action_df["Timestamp"].diff().dt.total_seconds()
        )
        action_df = action_df.dropna(subset=["Time Interval (s)"])
        action_df = action_df[action_df["Time Interval (s)"] > 0]
        q_low = action_df["Time Interval (s)"].quantile(0.01)
        q_high = action_df["Time Interval (s)"].quantile(0.99)
        action_df = action_df[action_df["Time Interval (s)"].between(q_low, q_high)]
        action_df["Time Range"] = pd.cut(
            action_df["Time Interval (s)"],
            bins=[0, 1, 2, 3, 4, 5],
            labels=["0-1s", "1-2s", "2-3s", "3-4s", "4-5s"],
        )

        fig, ax = plt.subplots(figsize=(9, 5))
        palette = sns.color_palette("coolwarm", n_colors=5)
        sns.boxplot(
            data=action_df,
            x="Time Range",
            y="Input Count",
            hue="Time Range",
            palette=palette,
            legend=False,
            linewidth=1.2,
            flierprops={"marker": "o", "markersize": 4, "alpha": 0.5},
            ax=ax,
        )
        ax.set_title(
            "Input Burst Count by Time Interval Between Actions",
            fontsize=14,
            fontweight="bold",
            pad=12,
        )
        ax.set_xlabel("Time Between Inputs (seconds)", fontsize=11)
        ax.set_ylabel("Input Count", fontsize=11)
        ax.set_xticklabels(["0–1s", "1–2s", "2–3s", "3–4s", "4–5s"], fontsize=10)
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        ax.set_axisbelow(True)
        sns.despine()
        plt.tight_layout()
        self._save_figure("box_plot")

    def render_line_plot(self, screen, dest):
        self._render_graph(screen, "line_plot", dest)

    def render_scatter_plot(self, screen, dest):
        self._render_graph(screen, "scatter_plot", dest)

    def render_bar_plot(self, screen, dest):
        self._render_graph(screen, "bar_plot", dest)

    def render_table_plot(self, screen, dest):
        self._render_graph(screen, "table_plot", dest)

    def render_box_plot(self, screen, dest):
        self._render_graph(screen, "box_plot", dest)
