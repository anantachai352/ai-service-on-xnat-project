import pydicom
import datetime
from PIL import Image
import cv2



def image_To_dicom(header, jpg_arr):

    # Recreate dicom tag 
    # Set up DICOM metadata fields. Most of them will be the same as original file header
    dicom_file = pydicom.dcmread(header, force=True)
    out = pydicom.Dataset(dicom_file)
    out.file_meta = pydicom.Dataset()

    out.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
    
    out.is_little_endian = True
    out.is_implicit_VR = False

    # We need to change class to Secondary Capture
    out.SOPClassUID = "1.2.840.10008.5.1.4.1.1.7" # Other class UID

    out.file_meta.MediaStorageSOPClassUID = out.SOPClassUID

    
    # set Instance UID (0020,000D)
    
    out.StudyInstanceUID = dicom_file.StudyInstanceUID
    studyInstanceUID = str(dicom_file.StudyInstanceUID)
    print("out.StudyInstanceUID: ", studyInstanceUID)

    # Series Instance UID (0020,000E)
    out.SeriesInstanceUID = pydicom.uid.generate_uid() #dicom_file.SeriesInstanceUID #"1.2.826.0.1.3680043.8.498.10364834036499017370462231161035836235"
    out.SOPInstanceUID = pydicom.uid.generate_uid()
    out.file_meta.MediaStorageSOPInstanceUID = out.SOPInstanceUID
    out.Modality = "OT" # Other
    out.SeriesDescription = "VUNO_AI" #dicom_file.SeriesDescription

    # Define StudyDescription as the same as project_id (This can be viewed by default by OHIF)
    out.StudyDescription = "studyDes" #  project_id #"VUNO_AI" #dicom_file.StudyDescription ########

    out.Rows = jpg_arr.shape[0]
    out.Columns = jpg_arr.shape[1]
    print("Rows:", jpg_arr.shape[0])
    print("Columns:", jpg_arr.shape[1])

    # out.InstanceNumber = dicom_file.InstanceNumber # for slicing view
    out.ImagePositionPatient = [0,0,1] # for slicing view
    out.ImageType = r"DERIVED\PRIMARY\AXIAL" # We are deriving this image from patient data
    out.SamplesPerPixel = 3 # we are building an RGB image.
    out.PhotometricInterpretation = "RGB"
    out.PlanarConfiguration = 0 # means that bytes encode pixels as R1G1B1R2G2B2... as opposed to R1R2R3...G1G2G3...
    out.BitsAllocated = 8 # we are using 8 bits/pixel
    out.BitsStored = 8
    out.HighBit = 7
    out.PixelRepresentation = 0

    # Set time and date
    dt = datetime.date.today().strftime("%Y%m%d")
    tm = datetime.datetime.now().strftime("%H%M%S")
    out.StudyDate = dt
    out.StudyTime = tm
    out.SeriesDate = dt
    out.SeriesTime = tm

    out.ImagesInAcquisition = 1

    # We empty these since most viewers will then default to auto W/L
    out.WindowCenter = ""
    out.WindowWidth = ""

    # Data imprinted directly into image pixels is called "burned in annotation"
    out.BurnedInAnnotation = "YES"
    jpg_arr = cv2.cvtColor(jpg_arr, cv2.COLOR_BGR2RGB)
    out.PixelData = jpg_arr.tobytes()
    return out


