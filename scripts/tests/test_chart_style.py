# -*- coding: utf-8 -*-
import sys

from dih_models.plotting.chart_style import format_tick_value


if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore


def test_format_tick_value_preserves_sub_cent_currency_precision() -> None:
    assert format_tick_value(0.000134, unit="USD/DALY") == "$0.000134"
    assert format_tick_value(-0.00004, unit="USD") == "-$0.00004"


def test_format_tick_value_keeps_existing_zero_and_cent_formatting() -> None:
    assert format_tick_value(0, unit="USD") == "$0"
    assert format_tick_value(0.01, unit="USD") == "$0.01"
    assert format_tick_value(0.5, unit="USD") == "$0.50"


def test_format_tick_value_preserves_small_non_currency_values() -> None:
    assert format_tick_value(0.000134, unit="ratio") == "0.000134"
