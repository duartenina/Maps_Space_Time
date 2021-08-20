"""
Shapefile sources
    China provinces:
        https://www.gadm.org/
    Rivers (1820):
        https://geodata.lib.berkeley.edu/?utf8=%E2%9C%93&f%5Bdc_format_s%5D%5B%5D=Shapefile&f%5Bdct_spatial_sm%5D%5B%5D=China&search_field=all_fields&q=river
    Rivers:
        http://worldmap.harvard.edu/data/geonode:River_basin_num2
    Dataverse:
        https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/T27RQO
    Cities/Hydrography/Water Bodies:
        https://tapiquen-sig.jimdofree.com/english-version/free-downloads/china/

"""

import functools
import os

from matplotlib.text import Text
os.environ['PROJ_LIB'] = r'D:\Programs\Anaconda3\Library\share\basemap'
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.path import Path
from matplotlib.collections import LineCollection, PathCollection
from matplotlib.font_manager import FontProperties
import matplotlib.patheffects as PathEffects
from matplotlib import cm
import matplotlib.patches as mpatch
from matplotlib.legend_handler import HandlerBase, HandlerTuple
import shapefile as sp
from china_settings import (
    text_bg_colors, data_folder, image_folder,
    provinces_file, colors_provinces, provinces_info, provinces_skip_outline,
    rivers_file, river_color, river_widths, rivers_info,
    cities_file, cities_info, city_filter_range, cities_colors, cities_sizes,
)

plt.style.use('default')

# c (crude), l (low), i (intermediate), h (high), f (full)
resolution = 'c'
zorders = {
    'ocean': -1,
    'continent': 0,
    'countries': 10,
    'provinces': 20,
    'rivers': 30,
    'par/med': 40,
    'cities': 50,
    'text': 100,
    'legend': 200,
}
PRINT_ALL_CITIES = False


@functools.lru_cache(maxsize=None)
def extract_polygons_from_shapefile(shp_reader, basemap):
    """
    How to add country data:
    https://www.geophysique.be/2013/02/12/matplotlib-basemap-tutorial-10-shapefiles-unleached-continued/
    """

    shapes = shp_reader.shapes()
    records = shp_reader.records()

    records_lines = []

    for record, shape in zip(records,shapes):
        try:
            lons,lats = zip(*shape.points)
        except ValueError:
            continue
        data = np.array(basemap(lons, lats)).T

        is_point = False
        if len(shape.parts) == 0:   # Point
            segs = data
            is_point = True
        elif len(shape.parts) == 1: # Line or Polygon
            segs = [data,]
        else:                       # Line or Polygon
            segs = []
            for i in range(1,len(shape.parts)):
                index = shape.parts[i-1]
                index2 = shape.parts[i]
                segs.append(data[index:index2])
            segs.append(data[index2:])

        if is_point:
            lines = segs
        else:
            lines = LineCollection(segs,antialiaseds=(1,))
        records_lines.append((record, shape, lines))

    return records_lines


def create_basemap(ax):
    basemap = Basemap(
        ax=ax,
        width=5_000_000,
        height=4_250_000,
        projection='lcc',
        resolution=resolution, # c (crude), l (low), i (intermediate), h (high), f (full)
        # lat_1=45.,
        # lat_2=55,
        lat_0=36.5,
        lon_0=102.
    )

    return basemap


def draw_provinces(ax, basemap, show_labels=True, lw_mult=1.,
                   show_outline=False, show_background=True):
    china_data_reader = sp.Reader(provinces_file)
    china_data_line_dict = extract_polygons_from_shapefile(china_data_reader, basemap)
    for record, shape, lines in china_data_line_dict:
        reg_name = record['NAME_1']
        # reg_type = record['ENGTYPE_1']

        bbox = shape.bbox
        # center_lon = np.mean(bbox[::2])
        # center_lat = np.mean(bbox[1::2])
        center_lon, center_lat = np.mean(np.reshape(bbox, (2,2)), axis=0)

        label, (lon, lat), color_code = provinces_info[reg_name]
        facecolor = colors_provinces[color_code]

        if lon == 0:
            lon = center_lon
        if lat == 0:
            lat = center_lat

        if color_code == -1:
            foreground = text_bg_colors['municipality'][0]
        else:
            foreground = text_bg_colors['province'][0]

        if show_outline:
            lines.set_linewidth(lw_mult)
            lines.set_edgecolors('w')
        else:
            lines.set_linewidth(0.)

        if show_background:
            lines.set_facecolors(facecolor)
        else:
            lines.set_facecolors('None')

        lines.set_zorder(zorders['provinces'])

        if show_outline and reg_name in provinces_skip_outline:
            pass
        else:
            ax.add_collection(lines)

        if show_labels:
            if label == '':
                label = reg_name

            txt = plt.annotate(
                label,
                color='k',
                xy=basemap(lon, lat), xycoords='data',
                ha='center', va='center',
                zorder=zorders['text'],
                fontsize=9 if color_code != -1 else 7
            )
            txt.set_path_effects([
                PathEffects.withStroke(linewidth=3, foreground=foreground)
            ])


