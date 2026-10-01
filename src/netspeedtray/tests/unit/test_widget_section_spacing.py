from types import SimpleNamespace

from PyQt6.QtCore import QRect

from netspeedtray.utils.widget_paint import WidgetMetrics, _draw_side_by_side


class _FakeRenderer:
    """Capture the x position of each section without relying on font metrics."""

    def __init__(self):
        self.calls = []
        self._last_width = 0

    def draw_network_speeds(self, *args, **kwargs):
        self.calls.append(("network", kwargs["x_offset"]))
        self._last_width = 100

    def draw_hardware_stats(self, *args, **kwargs):
        cpu_usage = args[1]
        gpu_usage = args[2]

        if cpu_usage is not None and gpu_usage is None:
            key = "cpu"
            self._last_width = 50
        elif gpu_usage is not None and cpu_usage is None:
            key = "gpu"
            self._last_width = 60
        else:
            key = "hardware"
            self._last_width = 60

        self.calls.append((key, kwargs["x_offset"]))

    def get_last_text_rect(self):
        return QRect(0, 0, self._last_width, 20)


def _positions(spacing):
    config = SimpleNamespace(
        widget_display_order=["network", "cpu", "gpu"],
        stack_hardware_stats=False,
        monitor_cpu_enabled=True,
        monitor_gpu_enabled=True,
        monitor_ram_enabled=False,
        monitor_vram_enabled=False,
        graph_enabled=False,
        widget_section_spacing=spacing,
    )

    renderer = _FakeRenderer()
    metrics = WidgetMetrics(cpu_usage=3.0, gpu_usage=2.0)

    _draw_side_by_side(
        None,
        renderer,
        width=400,
        height=52,
        config=config,
        metrics=metrics,
        layout="horizontal",
        network_width=100,
    )

    return dict(renderer.calls)



def test_default_section_spacing_uses_uniform_default_geometry():
    """Default uses 10 px visual spacing with renderer-margin compensation."""
    positions = _positions(None)

    assert positions["network"] == 0
    assert positions["cpu"] == 106
    assert positions["gpu"] == 164


def test_custom_section_spacing_applies_to_both_boundaries():
    """One custom value controls both Side-by-Side section boundaries."""
    positions = _positions(18)

    assert positions["network"] == 0
    assert positions["cpu"] == 114
    assert positions["gpu"] == 180


def test_bool_section_spacing_uses_default_layout():
    """bool must not be interpreted as a custom integer spacing value."""
    positions = _positions(True)

    assert positions["network"] == 0
    assert positions["cpu"] == 106
    assert positions["gpu"] == 164
