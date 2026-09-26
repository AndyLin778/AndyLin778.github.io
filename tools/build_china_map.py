"""Build the static China map used on the homepage.

Source geometry: GeoJSON.CN China 1.6.3 (assets/maps/china-geo.json).
The generated SVG has no runtime dependency on the source data.
"""

import json
import math
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "maps" / "china-geo.json"
OUTPUT = ROOT / "assets" / "maps" / "china-map.svg"
ROTATION = -8
ROTATION_CENTER = (460, 290)


def polygons(geometry):
    if geometry["type"] == "Polygon":
        yield geometry["coordinates"]
    elif geometry["type"] == "MultiPolygon":
        yield from geometry["coordinates"]


def main_xy(point):
    lon, lat = point[:2]
    # 南海纬度作适度压缩，让诸岛保留在主图下方，而不另设附图。
    y = 40 + (53.6 - max(lat, 18)) * 11.8
    if lat < 18:
        y += (18 - lat) * 5.8
    return 30 + (lon - 73.4) * 11.8, y


def rotated_xy(point):
    x, y = main_xy(point)
    cx, cy = ROTATION_CENTER
    angle = math.radians(ROTATION)
    return (
        cx + (x - cx) * math.cos(angle) - (y - cy) * math.sin(angle),
        cy + (x - cx) * math.sin(angle) + (y - cy) * math.cos(angle),
    )


def path_for_polygon(polygon, project):
    parts = []
    for ring in polygon:
        if not ring:
            continue
        points = [project(point) for point in ring]
        parts.append("M" + " ".join(f"{x:.1f},{y:.1f}" for x, y in points) + "Z")
    return " ".join(parts)


def make_svg(data):
    main = []
    dashes = []
    for feature in data["features"]:
        name = feature["properties"]["name"]
        geometry = feature["geometry"]
        if name == "十段线":
            for segment in geometry["coordinates"]:
                pts = [main_xy(point) for point in segment]
                dashes.append("M" + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts))
            continue
        for polygon in polygons(geometry):
            main.append((name, path_for_polygon(polygon, main_xy)))

    provinces = "\n".join(
        f'    <path d="{path}" aria-label="{escape(name)}"/>' for name, path in main
    )
    dash_paths = "\n".join(f'    <path d="{path}"/>' for path in dashes)
    korla = rotated_xy((86.17, 41.73))
    beijing = rotated_xy((116.41, 39.90))
    sea_label = rotated_xy((119.4, 4.2))
    rotation = f"rotate({ROTATION} {ROTATION_CENTER[0]} {ROTATION_CENTER[1]})"

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 580" role="img" aria-labelledby="map-title map-desc">
  <title id="map-title">中国地图：库尔勒与北京</title>
  <desc id="map-desc">中国地图包含台湾与主图下方的南海诸岛，库尔勒和北京以蓝色标记。地图逆时针微旋，南海纬度作了视觉压缩。</desc>
  <metadata>Map geometry: GeoJSON.CN China 1.6.3, https://geojson.cn/data/atlas/china</metadata>
  <style>
    .land path {{ fill: #f1f2f0; stroke: #a6adb0; stroke-width: 1.05; stroke-linejoin: round; vector-effect: non-scaling-stroke; }}
    .sea-lines path {{ fill: none; stroke: #87939a; stroke-width: 1.6; stroke-linecap: round; vector-effect: non-scaling-stroke; }}
    .city-ring {{ fill: #fdfdfd; stroke: #356bff; stroke-width: 1.6; vector-effect: non-scaling-stroke; }}
    .city-dot {{ fill: #356bff; }}
    .city-line {{ stroke: #356bff; stroke-width: 1; vector-effect: non-scaling-stroke; }}
    text {{ font-family: ui-monospace, Consolas, 'Microsoft YaHei', sans-serif; fill: #414c53; font-size: 12px; letter-spacing: .04em; }}
    .city-label {{ fill: #154dcc; font-size: 14px; font-weight: 600; }}
    .sea-label {{ font-size: 11px; fill: #66747b; letter-spacing: .12em; }}
  </style>
  <g class="land" transform="{rotation}">
{provinces}
  </g>
  <g aria-label="库尔勒" transform="translate({korla[0]:.1f} {korla[1]:.1f})">
    <circle class="city-ring" r="8"/><circle class="city-dot" r="3.5"/>
    <path class="city-line" d="M10 0H26"/><text class="city-label" x="32" y="5">库尔勒</text>
  </g>
  <g aria-label="北京" transform="translate({beijing[0]:.1f} {beijing[1]:.1f})">
    <circle class="city-ring" r="8"/><circle class="city-dot" r="3.5"/>
    <path class="city-line" d="M10 0H26"/><text class="city-label" x="32" y="5">北京</text>
  </g>
  <g class="sea-lines" transform="{rotation}">
{dash_paths}
  </g>
  <text class="sea-label" x="{sea_label[0]:.1f}" y="{min(sea_label[1] + 16, 568):.1f}">南海诸岛</text>
</svg>
'''


if __name__ == "__main__":
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    OUTPUT.write_text(make_svg(data), encoding="utf-8")
    print(OUTPUT)
