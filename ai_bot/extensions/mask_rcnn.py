import torchvision
import torch

from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor

class MaskRCNN():

    def __init__(self):
        self.model = self.build_model()
        self.model.eval()
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def build_model(self):
         # Define model and change according to our dataset
        model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)

        # # get number of input features for the classifier
        # in_features = model.roi_heads.box_predictor.cls_score.in_features
        # # replace the pre-trained head with a new one
        # model.roi_heads.box_predictor = FastRCNNPredictor(in_features)

        # # now get the number of input features for the mask classifier
        # in_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
        # hidden_layer = 256
        # # and replace the mask predictor with a new one
        # model.roi_heads.mask_predictor = MaskRCNNPredictor(in_features_mask,
        #                                                hidden_layer)
        return model
    
    def predict(self, images):
        predictions = []
        with torch.no_grad():
            for image in images:
                
                predictions.append(self.model([image.to(self.device)]))