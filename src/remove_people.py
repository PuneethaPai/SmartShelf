import cv2
import itertools
import numpy as np

cols = 400

rows = 400

global background


def apply_mask(frame):
    fgmask = fgbg.apply(frame)
    fgmask = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR)
    return cv2.bitwise_and(frame, fgmask)


def griddify(image):
    row_index = [index for index in xrange(0, rows, rows/4)]
    col_index = [index for index in xrange(0, cols, cols/4)]
    grid_size = rows / 4
    image_grids = [image[r:r+grid_size, c:c+grid_size] for r in row_index for c in col_index]
    return image_grids


def combine(image_grids):
    row_index = [index for index in xrange(0, 16, 4)]
    rows = [np.hstack(image_grids[index:index+4]) for index in row_index]
    image = np.vstack(rows)
    return image


def just_background(frame, current_background):
    fgmask = fgbg.apply(frame)
    mask_grids = griddify(fgmask)
    frame_grids = griddify(frame)
    background_grids = griddify(current_background)
    result_grids = [background_grid if mask_grid.any() else frame_grid
                    for background_grid, mask_grid, frame_grid in itertools.izip(background_grids, mask_grids, frame_grids)]
    result_image = combine(result_grids)
    return result_image


mob = "/Users/puneethp/Downloads/Shelf Focusing Videos/Testing/test_2.3gp"
cap = cv2.VideoCapture(mob)
print cap.get(5)
cap.set(5, 200)

fgbg = cv2.createBackgroundSubtractorMOG2()
ret, background = cap.read()
background = cv2.resize(background, (rows, cols), interpolation=cv2.INTER_AREA)

while 1:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (rows, cols), interpolation=cv2.INTER_AREA)
    masked_frame = apply_mask(frame)
    background = just_background(frame, background)
    cv2.imshow('Video', frame)
    cv2.imshow('Mask', masked_frame)
    cv2.imshow('Result', background)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
