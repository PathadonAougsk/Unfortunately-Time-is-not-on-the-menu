import threading
import tkinter as tk
from pathlib import Path


class _TkHost:
    _instance: "_TkHost | None" = None
    _lock = threading.Lock()

    @classmethod
    def get(cls) -> "_TkHost":
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance

    def __init__(self) -> None:
        self._ready = threading.Event()
        self.root: tk.Tk | None = None
        threading.Thread(target=self._loop, daemon=True).start()
        self._ready.wait()

    def _loop(self) -> None:
        self.root = tk.Tk()
        self.root.withdraw()  # keep it hidden; windows open as Toplevel children
        self._ready.set()
        self.root.mainloop()

    def call(self, fn) -> None:
        """Schedule fn() to run on the Tk thread."""
        self.root.after(0, fn)


import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from PIL import Image, ImageTk

_GRAPH_KEYS = ["line_plot", "scatter_plot", "bar_plot", "table_plot", "box_plot"]
_GRAPH_LABELS = [
    "Reaction Time vs Score",
    "Session Time vs Inputs",
    "Action Frequency",
    "Success Rate Table",
    "Input Burst by Interval",
]

BG = "#0a0a0a"
FG = "#b4b4b4"
ACCENT = "#c81e1e"
SEL = "#e6e632"
DIM = "#505050"
BTN_BG = "#1c1c1c"
BTN_ACTIVE = "#2e2e2e"


