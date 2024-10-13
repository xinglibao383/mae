import torch
import models_mae


class MAEFeatureExtractor:
    def __init__(self, model_name, checkpoint_path, device=None):
        self.device = device or self.prepare_device()
        self.model = self.prepare_model(model_name, checkpoint_path, self.device)

    @staticmethod
    def prepare_device():
        return torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    @staticmethod
    def load_model_checkpoint(model, checkpoint_path):
        checkpoint = torch.load(checkpoint_path)
        model.load_state_dict(checkpoint["model"])
        return model

    def prepare_model(self, model_name, checkpoint_path, device):
        model = models_mae.__dict__[model_name](norm_pix_loss=False)
        model.to(device)
        model = self.load_model_checkpoint(model, checkpoint_path)
        return model

    def extract_features(self, input_tensor, use_cls_token=False):
        self.model.eval()
        with torch.no_grad():
            features = self.model.forward_encoder_without_mask(input_tensor)

        return features[:, 0, :] if use_cls_token else features[:, 1:, :]

    def extract(self, input_tensor, use_cls_token=False):
        input_tensor = input_tensor.to(self.device)
        return self.extract_features(input_tensor, use_cls_token)


if __name__ == '__main__':
    model_name = 'mae_vit_base_patch4'
    checkpoint_path = '../output_dir/20241012193444/checkpoint-49.pth'

    extractor = MAEFeatureExtractor(model_name, checkpoint_path)

    input_tensor = torch.randn(64, 1, 128, 16)

    features = extractor.extract(input_tensor)

    print(f'Extracted features shape: {features.shape}')