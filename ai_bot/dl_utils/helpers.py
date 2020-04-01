SUPPORTED_MODELS = ["mask-rcnn"]

def get_supported_models():
    return SUPPORTED_MODELS

def is_model_supported(model):
    return model in SUPPORTED_MODELS