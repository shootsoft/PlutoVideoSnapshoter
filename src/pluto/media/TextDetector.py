import cv2


class TextDetector(object):

    def __init__(self):
        pass

    def detect_text_rect(self, image, threshold=250):
        """
        See https://stackoverflow.com/questions/24385714/detect-text-region-in-image-using-opencv
        :return:
        """
        img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, threshold, 255, cv2.THRESH_BINARY)
        image_final = cv2.bitwise_and(img2gray, img2gray, mask=mask)
        ret, new_img = cv2.threshold(image_final, threshold, 255,
                                     cv2.THRESH_BINARY)  # for black text , cv.THRESH_BINARY_INV
        '''
                line  8 to 12  : Remove noisy portion
        '''
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,
                                                             3))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
        dilated = cv2.dilate(new_img, kernel, iterations=9)  # dilate , more the iteration more the dilation
        im2, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # get contours

        rectangles = list()
        for contour in contours:
            # get rectangle bounding contour
            [x, y, w, h] = cv2.boundingRect(contour)

            # Don't plot small false positives that aren't text
            if w < 35 and h < 35:
                continue
            rectangles.append(Rect([x, y, w, h]))
            # draw rectangle around contour on original image
            # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
        rectangles.sort(key=lambda r: r.y, reverse=False)
        return rectangles

    def detect_subtitle_range(self, filename):
        image = cv2.imread(filename)
        height, width, channels = image.shape
        y_up = height * 0.6
        y_down = height
        rectangles = self.detect_text_rect(image)
        for rect in rectangles:
            if rect.y < y_up:
                continue
            if rect.y > y_up:
                y_up = rect.y
                break
        last_rect = rectangles[len(rectangles) - 1]
        max_down = last_rect.y + last_rect.height + max(last_rect.height * 0.3, 30)
        y_down = max_down if max_down < height else last_rect.y + last_rect.height
        # if y_down < max_down:
        #    y_down = max_down
        return int(y_up), int(y_down)


class Rect(object):
    def __init__(self, array):
        self.x = 0 if len(array) == 0 else array[0]
        self.y = 0 if len(array) < 1 else array[1]
        self.width = 0 if len(array) < 2 else array[2]
        self.height = 0 if len(array) < 3 else array[3]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "x=%s, y=%s, width=%s, height=%s" % (self.x, self.y, self.width, self.height)