def draw_rivers(ax, basemap, show_labels=True, lw_mult=1.):
    rivers_data_reader = sp.Reader(rivers_file)
    rivers_data_line_dict = extract_polygons_from_shapefile(rivers_data_reader, basemap)
    for record, shape, lines in rivers_data_line_dict:
        level_river = record['LEVEL_RIVE']
        river_name = record['NAME']
        river_name = river_name.split('(')[0]

        show_river = (
            (level_river in [1, 2, 3, 9])
            # or (river_name in rivers_info[:, 1])
        )

        if not show_river:
            continue

        color = river_color[level_river-1]
        lw = river_widths[level_river-1] * lw_mult

        lines.set_linewidth(lw)
        lines.set_edgecolors(color)
        lines.set_zorder(zorders['rivers'])

        ax.add_collection(lines)

    # font = FontProperties('SimSun')
    if not show_labels:
        return

    for name, chinese, (lon, lat), code in rivers_info:
        if code < 0:
            continue

        txt = plt.annotate(
            # f'{name}\n{chinese}',
            name,
            color='k',
            xy=basemap(lon, lat), xycoords='data',
            ha='center', va='center',
            zorder=zorders['text'],
            fontsize=10 - code*2,       #
            # fontproperties=font
        )
        txt.set_path_effects([
            PathEffects.withStroke(linewidth=3, foreground=text_bg_colors['water body'][0])
        ])


def draw_cities(ax, basemap, show_labels=True, ms_mult=1.):
    reader = sp.Reader(cities_file)
    line_dict = extract_polygons_from_shapefile(reader, basemap)
    for record, shape, lines in line_dict:
        city = record['NAME'].lower()
        city_info = cities_info.get(
            city,
            (city.title(), (0, 0.1), 3, (0, 0))
        )
        name, (left, top), level, filt = city_info

        if (level == 3) and not PRINT_ALL_CITIES:
            continue

        lat, lon = lines[0]
        color = cities_colors[level]
        size_out, size_in = cities_sizes[level]

        if filt != (0, 0):
            filt_lat, filt_lon = basemap(*filt)

            # print('{} {:8.0f} {:8.0f} {:8.0f} {:8.0f}'.format(city, lat, lon, filt_lat, filt_lon))

            if not ((-city_filter_range + filt_lat) < lat < (city_filter_range + filt_lat)):
                continue

            if not((-city_filter_range + filt_lon) < lon < (city_filter_range + filt_lon)):
                continue

        ax.plot(
            lat, lon, 'o',
            ms=size_out * ms_mult,
            color='k',
            zorder=zorders['cities']
        )
        ax.plot(
            lat, lon, 'o',
            ms=size_in * ms_mult,
            color=color,
            zorder=zorders['cities']+1
        )

        if name is None:
            continue

        if name == '':
            name = city.title()

        va = 'center'
        ha = 'center'
        if top != 0:
            va = 'top' if top < 0 else 'bottom'
        elif left != 0:
            ha = 'left' if left > 0 else 'right'

        if show_labels:
            txt = plt.annotate(
                name,
                xy=(lat + left * 25_000, lon + top * 25_000), xycoords='data',
                ha=ha, va=va,
                color='k', zorder=zorders['text'],
                fontsize=(8 - level)
            )
            txt.set_path_effects([
                PathEffects.withStroke(linewidth=3, foreground=text_bg_colors['city'][0])
            ])


class TextHandlerA(HandlerBase):
    def create_artists(self, legend, artist ,xdescent, ydescent,
                        width, height, fontsize, trans):
        color = artist.get_color()
        fontsize = artist.get_fontsize()
        tx = Text(width/2.,height/2, artist.get_text(), fontsize=fontsize,
                  ha="center", va="center", color='k')
        tx.set_path_effects([
            PathEffects.withStroke(linewidth=3, foreground=color)
        ])
        return [tx]


def add_legends(ax, loc='best', ncol=1, bbox=None):
    handles_labels = []

    # Province Colors
    # recs = []
    # for color in colors_provinces[:-1]:
    #     line, = ax.plot(np.nan, 's', color=color)
    #     recs.append(line)
    # handles_labels.append(
    #     [tuple(recs), 'Province']
    # )

    # line, = ax.plot(np.nan, 's', color=colors_provinces[-1])
    # handles_labels.append([line, 'Municipality'])

    # line, = ax.plot(np.nan, 'o', alpha=0)
    # handles_labels.append([line, ''])

    # Labels
    for type in text_bg_colors:
        color, text = text_bg_colors[type]
        label = type.title()
        txt = Text(np.nan, np.nan, text, color=color, fontsize=8)
        handles_labels.append([txt, label])

    # Rivers
    river_legends = ((0, 'Major River'), (1, 'River'), (8, 'Grand Canal'))
    for n, label in river_legends:
        line, = ax.plot(np.nan, '-', color=river_color[n], lw=river_widths[n])
        handles_labels.append([line, label])

    # Cities
    city_legends = ('Country Capital', 'Province Capital', 'City')
    for n, label in enumerate(city_legends):
        ms = cities_sizes[n][0]
        line, = ax.plot(np.nan, 'o', ms=ms, mew=ms/3, mec='k', mfc=cities_colors[n])
        handles_labels.append([line, label])

    leg = ax.legend(*zip(*handles_labels), loc=loc, ncol=ncol,
                    handler_map={
                        tuple: HandlerTuple(ndivide=None, pad=0),
                        Text: TextHandlerA()
                    }, bbox_to_anchor=bbox)
    leg.set_zorder(zorders['legend'])


