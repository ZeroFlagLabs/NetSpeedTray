"""
Widget Settings Page (2.0 IA).

Everything about the on-taskbar widget itself - how its stats are laid out (display mode + order),
and how it behaves/sits on the taskbar (free-move, keep-visible-in-fullscreen, tray offset). These
controls used to be scattered across the General page (behavior) and the Hardware page (layout); the
2.0 IA gathers them here so "the widget" is one place.

Slider→Segmented and QListWidget upgrades are intentionally NOT done here - the controls move as-is
(same widgets, same config mappings) so the reshuffle can't silently corrupt a saved value.
"""
from typing import Dict, Any, Callable, List

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QComboBox, QLabel, QHBoxLayout, QSpinBox

from netspeedtray import constants
from netspeedtray.utils import styles as su
from netspeedtray.utils.components import Win11Toggle, SettingCard, Win11ComboBox
from netspeedtray.views.settings.pages._fluent import section_header, page_layout


class WidgetPage(QWidget):
    """Layout (display mode + order) and on-taskbar behavior (free-move, fullscreen, offset)."""

    layout_changed = pyqtSignal()

    def __init__(self, i18n, on_change: Callable[[], None]):
        super().__init__()
        self.i18n = i18n
        self.on_change = on_change
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = page_layout(self)

        # --- Display mode ---
        layout.addWidget(section_header(self.i18n.WIDGET_DISPLAY_MODE_LABEL))
        self.display_mode_combo = Win11ComboBox()
        self.display_mode_combo.addItem(self.i18n.DISPLAY_MODE_NETWORK, userData="network_only")
        self.display_mode_combo.addItem(self.i18n.DISPLAY_MODE_COMBINED, userData="side_by_side")
        self.display_mode_combo.addItem(self.i18n.DISPLAY_MODE_STACKED_COLUMN, userData="side_by_stack")
        self.display_mode_combo.addItem(self.i18n.DISPLAY_MODE_CYCLE, userData="cycle")
        self.display_mode_combo.currentIndexChanged.connect(self.on_change)
        layout.addWidget(self.display_mode_combo)
        note = QLabel(self.i18n.HARDWARE_GRAPH_NOTE)
        note.setWordWrap(True)
        note.setStyleSheet(
            f"color: {su.semantic_colors()['text_secondary']}; background: transparent; padding: 0 2px;")
        layout.addWidget(note)

        # --- Display order ---
        layout.addWidget(section_header(self.i18n.WIDGET_DISPLAY_ORDER_LABEL))
        self.pos_combos: List[QComboBox] = []
        for i in range(3):
            combo = Win11ComboBox()
            combo.addItem(self.i18n.ORDER_TYPE_NETWORK, userData="network")
            combo.addItem(self.i18n.ORDER_TYPE_CPU, userData="cpu")
            combo.addItem(self.i18n.ORDER_TYPE_GPU, userData="gpu")
            combo.addItem(self.i18n.ORDER_TYPE_NONE, userData="none")
            combo.setMinimumWidth(160)
            combo.currentIndexChanged.connect(lambda _, idx=i: self._on_pos_changed(idx))
            layout.addWidget(SettingCard(getattr(self.i18n, f"ORDER_POSITION_{i+1}"), control=combo))
            self.pos_combos.append(combo)

        # --- Section spacing ---
        spacing_control = QWidget()
        spacing_layout = QHBoxLayout(spacing_control)
        spacing_layout.setContentsMargins(0, 0, 0, 0)
        spacing_layout.setSpacing(8)

        self.section_spacing_mode = Win11ComboBox()
        self.section_spacing_mode.addItem(self.i18n.WIDGET_SECTION_SPACING_DEFAULT, userData="default")
        self.section_spacing_mode.addItem(self.i18n.WIDGET_SECTION_SPACING_CUSTOM, userData="custom")
        self.section_spacing_mode.setMinimumWidth(110)
        self.section_spacing_mode.currentIndexChanged.connect(
            self._on_section_spacing_mode_changed
        )

        self.section_spacing_value = QSpinBox()
        self.section_spacing_value.setRange(
            constants.layout.WIDGET_SECTION_SPACING_MIN_PX,
            constants.layout.WIDGET_SECTION_SPACING_MAX_PX,
        )
        self.section_spacing_value.setSuffix(" px")
        self.section_spacing_value.setValue(
            constants.layout.WIDGET_SECTION_SPACING_DEFAULT_PX
        )
        self.section_spacing_value.setMinimumWidth(80)
        self.section_spacing_value.setEnabled(False)
        self.section_spacing_value.valueChanged.connect(self.on_change)

        spacing_layout.addWidget(self.section_spacing_mode)
        spacing_layout.addWidget(self.section_spacing_value)

        layout.addWidget(SettingCard(self.i18n.WIDGET_SECTION_SPACING_LABEL, control=spacing_control))

        self.section_dividers = Win11Toggle(label_text="")
        self.section_dividers.toggled.connect(self.on_change)
        layout.addWidget(
            SettingCard(
                self.i18n.WIDGET_SECTION_DIVIDERS_LABEL,
                control=self.section_dividers,
            )
        )

        self.space_before_hardware_units = Win11Toggle(label_text="")
        self.space_before_hardware_units.toggled.connect(self.on_change)
        layout.addWidget(
            SettingCard(
                self.i18n.SPACE_BEFORE_HARDWARE_UNITS_LABEL,
                control=self.space_before_hardware_units,
            )
        )

        # --- Behavior (was on the General page) ---
        layout.addWidget(section_header(self.i18n.BEHAVIOR_GROUP_TITLE))
        self.free_move = Win11Toggle(label_text="")
        self.free_move.toggled.connect(self._on_free_move_toggled)
        layout.addWidget(
            SettingCard(
                self.i18n.FREE_MOVE_LABEL,
                description=(
                    "Allow the widget to be positioned anywhere on the screen. "
                    "Position may need adjusting after changes to displays, "
                    "resolution, scaling/DPI or monitor arrangement."
                ),
                control=self.free_move,
            )
        )

        self.free_move_anchor = Win11ComboBox()
        self.free_move_anchor.addItem("Left", userData="left")
        self.free_move_anchor.addItem("Right", userData="right")
        self.free_move_anchor.setMinimumWidth(110)
        self.free_move_anchor.setEnabled(True)
        self.free_move_anchor.currentIndexChanged.connect(self.on_change)
        layout.addWidget(
            SettingCard(
                "Content Anchor",
                description=(
                    "Choose which side of the visible widget content stays fixed "
                    "when displayed values change width."
                ),
                control=self.free_move_anchor,
            )
        )

        self.lock_position = Win11Toggle(label_text="")
        self.lock_position.setEnabled(True)
        self.lock_position.toggled.connect(self.on_change)
        layout.addWidget(SettingCard(
            getattr(self.i18n, "LOCK_POSITION_LABEL", "Lock Free Move Position"),
            description=getattr(
                self.i18n,
                "LOCK_POSITION_DESCRIPTION",
                "Prevent the widget being accidentally dragged. Display and "
                "taskbar changes may still reposition it when required.",
            ),
            control=self.lock_position,
        ))

        # #188: float the widget on a preferred monitor that has no taskbar of its own.
        self.free_float = Win11Toggle(label_text="")
        self.free_float.toggled.connect(self.on_change)
        layout.addWidget(SettingCard(
            getattr(self.i18n, "FREE_FLOAT_LABEL", "Float on a display without a taskbar"),
            control=self.free_float))

        self.keep_visible_fullscreen = Win11Toggle(label_text="")
        self.keep_visible_fullscreen.toggled.connect(self.on_change)
        layout.addWidget(SettingCard(self.i18n.KEEP_VISIBLE_FULLSCREEN_LABEL,
                                     control=self.keep_visible_fullscreen))

        # NOTE: there is intentionally no tray-offset slider. Free Move (drag the widget anywhere) is the
        # reposition escape hatch; the auto-position uses sensible default offsets. tray_offset_x/y remain
        # in config for the position engine (position_manager) but aren't surfaced as fiddly px sliders.

        layout.addStretch()

    def _on_section_spacing_mode_changed(self, _index: int) -> None:
        custom = self.section_spacing_mode.currentData() == "custom"

        if not custom:
            # Default is a real uniform 10 px layout. Reset the displayed
            # value too, so Default -> Custom never causes a visual jump.
            self.section_spacing_value.blockSignals(True)
            self.section_spacing_value.setValue(
                constants.layout.WIDGET_SECTION_SPACING_DEFAULT_PX
            )
            self.section_spacing_value.blockSignals(False)

        self.section_spacing_value.setEnabled(custom)
        self.on_change()

    # --- behavior ---------------------------------------------------------------
    def _on_free_move_toggled(self, enabled: bool) -> None:
        """Free Move changes positioning mode only; anchor and lock remain independent."""
        self.lock_position.setEnabled(True)
        self.free_move_anchor.setEnabled(True)
        self.on_change()

    def ensure_hardware_visible(self) -> None:
        """Called by the dialog when a hardware monitor is enabled on the Hardware page: switch the
        widget out of network-only so the freshly-enabled stat is actually visible. This is the
        convenience the Hardware page did itself before display-mode moved to this page."""
        if self.display_mode_combo.currentData() == "network_only":
            idx = self.display_mode_combo.findData("side_by_side")
            if idx >= 0:
                self.display_mode_combo.setCurrentIndex(idx)   # fires on_change

    def _on_pos_changed(self, combo_index: int) -> None:
        """Prevents duplicate positional items by auto-swapping with the absent item."""
        values = [c.currentData() for c in self.pos_combos]
        new_val = values[combo_index]
        if new_val == "none":
            self.on_change()
            return
        for i in range(3):
            if i != combo_index and values[i] == new_val:
                used = set(values)
                missing = {"network", "cpu", "gpu"} - used
                if missing:
                    next_item = list(missing)[0]
                    idx = self.pos_combos[i].findData(next_item)
                    if idx >= 0:
                        self.pos_combos[i].blockSignals(True)
                        self.pos_combos[i].setCurrentIndex(idx)
                        self.pos_combos[i].blockSignals(False)
                break
        self.on_change()

    # --- config ------------------------------------------------------------------
    def load_settings(self, config: Dict[str, Any]) -> None:
        mode = config.get("widget_display_mode", "network_only")
        # "side_by_stack" is the side-by-side layout with the hardware column stacked - encoded as
        # widget_display_mode="side_by_side" + stack_hardware_stats=True on disk.
        if mode == "side_by_side" and config.get("stack_hardware_stats", False):
            mode = "side_by_stack"
        index = self.display_mode_combo.findData(mode)
        if index >= 0:
            self.display_mode_combo.setCurrentIndex(index)

        order = config.get("widget_display_order", ["network", "cpu", "gpu"])
        for i, combo in enumerate(self.pos_combos):
            val = order[i] if i < len(order) else "none"
            idx = combo.findData(val)
            if idx >= 0:
                combo.setCurrentIndex(idx)

        spacing = config.get("widget_section_spacing")
        custom_spacing = isinstance(spacing, int) and not isinstance(spacing, bool)

        spacing_mode = "custom" if custom_spacing else "default"
        index = self.section_spacing_mode.findData(spacing_mode)
        if index >= 0:
            self.section_spacing_mode.setCurrentIndex(index)

        self.section_spacing_value.blockSignals(True)

        if custom_spacing:
            self.section_spacing_value.setValue(
                max(
                    constants.layout.WIDGET_SECTION_SPACING_MIN_PX,
                    min(
                        constants.layout.WIDGET_SECTION_SPACING_MAX_PX,
                        spacing,
                    ),
                )
            )
        else:
            self.section_spacing_value.setValue(
                constants.layout.WIDGET_SECTION_SPACING_DEFAULT_PX
            )

        self.section_spacing_value.blockSignals(False)
        self.section_spacing_value.setEnabled(custom_spacing)

        self.section_dividers.setChecked(
            config.get("widget_section_dividers", False)
        )

        self.space_before_hardware_units.setChecked(
            config.get("space_before_hardware_units", False)
        )

        free_move = bool(config.get("free_move", False))
        self.free_move.setChecked(free_move)

        anchor = config.get("free_move_anchor", "right")
        index = self.free_move_anchor.findData(anchor)
        if index >= 0:
            self.free_move_anchor.setCurrentIndex(index)
        self.free_move_anchor.setEnabled(True)

        self.lock_position.setChecked(
            bool(config.get("lock_position", False))
        )
        self.lock_position.setEnabled(True)

        self.free_float.setChecked(config.get("free_float", True))
        self.keep_visible_fullscreen.setChecked(
            config.get("keep_visible_fullscreen", constants.config.defaults.DEFAULT_KEEP_VISIBLE_FULLSCREEN))

    def get_settings(self) -> Dict[str, Any]:
        mode = self.display_mode_combo.currentData()
        order = [c.currentData() for c in self.pos_combos]
        return {
            "widget_display_mode": "side_by_side" if mode == "side_by_stack" else mode,
            "stack_hardware_stats": mode == "side_by_stack",
            "widget_display_order": order,
            "widget_section_spacing": (
                self.section_spacing_value.value()
                if self.section_spacing_mode.currentData() == "custom"
                else None
            ),
            "widget_section_dividers": self.section_dividers.isChecked(),
            "space_before_hardware_units": self.space_before_hardware_units.isChecked(),
            "free_move": self.free_move.isChecked(),
            "free_move_anchor": self.free_move_anchor.currentData(),
            "lock_position": self.lock_position.isChecked(),
            "free_float": self.free_float.isChecked(),
            "keep_visible_fullscreen": self.keep_visible_fullscreen.isChecked(),
        }
