import numpy as np
import tensorflow as tf
from scipy.special import logsumexp

# ----- Unified Detector -----
class UnifiedUnknownDetector:
    def __init__(self,model,load_dir,temperature:float = 1):
        self.model = model
        self.load_dir = load_dir
        self.temperature = temperature

        #Load Detection Parameters
        self._load_detection_params(load_dir)


    def _load_detection_params(self,load_dir):
        try:
            # Enery thresholds
            self.crop_energy_threshold = float(np.load(f"{load_dir}/crop_energy_threshold.npy"))
            self.disease_energy_threshold = float(np.load(f"{load_dir}/disease_energy_threshold.npy"))

            # Softmax thresholds
            self.crop_softmax_threshold = float(np.load(f"{load_dir}/crop_softmax_threshold.npy"))
            self.disease_softmax_threshold = float(np.load(f"{load_dir}/disease_softmax_threshold.npy"))

        except FileNotFoundError as e:
            print(f"ERROR: Missing some files: {e}")
            raise
        
    def _compute_energy(self, logits):
        logits = logits / self.temperature
        return -np.log(np.sum(np.exp(logits), axis=-1))
           

    def predict(self,image,crop_labels=None,disease_labels=None,return_details=False):
        # Ensure batch dimension
        if len(image.shape) == 3:
            image = np.expand_dims(image, axis=0)
  
        #model
        crop_logits, disease_logits = self.model.predict(image,verbose=0)

        # ------ Energy Based Detection ----- 
        crop_energy = float(self._compute_energy(crop_logits)[0])
        disease_energy = float(self._compute_energy(disease_logits)[0])
        energy_unknown = (crop_energy > self.crop_energy_threshold) or (disease_energy > self.disease_energy_threshold)


        # ------- Softmax Confidence Detection ---------
        crop_probs = tf.nn.softmax(crop_logits, axis=-1).numpy()
        disease_probs = tf.nn.softmax(disease_logits, axis=-1).numpy()
        crop_max_prob = float(np.max(crop_probs))
        disease_max_prob = float(np.max(disease_probs))
        softmax_unknown = (crop_max_prob < 0.6) and (disease_max_prob < 0.6)

        is_unknown = energy_unknown

        # -------- PREDICTED CLASSES
        crop_idx = int(np.argmax(crop_probs, axis=-1)[0])
        disease_idx = int(np.argmax(disease_probs, axis=-1)[0])

        # --------- LABEL MAPPING
        crop_name = (crop_labels.get(crop_idx) if crop_labels else crop_idx)
        disease_name = (disease_labels.get(disease_idx) if disease_labels else disease_idx)

        # disease_name = (f"{crop_name}_healthy") if (crop_max_prob > 0.6) else disease_name
        # crop_name = (disease_name.split("_")[0]) if (disease_max_prob > 0.6) else crop_name

        # UNKNOWN RESULT
        if is_unknown:

            result = {
                "is_unknown": True,
                "label": "unknown",

                "energy_unknown":energy_unknown,
                "softmax_unknown": softmax_unknown,

                "crop": crop_name,
                "disease": disease_name,

                "crop_confidence": crop_max_prob,
                "disease_confidence": disease_max_prob,

                "crop_energy": crop_energy,
                "disease_energy": disease_energy,

            }

            return result if return_details else "unknown"

        # ----- Build Return Result
        result = {
            "is_unknown": False,

            "energy_unknown":energy_unknown,
            "softmax_unknown": softmax_unknown,

            "label": f"{crop_name}_{disease_name}",

            "crop": crop_name,
            "disease": disease_name,

            "crop_index": crop_idx,
            "disease_index": disease_idx,

            "crop_confidence": crop_max_prob,
            "disease_confidence": disease_max_prob,

            "crop_energy": crop_energy,
            "disease_energy": disease_energy,

        }

        return result if return_details else result["label"]
