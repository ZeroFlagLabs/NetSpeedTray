"""Widget settings page (2.0 IA) - the controls that moved here from General (behavior) and Hardware
(layout) must round-trip, and the hardware auto-switch convenience must survive the move."""
import pytest

from netspeedtray.constants.i18n import I18nStrings
from netspeedtray.views.settings.pages.widget import WidgetPage


@pytest.fixture
def page(q_app):
    return WidgetPage(I18nStrings("en_US"), lambda: None)


def test_layout_and_behaviour_round_trip(page):
    page.load_settings({
        "widget_display_mode": "cycle",
        "widget_display_order": ["gpu", "cpu", "network"],
        "free_move": True,
        "keep_visible_fullscreen": True,
    })
    out = page.get_settings()
    assert out["widget_display_mode"] == "cycle"
    assert out["widget_display_order"] == ["gpu", "cpu", "network"]
    assert out["free_move"] is True
    assert out["keep_visible_fullscreen"] is True
    # Tray offset is intentionally not a Widget-page control (Free Move handles repositioning).
    assert "tray_offset_x" not in out
    assert "tray_offset_y" not in out


def test_stacked_mode_encoding_round_trips(page):
    """side_by_stack is stored as widget_display_mode=side_by_side + stack_hardware_stats=True - the
    encoding must survive load->get unchanged (a corruption here silently changes the widget layout)."""
    page.load_settings({"widget_display_mode": "side_by_side", "stack_hardware_stats": True})
    out = page.get_settings()
    assert out["widget_display_mode"] == "side_by_side"
    assert out["stack_hardware_stats"] is True


def test_ensure_hardware_visible_leaves_network_only(page):
    """The convenience the Hardware page used to do itself: enabling a monitor switches the widget out
    of network-only so the new stat is visible."""
    page.load_settings({"widget_display_mode": "network_only"})
    assert page.get_settings()["widget_display_mode"] == "network_only"
    page.ensure_hardware_visible()
    assert page.get_settings()["widget_display_mode"] == "side_by_side"


def test_ensure_hardware_visible_respects_existing_choice(page):
    """If the user already picked a non-network-only mode, enabling a monitor must NOT override it."""
    page.load_settings({"widget_display_mode": "cycle"})
    page.ensure_hardware_visible()
    assert page.get_settings()["widget_display_mode"] == "cycle"

def test_section_spacing_defaults_to_uniform_layout(page):
    """Default mode uses the fixed uniform section spacing."""
    page.load_settings({})

    assert page.section_spacing_mode.currentData() == "default"
    assert page.section_spacing_value.value() == 10
    assert page.section_spacing_value.isEnabled() is False
    assert page.get_settings()["widget_section_spacing"] is None


def test_custom_section_spacing_round_trips(page):
    """A custom spacing value is restored and returned unchanged."""
    page.load_settings({"widget_section_spacing": 18})

    assert page.section_spacing_mode.currentData() == "custom"
    assert page.section_spacing_value.value() == 18
    assert page.section_spacing_value.isEnabled() is True
    assert page.get_settings()["widget_section_spacing"] == 18


def test_returning_to_default_resets_custom_spacing_to_ten(page):
    """Leaving Custom mode resets the suggested custom value to 10 px."""
    page.load_settings({"widget_section_spacing": 18})

    default_index = page.section_spacing_mode.findData("default")
    assert default_index >= 0

    page.section_spacing_mode.setCurrentIndex(default_index)

    assert page.section_spacing_mode.currentData() == "default"
    assert page.section_spacing_value.value() == 10
    assert page.section_spacing_value.isEnabled() is False
    assert page.get_settings()["widget_section_spacing"] is None


def test_section_dividers_default_off_and_round_trip(page):
    """Section dividers are opt-in and the Widget page preserves the setting."""
    page.load_settings({})

    assert page.section_dividers.isChecked() is False
    assert page.get_settings()["widget_section_dividers"] is False

    page.load_settings({"widget_section_dividers": True})

    assert page.section_dividers.isChecked() is True
    assert page.get_settings()["widget_section_dividers"] is True