class StatisticWindow:
    def __init__(self) -> None:
        self._index = 0
        self._graphs_dir = Path.cwd() / "graphs"
        self._graphs_dir.mkdir(exist_ok=True)
        self._animatronics: list[str] = []
        self._active_filters: set[str] = set()
        self._has_data = False
        self._loading = False
        self.df: pd.DataFrame | None = None
        self.reaction_df: pd.DataFrame | None = None
        self._photo_ref = None  # keep ImageTk ref alive

        xlsx_path = Path.cwd() / "Data.xlsx"
        if xlsx_path.exists():
            self.df = pd.read_excel(xlsx_path)
            self._annotate_df()
            self._has_data = True
            self._animatronics = sorted(
                self.reaction_df["Threat Name"].dropna().unique().tolist()
            )
            self._active_filters = set(self._animatronics)

    def open(self, on_close=None) -> None:
        """Open the stats window. Safe to call multiple times."""
        self._on_close = on_close
        _TkHost.get().call(self._build_window)

    def _close(self) -> None:
        if self._on_close is not None:
            self._on_close()
        self.root.destroy()

    def _build_window(self) -> None:
        """Called on the Tk thread — creates a fresh Toplevel each time."""
        host = _TkHost.get()
        self.root = tk.Toplevel(host.root)
        self.root.title("Statistics — Till 6 AM")
        self.root.configure(bg=BG)
        self.root.geometry("1050x720")
        self.root.minsize(700, 500)
        self.root.protocol("WM_DELETE_WINDOW", self._close)

        self._build_ui()

        if self._has_data:
            self._loading = True
            self._set_status("Loading graphs…")
            threading.Thread(target=self._bg_generate_all, daemon=True).start()
        else:
            self._set_status("No data yet — play a round first.")

    def _build_ui(self) -> None:
        # ---- Title ----
        tk.Label(
            self.root,
            text="STATISTICS",
            font=("Arial", 26, "bold"),
            fg=ACCENT,
            bg=BG,
        ).pack(pady=(14, 2))

        self._filter_frame = tk.Frame(self.root, bg=BG)
        self._filter_frame.pack(fill="x", padx=24, pady=(4, 0))
        self._filter_vars: dict[str, tk.BooleanVar] = {}
        self._build_filter_buttons()

        # ---- Bottom section packed first so the graph doesn't crowd it out ----
        nav = tk.Frame(self.root, bg=BG)
        nav.pack(side="bottom", fill="x", padx=24, pady=(6, 12))

        tk.Button(
            nav,
            text="◀  PREV",
            font=("Arial", 11, "bold"),
            fg=FG,
            bg=BTN_BG,
            activeforeground="#ffffff",
            activebackground=BTN_ACTIVE,
            relief="flat",
            bd=0,
            padx=14,
            pady=6,
            command=self._prev_graph,
        ).pack(side="left")

        tk.Button(
            nav,
            text="Close",
            font=("Arial", 11),
            fg=DIM,
            bg=BTN_BG,
            activeforeground="#ffffff",
            activebackground=BTN_ACTIVE,
            relief="flat",
            bd=0,
            padx=14,
            pady=6,
            command=self._close,
        ).pack(side="left", padx=(8, 0))

        tk.Button(
            nav,
            text="NEXT  ▶",
            font=("Arial", 11, "bold"),
            fg=FG,
            bg=BTN_BG,
            activeforeground="#ffffff",
            activebackground=BTN_ACTIVE,
            relief="flat",
            bd=0,
            padx=14,
            pady=6,
            command=self._next_graph,
        ).pack(side="right")

        self._page_var = tk.StringVar()
        tk.Label(
            self.root,
            textvariable=self._page_var,
            font=("Arial", 10),
            fg=FG,
            bg=BG,
        ).pack(side="bottom")

        self._caption_var = tk.StringVar()
        tk.Label(
            self.root,
            textvariable=self._caption_var,
            font=("Arial", 12, "bold"),
            fg=SEL,
            bg=BG,
        ).pack(side="bottom", pady=(2, 0))

        self._status_var = tk.StringVar()
        self._status_label = tk.Label(
            self.root,
            textvariable=self._status_var,
            font=("Arial", 11),
            fg=DIM,
            bg=BG,
        )
        self._status_label.pack(side="bottom", pady=2)

        # ---- Graph fills remaining space ----
        self._graph_frame = tk.Frame(self.root, bg=BG)
        self._graph_frame.pack(fill="both", expand=True, padx=24, pady=4)

        self._graph_label = tk.Label(self._graph_frame, bg=BG)
        self._graph_label.pack(fill="both", expand=True)

        # ---- Key bindings ----
        self.root.bind("<Left>", lambda _: self._prev_graph())
        self.root.bind("<Right>", lambda _: self._next_graph())
        self.root.bind("<a>", lambda _: self._prev_graph())
        self.root.bind("<d>", lambda _: self._next_graph())
        self.root.bind("<Escape>", lambda _: self._close())
        self.root.bind("<Configure>", lambda _: self._on_resize())

    def _build_filter_buttons(self) -> None:
        for w in self._filter_frame.winfo_children():
            w.destroy()
        self._filter_vars.clear()

        if not self._animatronics:
            return

        tk.Label(
            self._filter_frame,
            text="Filter:",
            font=("Arial", 10),
            fg=DIM,
            bg=BG,
        ).pack(side="left", padx=(0, 8))

        for name in self._animatronics:
            var = tk.BooleanVar(value=True)
            self._filter_vars[name] = var
            tk.Checkbutton(
                self._filter_frame,
                text=name,
                variable=var,
                font=("Arial", 10),
                fg="#ffffff",
                bg=BG,
                selectcolor="#7a1010",
                activebackground=BG,
                activeforeground="#ffffff",
                command=self._on_filter_change,
            ).pack(side="left", padx=4)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def _prev_graph(self) -> None:
        self._index = (self._index - 1) % len(_GRAPH_KEYS)
        if not self._loading:
            self._update_graph_display()

    def _next_graph(self) -> None:
        self._index = (self._index + 1) % len(_GRAPH_KEYS)
        if not self._loading:
            self._update_graph_display()

    def _on_resize(self) -> None:
        if not self._loading and self._has_data:
            self._update_graph_display()

    # ------------------------------------------------------------------
    # Filters
    # ------------------------------------------------------------------

    def _on_filter_change(self) -> None:
        active = {n for n, v in self._filter_vars.items() if v.get()}
        if not active:
            for v in self._filter_vars.values():
                v.set(True)
            active = set(self._animatronics)
        self._active_filters = active
        threading.Thread(target=self._regen_filtered, daemon=True).start()

    def _regen_filtered(self) -> None:
        filtered = self._filtered_reaction_df()
        self.line_plot(filtered)
        self.table_plot(filtered)
        self.root.after(0, self._update_graph_display)

    # ------------------------------------------------------------------
    # Graph display
    # ------------------------------------------------------------------

    def _bg_generate_all(self) -> None:
        self._generate_all()
        self._loading = False
        self.root.after(0, self._on_graphs_ready)

    def _on_graphs_ready(self) -> None:
        self._set_status("")
        self._status_label.pack_forget()
        self._update_graph_display()

    def _set_status(self, msg: str) -> None:
        self._status_var.set(msg)

    def _update_graph_display(self) -> None:
        if not self._has_data:
            return
        key = _GRAPH_KEYS[self._index]
        path = self._graphs_dir / f"{key}.png"
        if not path.exists():
            return

        self._graph_frame.update_idletasks()
        frame_w = max(self._graph_frame.winfo_width(), 600)
        frame_h = max(self._graph_frame.winfo_height(), 380)

        img = Image.open(str(path))
        img_w, img_h = img.size
        scale = min(frame_w / img_w, frame_h / img_h)
        w = int(img_w * scale)
        h = int(img_h * scale)
        img = img.resize((w, h), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        self._graph_label.configure(image=photo)
        self._photo_ref = photo  # prevent GC

        self._caption_var.set(_GRAPH_LABELS[self._index])
        self._page_var.set(f"{self._index + 1} / {len(_GRAPH_KEYS)}")

    # ------------------------------------------------------------------
    # Data helpers
    # ------------------------------------------------------------------

    def _filtered_reaction_df(self) -> pd.DataFrame:
        if self._active_filters and self._animatronics:
            return self.reaction_df[
                self.reaction_df["Threat Name"].isin(self._active_filters)
            ]
        return self.reaction_df

    def _annotate_df(self) -> None:
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

    def _generate_all(self) -> None:
        filtered = self._filtered_reaction_df()
        self.line_plot(filtered)
        self.scatter_plot()
        self.bar_plot()
        self.table_plot(filtered)
        self.box_plot()

    def _save_figure(self, name: str) -> None:
        path = self._graphs_dir / f"{name}.png"
        plt.savefig(path, dpi=100, bbox_inches="tight")
        plt.close()

    # ------------------------------------------------------------------
    # Graph generation (mirrors StatisticScreen)
    # ------------------------------------------------------------------

    def line_plot(self, df: pd.DataFrame | None = None) -> None:
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

    def scatter_plot(self) -> None:
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

    def bar_plot(self) -> None:
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

    def table_plot(self, df: pd.DataFrame | None = None) -> None:
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

    def box_plot(self) -> None:
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
