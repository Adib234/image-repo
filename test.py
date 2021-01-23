# import base64
# data = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAADBQTFRFA6b1q Ci5/f2lt/9yu3 Y8v2cMpb1/DSJbz5i9R2NLwfLrWbw m T8I8////////SvMAbAAAABB0Uk5T////////////////////AOAjXRkAAACYSURBVHjaLI8JDgMgCAQ5BVG3//9t0XYTE2Y5BPq0IGpwtxtTP4G5IFNMnmEKuCopPKUN8VTNpEylNgmCxjZa2c1kafpHSvMkX6sWe7PTkwRX1dY7gdyMRHZdZ98CF6NZT2ecMVaL9tmzTtMYcwbP y3XeTgZkF5s1OSHwRzo1fkILgWC5R0X4BHYu7t/136wO71DbvwVYADUkQegpokSjwAAAABJRU5ErkJggg=='.replace(
#     ' ', '+')
# print(data)
# imgdata = base64.b64decode(data)
# filename = 'some_image.jpg'
# with open(filename, 'wb') as f:
#     f.write(imgdata)

import os
filename = 'some_image.jpg'
os.remove(filename)
