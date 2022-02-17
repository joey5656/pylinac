from pylinac.core.image import DicomImage, ArrayImage, FileImage
from pylinac.core.profile import SingleProfile, MultiProfile
from pylinac import ct

import pydicom
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math

# -------------------------------------------------------
# Preliminary code setup: File, pixel spacing, profiles
# -------------------------------------------------------
filename = r"C:\Users\kjaps\Documents\Coding\Python\PyLinac\L2R and Dual Plannar\Processed\20220119_175002_6x [MV]_G360_C360_T360_97.dcm"
ds = pydicom.dcmread(filename)
arr = ds.pixel_array

# Get values from dicom tags for corrected px/mm at iso
sid = round(ds.RTImageSID, 1)
# sid=1500
print(f'SID: {sid}')
sad = round(ds.RadiationMachineSAD, 1)
px_spac_at_sid = np.mean(ds.ImagePlanePixelSpacing)
print(f'Pixel spacing at SID:{px_spac_at_sid}')
px_spac_corrected = px_spac_at_sid * (sad / sid)
print(f'Pixel spacing correction:{px_spac_corrected}')

dcm_img = DicomImage(filename)
arr_img = ArrayImage(arr, sid=sid)

# Get central row/col for the line profile
array_size_x = arr_img.shape[1]
array_size_y = arr_img.shape[0]
print(f'Array size (x):{array_size_x} Array size(y):{array_size_y}')
mid_array_x = int(array_size_x / 2)
mid_array_y = int(array_size_y / 2)

# Detect if the image needs inverting by checking pixel value of center vs corner.
if (arr_img[mid_array_x, mid_array_y] <= arr_img[0, 0]):
    arr_img.invert()

# Get array for row/col to plot as single profile
row = arr_img[mid_array_y, :]
col = arr_img[:, mid_array_x]
x_prof = SingleProfile(row)

testing = SingleProfile._geometric_center(self=SingleProfile,values=row)
print("This is" + str(testing))


y_prof = SingleProfile(col)
#x_prof.plot()
#y_prof.plot()
# ground profiles such that minimum = 0
x_prof.ground()
y_prof.ground()

# -------------------------------------
# Radiation Field Size and Center
# -------------------------------------
# Find central coordinate of the radiation field from the profile's full width half max
x_rad_center = round(x_prof.fwxm_data(50)['center index (exact)'])
y_rad_center = round(y_prof.fwxm_data(50)['center index (exact)'])
rad_center_coords = (x_rad_center, y_rad_center)
print(f'Radiation field center (pixels): {rad_center_coords}')

# Find the radiation field size
x_edges_left = x_prof.field_data()['left index (exact)']
x_edges_right = x_prof.field_data()['right index (exact)']
x_edges = [x_edges_left, x_edges_right]
x_size_px = x_edges[1] - x_edges[0]
x_size_mm = round(x_size_px * px_spac_corrected, 2)
x_size_cm = x_size_mm / 10
x1_edge = -round(x_edges[0], 2)
x2_edge = round(x_edges[1], 2)

y_edges_left = y_prof.field_data()['left index (exact)']
y_edges_right = y_prof.field_data()['right index (exact)']
y_edges = [y_edges_left, y_edges_right]
y_size_px = y_edges[1] - y_edges[0]
y_size_mm = round(y_size_px * px_spac_corrected, 2) #was px_spac_corrected
y_size_cm = y_size_mm / 10
y1_edge = -round(y_edges[1], 2)
y2_edge = round(y_edges[0], 2)

print(f'Radiation field size: \n Crossplane = {x_size_cm} cm \n Inplane = {y_size_cm} cm')
# print(f'Y edges:{y_edges} X edges:{x_edges}')

