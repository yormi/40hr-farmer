#!/usr/bin/env python3
"""Peak heat load + electric service check for an arched high tunnel."""
import argparse
import math

U_VALUES = {"single_poly": 1.15, "double_poly": 0.7, "glass": 1.1, "polycarbonate_twinwall": 0.6}  # BTU/h·ft²·°F
BTU_PER_KW = 3412


def half_ellipse_arc(semi_width, rise):
    a, b = semi_width, rise
    return math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b))) / 2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=float, required=True, help="ft")
    parser.add_argument("--length", type=float, required=True, help="ft")
    parser.add_argument("--wall-height", type=float, required=True, help="ft, sidewall")
    parser.add_argument("--peak-height", type=float, required=True, help="ft")
    parser.add_argument("--cover", choices=U_VALUES, default="double_poly")
    parser.add_argument("--air-changes", type=float, default=1.0, help="per hour; 1 if tightness unknown")
    parser.add_argument("--target", type=float, required=True, help="°C inside")
    parser.add_argument("--design-low", type=float, required=True, help="°C outside, coldest night in season")
    parser.add_argument("--service-amps", type=float, default=200)
    parser.add_argument("--service-volts", type=float, default=240)
    parser.add_argument("--existing-load-kw", type=float, default=0)
    arguments = parser.parse_args()

    rise = arguments.peak_height - arguments.wall_height
    cross_section = arguments.width * arguments.wall_height + math.pi / 4 * arguments.width * rise
    roof_and_sides = (2 * arguments.wall_height + half_ellipse_arc(arguments.width / 2, rise)) * arguments.length
    skin_area = roof_and_sides + 2 * cross_section
    volume = cross_section * arguments.length

    delta_fahrenheit = (arguments.target - arguments.design_low) * 1.8
    conduction = U_VALUES[arguments.cover] * skin_area * delta_fahrenheit
    infiltration = 0.018 * volume * arguments.air_changes * delta_fahrenheit
    total_btu = conduction + infiltration
    total_kw = total_btu / BTU_PER_KW
    usable_kw = arguments.service_amps * arguments.service_volts * 0.8 / 1000 - arguments.existing_load_kw

    print(f"Skin area        {skin_area:,.0f} ft²")
    print(f"Volume           {volume:,.0f} ft³")
    print(f"Conduction       {conduction:,.0f} BTU/h")
    print(f"Infiltration     {infiltration:,.0f} BTU/h")
    print(f"Peak load        {total_btu:,.0f} BTU/h = {total_kw:.0f} kW")
    print(f"Per °C gap       {total_kw / (arguments.target - arguments.design_low):.2f} kW/°C")
    print(f"Usable electric  {usable_kw:.0f} kW (80% continuous, minus existing)")
    print(f"Resistance heat  {'fits' if usable_kw >= total_kw else 'does NOT fit'}")
    print(f"Heat pump COP 2  {'fits' if usable_kw >= total_kw / 2 else 'does NOT fit'} (needs {total_kw / 2:.0f} kW)")


if __name__ == "__main__":
    main()
