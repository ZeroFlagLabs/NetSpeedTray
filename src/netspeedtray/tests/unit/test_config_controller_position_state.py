"""Position state must survive unrelated Settings live-preview updates."""

from unittest.mock import MagicMock, patch

from netspeedtray.core.config_controller import ConfigController


def test_settings_preview_preserves_live_docked_position():
    widget = MagicMock()
    widget.config = {
        "free_move": False,
        "position_x": None,
        "position_y": None,
        "docked_position_ratio": 0.73,
        "tray_offset_x": 12,
        "tray_offset_y": 3,
    }

    controller = ConfigController(widget, MagicMock())

    # Simulates the stale SettingsDialog snapshot that existed before the
    # user dragged the widget to its new docked position.
    stale_settings = {
        "free_move": False,
        "lock_position": True,
        "position_x": None,
        "position_y": None,
        "docked_position_ratio": None,
        "tray_offset_x": 999,
        "tray_offset_y": 999,
    }

    with patch.object(controller, "apply_all_settings"):
        controller.handle_settings_changed(
            stale_settings,
            save_to_disk=False,
        )

    assert widget.config["lock_position"] is True
    assert widget.config["docked_position_ratio"] == 0.73
    assert widget.config["tray_offset_x"] == 12
    assert widget.config["tray_offset_y"] == 3

    # The caller's Settings snapshot must not itself be mutated.
    assert stale_settings["docked_position_ratio"] is None


def test_disabling_free_move_still_clears_absolute_coordinates():
    widget = MagicMock()
    widget.config = {
        "free_move": True,
        "position_x": 800,
        "position_y": 500,
        "docked_position_ratio": 0.42,
        "tray_offset_x": 0,
        "tray_offset_y": 3,
    }

    controller = ConfigController(widget, MagicMock())

    settings = {
        "free_move": False,
        "position_x": 100,
        "position_y": 100,
        "docked_position_ratio": None,
    }

    with patch.object(controller, "apply_all_settings"):
        controller.handle_settings_changed(
            settings,
            save_to_disk=False,
        )

    assert widget.config["position_x"] is None
    assert widget.config["position_y"] is None

    # The previous docked placement remains ready for returning to docked mode.
    assert widget.config["docked_position_ratio"] == 0.42