mid_array_x = int(array_size_x/2)
mid_array_y = int(array_size_y/2)
pixel_bounds_x = 50
pixel_bounds_y = 50
#ROI for analysis
xbounds_mid = (int(mid_array_x - (pixel_bounds_x/2)), int(mid_array_x + (pixel_bounds_y/2)))
ybounds_mid = (int(mid_array_y - (pixel_bounds_y/2)), int(mid_array_y + (pixel_bounds_y/2)))
geo_img_mid = ds.pixel_array[ybounds_mid[0]:ybounds_mid[1], xbounds_mid[0]:xbounds_mid[1]]
arr_img_mid = ArrayImage(geo_img_mid, sid=sid)

# ------------------------------
# Light Field Center form BB's
# ------------------------------
# Phantom is aligned to light-field. Central position of the 4 eqally spaced BB's == light field center.

fc2_10_rois = {
    'roi 1': {'x distance from center': 0.0, 'y distance from center': 0.0},
    'roi 2': {'x distance from center': -4.0, 'y distance from center': 4.0},
    'roi 3': {'x distance from center': 4.0, 'y distance from center': 4.0},
    'roi 4': {'x distance from center': -4.0, 'y distance from center': -4.0},
    'roi 5': {'x distance from center': 4.0, 'y distance from center': -4.0}
}

fc2_15_rois = {
    'roi 1': {'x distance from center': 0.0, 'y distance from center': 0.0},
    'roi 2': {'x distance from center': -6.5, 'y distance from center': 6.5},
    'roi 3': {'x distance from center': 6.5, 'y distance from center': 6.5},
    'roi 4': {'x distance from center': -4.0, 'y distance from center': 4.0},
    'roi 5': {'x distance from center': 4.0, 'y distance from center': 4.0},
    'roi 6': {'x distance from center': -4.0, 'y distance from center': -4.0},
    'roi 7': {'x distance from center': 4.0, 'y distance from center': -4.0},
    'roi 8': {'x distance from center': -6.5, 'y distance from center': -6.5},
    'roi 9': {'x distance from center': 6.5, 'y distance from center': -6.5}
}

# using pylinac modules to find BB. Bounds are created as a search region
roi_size_px = 25
centers = []
if x_size_cm > 13:  #is 15x15
    rois = fc2_15_rois.values()
else:  #is 10x10
    rois = fc2_10_rois.values()
for stng in rois:
    print(stng['x distance from center'])
    xbounds_shift = x_rad_center + stng['x distance from center']/px_spac_corrected * 10
    ybounds_shift = y_rad_center + stng['y distance from center']/px_spac_corrected * 10
    print(xbounds_shift, ybounds_shift)
    xbounds = (int(xbounds_shift - roi_size_px/2), int(xbounds_shift + roi_size_px/2))
    ybounds = (int(ybounds_shift - roi_size_px/2), int(ybounds_shift + roi_size_px/2))
    print(xbounds, ybounds)
    geo_img = ds.pixel_array #[ybounds[0]:ybounds[1], xbounds[0]:xbounds[1]]  # returns array within the bounded area
    print(geo_img)
    larr, regionprops, num_roi = ct.get_regions(geo_img, fill_holes=True, clear_borders=False)
    center = [(round(regionprops[0].weighted_centroid[1] + xbounds[0], 2), round(regionprops[0].weighted_centroid[0] + ybounds[0], 2))]
    centers += center

print('centers',centers[0])
x_bb = [centers[0]]
y_bb = [centers[0]]
print("X_bb", x_bb,"y_bb", y_bb)
# Centers is list of tuples (x, y) for the 4 BB's. Central pixel coordinate (x, y),
# where x = average of x for all 4 points, and y = average of y for all 4 points.
print(f'Outer BBs:{centers}')


x_light_center = round(centers[0][0], 2)
y_light_center = round(centers[0][1], 2)
light_center_coords = (x_light_center, y_light_center)

print(f'Light field center (pixels): {light_center_coords}')

# ------------------------------------
# Light-Rad Field Center Difference
# ------------------------------------
x_diff_mm = round((centers[0][0] - x_rad_center) * px_spac_corrected, 2)
y_diff_mm = round((centers[0][1] - y_rad_center) * px_spac_corrected, 2)