def create_new_axes(fig, fig_ratio, x0=None, y0=None, dx=None, dy=None, pad=.0025):
    if dy is None: dy = 0.3
    if dx is None: dx = (dy * fig_ratio)
    if x0 is None: x0 = pad - .021
    if y0 is None: y0 = pad
    if y0 < 0: y0 = 1 - pad - dy

    ax = fig.add_axes((x0, y0, dx, dy))
    ax.set_xticks([])
    ax.set_yticks([])

    return ax


def complete_china_map():
    fig_ratio = 10/8.5
    fig_height = 8.5
    fig = plt.figure(figsize=(fig_height * fig_ratio, fig_height))

    ##### Main Axes #####
    ax = fig.add_axes((.045, .025, .9, .925))
    basemap = create_basemap(ax)

    # draw a boundary around the map, fill the background.
    # this background will end up being the ocean color, since
    # the continents will be drawn on top.
    # basemap.drawmapboundary(fill_color='lightblue', zorder=zorders['ocean'])
    # basemap.fillcontinents(color='grey', lake_color='lightblue', zorder=zorders['continent'])
    basemap.shadedrelief(scale=1., zorder=zorders['continent'])

    basemap.drawcountries(color='w', zorder=zorders['countries'], linewidth=2)

    parallels = np.arange(20, 51, 5)
    meridians = np.arange(75, 136, 5)
    basemap.drawparallels(parallels, zorder=zorders['par/med'], labels=[True]*len(parallels))
    basemap.drawmeridians(meridians, zorder=zorders['par/med'], labels=[True]*len(meridians))

    # basemap.drawcoastlines(color='w', zorder=zorders['provinces'])
    draw_provinces(ax, basemap, show_outline=True, show_background=False)
    # draw_provinces(ax, basemap)
    draw_rivers(ax, basemap)
    draw_cities(ax, basemap)

    add_legends(ax, loc='upper center', ncol=3, bbox=(0,0,1,1))

    ##### Bottom Left Axes #####
    ax_corner_bl = create_new_axes(fig, fig_ratio)

    basemap_corner_bl = create_basemap(ax_corner_bl)
    basemap_corner_bl.etopo(scale=1, zorder=zorders['continent'])
    basemap_corner_bl.drawcountries(color='w', zorder=zorders['countries'], linewidth=1)

    # basemap_corner_bl.drawparallels(parallels, zorder=zorders['par/med'])
    # basemap_corner_bl.drawmeridians(meridians, zorder=zorders['par/med'])

    draw_provinces(ax_corner_bl, basemap_corner_bl, show_labels=False, lw_mult=.5,
                show_outline=True, show_background=False)
    draw_rivers(ax_corner_bl, basemap_corner_bl, show_labels=False, lw_mult=.3)
    draw_cities(ax_corner_bl, basemap_corner_bl, show_labels=False, ms_mult=.4)

    # ##### Top Left Axes #####
    ax_corner_tl = create_new_axes(fig, fig_ratio, dy=.25, y0=-1)

    basemap_corner_tl = create_basemap(ax_corner_tl)

    basemap_corner_tl.drawmapboundary(fill_color='lightblue', zorder=zorders['ocean'])
    basemap_corner_tl.fillcontinents(color='grey', lake_color='lightblue', zorder=zorders['continent'])
    basemap_corner_tl.drawcountries(color='k', zorder=zorders['countries'], linewidth=1)

    # basemap_corner_tl.drawparallels(parallels, zorder=zorders['par/med'])
    # basemap_corner_tl.drawmeridians(meridians, zorder=zorders['par/med'])

    draw_provinces(ax_corner_tl, basemap_corner_tl, show_labels=False)
    draw_rivers(ax_corner_tl, basemap_corner_tl, show_labels=False, lw_mult=.3)
    draw_cities(ax_corner_tl, basemap_corner_tl, show_labels=False, ms_mult=.4)

    ##### Top Center Axes #####
    # ax_top_center = create_new_axes(fig, fig_ratio, dy=.25, y0=-1, x0=.36)
    # ax_top_center.axis('off')

    ax.set_title('Political and River Map of China', y=1.025)

    # plt.tight_layout()
    plt.savefig(image_folder + f'china_map{"_full" if resolution != "c" else ""}.png',
                dpi=300)

    if PRINT_ALL_CITIES:
        plt.show()
    else:
        plt.close()
    print('Done')


if __name__ == '__main__':
    complete_china_map()
