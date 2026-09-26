# 首页中国地图

`china-geo.json` 下载自 [GeoJSON.CN 中国地图数据集](https://geojson.cn/data/atlas/china)，版本 1.6.3。数据包含台湾、南海诸岛及南海断续线；首页也标注了数据来源。

运行 `python tools/build_china_map.py` 可重新生成静态 `china-map.svg`。地图轻微逆时针旋转，南海纬度作视觉压缩，以便将诸岛接在主图下方。库尔勒和北京的标记坐标写在该脚本中，地点介绍写在 `index.html` 的 `about-scene-places` 区域。