print(f'Light-Rad difference: \n X/Y: {x_diff_mm} / {y_diff_mm} mm')

if x_size_mm < 120:
    fieldsize = 50
if x_size_mm > 130:
    fieldsize = 75
x1_diff_mm = round((centers[0][0] + x1_edge) * px_spac_corrected - fieldsize, 2)
x2_diff_mm = -round((centers[0][0] - x2_edge) * px_spac_corrected + fieldsize, 2)
y1_diff_mm = -round((centers[0][1] + y1_edge) * px_spac_corrected + fieldsize, 2)
y2_diff_mm = round((centers[0][1] - y2_edge) * px_spac_corrected - fieldsize, 2)

print(f' Left/Right: {round(x1_diff_mm, 3)} / {round(x2_diff_mm, 3)} mm')
print(f' Top/Bottom: {round(y2_diff_mm, 3)} / {round(y1_diff_mm, 3)} mm')

# ------------------------------------
# Light Field Angle of Rotation
# ------------------------------------
# Use the BB coodinates to find phantom angle (and therefore light field angle if set to lightfield correctly)
# 4 BB's are 0,1,2,3 from top left, top right, bottom left, bottom right respectively
bb0_1_radians = math.atan2(centers[0][1] - centers[1][1], centers[0][0] - centers[1][0])
bb0_1_degrees = math.degrees(bb0_1_radians)

# bb0_2_radians = math.atan2(y_bb[2]-y_bb[0], x_bb[2]-x_bb[0])
# bb0_2_degrees = math.degrees(bb0_2_radians) - 90

# bb2_3_radians = math.atan2(y_bb[3]-y_bb[2], x_bb[3]-x_bb[2])
# bb2_3_degrees = math.degrees(bb2_3_radians)

# bb1_3_radians = math.atan2(y_bb[3]-y_bb[1], x_bb[3]-x_bb[1])
# bb1_3_degrees = math.degrees(bb1_3_radians) - 90

# angles = [bb0_1_degrees, bb0_2_degrees, bb2_3_degrees, bb1_3_degrees]

# light_angle = np.mean(angles)
light_angle = bb0_1_degrees
print(f'Lightfield Rotation = {light_angle:.3f} degrees')

# ------------------------------------
# Radiation Field Angle of Rotation
# ------------------------------------
# Get array for row/col to plot as single profile
off_center = int(25 / px_spac_corrected)  # mm in pixels to shift the profile off center

# make profiles offset 6cm either side of the center
offset_row_1 = arr_img[mid_array_y - off_center, :]
offset_x_prof1 = SingleProfile(offset_row_1)

offset_row_2 = arr_img[mid_array_y + off_center, :]
offset_x_prof2 = SingleProfile(offset_row_2)

offset_col_1 = arr_img[:, mid_array_x - off_center]
offset_y_prof1 = SingleProfile(offset_col_1)

offset_col_2 = arr_img[:, mid_array_x + off_center]
offset_y_prof2 = SingleProfile(offset_col_2)

# Find the radiation edge from FWHM for each offset profile
x1_offset_edges = offset_x_prof1.field_data()['field values']
x2_offset_edges = offset_x_prof2.field_data()['field values']

y1_offset_edges = offset_y_prof1.field_data()['field values']
y2_offset_edges = offset_y_prof2.field_data()['field values']

offset_edges = {'left - offset': (x1_offset_edges[0], mid_array_y - off_center),
                'right - offset': (x1_offset_edges[1], mid_array_y - off_center),
                'left + offset': (x2_offset_edges[0], mid_array_y + off_center),
                'right + offset': (x2_offset_edges[1], mid_array_y + off_center),

                'top - offset': (mid_array_x - off_center, y1_offset_edges[0]),
                'bottom - offset': (mid_array_x - off_center, y1_offset_edges[1]),
                'top + offset': (mid_array_x + off_center, y2_offset_edges[0]),
                'bottom + offset': (mid_array_x + off_center, y2_offset_edges[1])
                }

