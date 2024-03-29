import cv2
import numpy
import enum
import csv
from dataclasses import dataclass
from matplotlib import colors

class Control(enum.Enum):
    DEBUG = True

@dataclass
class MainKeys:
    EXIT = 'q'
    COLORPICKER = 'c'
    CROPOBJECT = 'o'
    TRACKBAR = 't'
    HSVCONTROL = 'h'
    STOPPLAYING = ' '

@dataclass
class Frame:
    main = None
    mask = None
    gray = None
    blur = None
    hsv = None

@dataclass
class HsvConfiguration:
    colorname = 'orange'
    lowerblue = 0
    upperblue = 196
    lowergreen = 113
    uppergreen = 163
    lowerred = 135
    upperred = 188

@dataclass
class TrackingConfiguration:
    pass

class TheBall:
    def __init__(self) -> None:
        self.trackbarsrc = False
        self.starttrackbar = False
        self.colors_mouse_picker = []
        self.posations_of_mouse = []

    def get_posation_with_hsv(
            self, 
            mat:numpy.ndarray,
            lower:tuple = None, 
            upper:tuple = None,
            ) -> None:
        
        if not isinstance(mat, numpy.ndarray):
            return None

        if not lower and not upper:
            lower = (HsvConfiguration.lowerblue,
                     HsvConfiguration.lowergreen,
                     HsvConfiguration.lowerred)
            
            upper = (HsvConfiguration.upperblue,
                     HsvConfiguration.uppergreen,
                     HsvConfiguration.upperred)
        
        lower = numpy.array(lower)
        upper = numpy.array(upper)

        Frame.hsv = cv2.cvtColor(mat, cv2.COLOR_BGR2HSV)
        Frame.mask = cv2.inRange(Frame.hsv, lower, upper)
        Frame.mask = cv2.erode(Frame.mask, None, iterations = 1)
        Frame.mask = cv2.dilate(Frame.mask, None, iterations = 2)

        mask_copy = Frame.mask.copy()

        cnts = cv2.findContours(
            mask_copy, 
            cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        if len(cnts) < 1:
            if Control.DEBUG.value:
                mat_copy = mat.copy()
                cv2.rectangle(mat_copy, (0, 0), (20, 20), 
                                         (0, 0, 255), -1) 
                cv2.imshow('HSV_Result', mat_copy)
            return None
        
        maxc = max(cnts, key = cv2.contourArea)
        
        ((x_posation, y_posation), radius) = cv2.minEnclosingCircle(maxc)
        
        x_posation = int(x_posation)  
        y_posation = int(y_posation)
          
        if Control.DEBUG.value:
            mat_copy = mat.copy()
            font = cv2.FONT_HERSHEY_SIMPLEX  
            cv2.putText(mat_copy, 'Detected', (40,60), font, 0.5, 
                                    (255,255,255), 1, cv2.LINE_AA)
            cv2.rectangle(mat_copy, (0, 0), (20, 20), 
                                     (255, 0, 0), -1) 
            cv2.rectangle(mat_copy, (int(x_posation-radius),int(y_posation+radius)),  
                  (int(x_posation+radius),int(y_posation-radius)), (255,255,255), 1) 
            cv2.imshow('HSV_Result', mat_copy)

        return (x_posation, y_posation, radius)

    def get_posation_with_tracking(self):
        pass

    def predict_posation_ball(self):
        pass
    

    def configs_key_control(self):
        key = cv2.waitKey(1) & 0xFF
        key = chr(key) if key != -1 else None
        
        match key:
            case None:
                return None
            
            case MainKeys.EXIT: # exiting
                return -1
            
            case MainKeys.TRACKBAR:
                self.starttrackbar = not self.starttrackbar
                cv2.destroyAllWindows()
                self.trackbarsrc = False

            case MainKeys.STOPPLAYING:
                while True:
                    if cv2.waitKey(1) & 0xFF == ord(MainKeys.STOPPLAYING):
                        break
            
            case MainKeys.COLORPICKER: # color picker
                self.trackbarsrc = False
                minr, ming, minb, maxr, maxg, maxb = self.color_picker(Frame.hsv)
                print(minr, ming, minb, maxr, maxg, maxb)
                if minr is not None:
                    HsvConfiguration.lowerblue = minb #mainb-5
                    HsvConfiguration.upperblue = maxb #mainb+20
                    HsvConfiguration.lowergreen = ming #maing-20
                    HsvConfiguration.uppergreen = maxg #maing+20
                    HsvConfiguration.lowerred = minr #mainr-20
                    HsvConfiguration.upperred = maxr #mainr+20
    
    def color_picker(self, image:numpy.ndarray) -> tuple:
        if not isinstance(image, numpy.ndarray):
            print('TypeError: image must be numpy.ndarray')
            return None, None, None
        
        brightnes = [.9, 1, 1.1]
        images = []
        self.colors_mouse_picker = []
        for persent in brightnes:
            images.append(self.brightness(image, persent, persent))
        image = numpy.hstack(images)

        while True:
            cv2.imshow('picking_color', image)
            cv2.setMouseCallback('picking_color', self.on_mouse_click, image)
            print(self.colors_mouse_picker)
            if cv2.waitKey(1) & 0xFF == ord(MainKeys.COLORPICKER):
                cv2.destroyAllWindows()
                if self.colors_mouse_picker == []:
                    return None, None, None, None, None, None
                minb = min(c[0] for c in self.colors_mouse_picker)
                ming = min(c[1] for c in self.colors_mouse_picker)
                minr = min(c[2] for c in self.colors_mouse_picker)
                maxb = max(c[0] for c in self.colors_mouse_picker)
                maxg = max(c[1] for c in self.colors_mouse_picker)
                maxr = max(c[2] for c in self.colors_mouse_picker)
                # avgb = int(sum(c[0] for c in self.colors_mouse_picker) / len(self.colors_mouse_picker))
                # avgg = int(sum(c[1] for c in self.colors_mouse_picker) / len(self.colors_mouse_picker))
                # avgr = int(sum(c[2] for c in self.colors_mouse_picker) / len(self.colors_mouse_picker))
                return minr, ming, minb, maxr, maxg, maxb

    def on_mouse_click(self, event, x_posation, y_posation, 
                                     flags, frame) -> None:
        if event == cv2.EVENT_LBUTTONUP:
            self.colors_mouse_picker.append(frame[y_posation,x_posation].tolist())
            self.posations_of_mouse.append((x_posation, y_posation))

    def the_trackbar_hsv(self):
        if not self.starttrackbar:
            return
        if not self.trackbarsrc:
            self.trackbarsrc = True
            self.trackbarlist = (
                ('low_blue', HsvConfiguration.lowerblue, 255), 
                ('high_blue', HsvConfiguration.upperblue, 255), 
                ('low_green', HsvConfiguration.lowergreen, 255),
                ('high_green', HsvConfiguration.uppergreen, 255),
                ('low_red', HsvConfiguration.lowerred, 255),
                ('high_red', HsvConfiguration.upperred, 255)
            )
            cv2.namedWindow('HsvConfiguration')
            for color, down, up in self.trackbarlist:
                cv2.createTrackbar(color,'HsvConfiguration', down, up, 
                                                            lambda x:x)
        HsvConfiguration.lowerblue = int(cv2.getTrackbarPos('low_blue', 'HsvConfiguration'))
        HsvConfiguration.upperblue = int(cv2.getTrackbarPos('high_blue', 'HsvConfiguration'))
        HsvConfiguration.lowergreen = int(cv2.getTrackbarPos('low_green', 'HsvConfiguration'))
        HsvConfiguration.uppergreen = int(cv2.getTrackbarPos('high_green', 'HsvConfiguration'))
        HsvConfiguration.lowerred = int(cv2.getTrackbarPos('low_red', 'HsvConfiguration'))
        HsvConfiguration.upperred = int(cv2.getTrackbarPos('high_red', 'HsvConfiguration'))
        cv2.imshow('HsvConfiguration', Frame.mask)

    def brightness(self, 
                   img:numpy.ndarray, 
                   first_argument:float, 
                   secound_argument:float) -> numpy.ndarray:
        hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv = numpy.array(hsv_image, dtype = numpy.float64)
        
        hsv[:,:,1] = hsv[:,:,1] * first_argument
        hsv[:,:,1][hsv[:,:,1]>255]  = 255

        hsv[:,:,2] = hsv[:,:,2] * secound_argument
        hsv[:,:,2][hsv[:,:,2]>255]  = 255

        hsv_image = numpy.array(hsv, dtype = numpy.uint8)
        img = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        return img

    def write_and_read(
            self, 
            namefile:str = None,
            indata:any = None
            ) -> list:
        pass