# find the angles between the points
# math.atan2(y1 - y0, x1 - x0) = radians between 2 points
top_edge_radians = math.atan2(offset_edges['top + offset'][1] - offset_edges['top - offset'][1],
                              offset_edges['top + offset'][0] - offset_edges['top - offset'][0])
top_edge_degrees = math.degrees(top_edge_radians)

bottom_edge_radians = math.atan2(offset_edges['bottom + offset'][1] - offset_edges['bottom - offset'][1],
                                 offset_edges['bottom + offset'][0] - offset_edges['bottom - offset'][0])
bottom_edge_degrees = math.degrees(bottom_edge_radians)

left_edge_radians = math.atan2(offset_edges['left + offset'][1] - offset_edges['left - offset'][1],
                               offset_edges['left + offset'][0] - offset_edges['left - offset'][0])
left_edge_degrees = math.degrees(left_edge_radians) - 90

right_edge_radians = math.atan2(offset_edges['right + offset'][1] - offset_edges['right - offset'][1],
                                offset_edges['right + offset'][0] - offset_edges['right - offset'][0])
right_edge_degrees = math.degrees(left_edge_radians) - 90

radiation_angle = np.mean([top_edge_degrees, bottom_edge_degrees, left_edge_degrees, right_edge_degrees])
print(f'Radiation Field Rotation = {radiation_angle:.3f} degrees')

# ------------------------------------------------
# Plotting the profiles and image (if you want)
# ------------------------------------------------
fig, (ax1, ax2) = plt.subplots(2, sharey=True)
distance_x = [x * px_spac_corrected for x in range(0, ds.Columns, 1)]
distance_y = [y * px_spac_corrected for y in range(0, ds.Rows, 1)]

ax1.plot(distance_x, x_prof)
ax1.set_title('Crossplane')
ax1.set_xlabel('Distance (mm)')
ax1.set_ylabel('Pixel Value')

ax2.plot(distance_y, y_prof)
ax2.set_title('Inplane')
ax2.set_xlabel('Distance (mm)')
ax2.set_ylabel('Pixel Value')

fig.tight_layout()
plt.show()

# Plot image with lines showing crossplane and inplane.
fig2, ax3 = plt.subplots(1)
plt.imshow(ds.pixel_array, cmap='gray', vmin=np.mean(arr_img_mid)*0.5, vmax=np.mean(arr_img_mid))
# Draw line to visualise where profiles taken from.
ax3.axvline(x=mid_array_x, c='g')
ax3.axhline(y=mid_array_y, c='g')
ax3.axvline(x=x_light_center, c='r')
ax3.axhline(y=y_light_center, c='r')
ax3.axvline(x=centers[0][0], c='y')
ax3.axhline(y=centers[0][1], c='y')
ax3.axvline(x=x_rad_center, c='b')
ax3.axhline(y=y_rad_center, c='b')

ax3.scatter(*zip(*centers), c='red')
ax3.scatter(centers[0][0], centers[0][1], c='purple')
ax3.scatter(*zip(*list(offset_edges.values())), c='orange')

# Create a Rectangle patch outlining the radiation field
rec_roi = patches.Rectangle((x_edges[0], y_edges[0]),
                            x_size_px, y_size_px,
                            linewidth=1, edgecolor='b', facecolor='none')
# Add the patch to the Axes
ax3.add_patch(rec_roi)

fig.tight_layout()
plt.show()

lvr_upload_analysis = {
    'Lightfield_diff_x': x_diff_mm,
    'Lightfield_diff_y': y_diff_mm,
    'X1 diff': x1_diff_mm,
    'X2 diff': x2_diff_mm,
    'Y1 diff': y1_diff_mm,
    'Y2 diff': y2_diff_mm,
    'X size': x_size_mm,
    'Y size': y_size_mm,
    'Light angle': light_angle,
    'Radiation angle': radiation_angle
}