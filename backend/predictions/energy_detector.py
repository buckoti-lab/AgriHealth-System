import numpy as np
import tensorflow as tf
from scipy.special import logsumexp


class EnergyBasedUnknownDetector:

    def __init__(self, model, temperature=0.1):

        self.model = model
        self.temperature = temperature

        # self.crop_energy_threshold = -10.0
        # self.disease_energy_threshold = -10.0
        self.crop_energy_threshold = float(np.load("models/crop_threshold.npy"))
        self.disease_energy_threshold = float(np.load("models/disease_threshold.npy"))

    # ==========================================
    # ENERGY FUNCTION
    # ==========================================
    def _calculate_energy(self, logits):

        return -self.temperature * logsumexp(
            logits / self.temperature,
            axis=-1
        )

    # ==========================================
    # PREDICTION WITH UNKNOWN DETECTION
    # ==========================================
    def predict_with_unknown(
        self,
        image,
        crop_labels=None,
        disease_labels=None,
        return_details=False
    ):


        # Ensure batch dimension
        if len(image.shape) == 3:
            image = np.expand_dims(image, axis=0)

        # ==========================================
        # MODEL OUTPUTS (LOGITS)
        # ==========================================
        crop_logits, disease_logits = self.model.predict(
            image,
            verbose=0
        )

        # ==========================================
        # SOFTMAX PROBABILITIES
        # ==========================================
        crop_probs = tf.nn.softmax(crop_logits, axis=-1).numpy()
        disease_probs = tf.nn.softmax(disease_logits, axis=-1).numpy()

        # ==========================================
        # CONFIDENCE SCORES
        # ==========================================
        crop_confidence = float(np.max(crop_probs))
        disease_confidence = float(np.max(disease_probs))

        # ==========================================
        # ENERGY SCORES
        # ==========================================
        crop_energy = float(
            self._calculate_energy(crop_logits)[0]
        )

        disease_energy = float(
            self._calculate_energy(disease_logits)[0]
        )
        
        is_unknown = (
            crop_energy > self.crop_energy_threshold or
            disease_energy > self.disease_energy_threshold or
            crop_confidence < 0.60 or
            disease_confidence < 0.60
        )

        # ==========================================
        # PREDICTED CLASSES
        # ==========================================
        crop_idx = int(np.argmax(crop_probs, axis=-1)[0])
        disease_idx = int(np.argmax(disease_probs, axis=-1)[0])

        # ==========================================
        # LABEL MAPPING
        # ==========================================
        crop_name = (
            crop_labels.get(crop_idx)
            if crop_labels else crop_idx
        )

        disease_name = (
            disease_labels.get(disease_idx)
            if disease_labels else disease_idx
        )

        # ==========================================
        # UNKNOWN RESULT
        # ==========================================
        if is_unknown:

            result = {
                "is_unknown": True,
                "label": "unknown",

                "crop": None,
                "disease": None,

                "crop_confidence": None,
                "disease_confidence": None,

                "crop_energy": crop_energy,
                "disease_energy": disease_energy,

                "crop_threshold": self.crop_energy_threshold,
                "disease_threshold": self.disease_energy_threshold
            }

            return result if return_details else "unknown"

        # ==========================================
        # KNOWN RESULT
        # ==========================================
        result = {
            "is_unknown": False,

            "label": f"{crop_name}_{disease_name}",

            "crop": crop_name,
            "disease": disease_name,

            "crop_index": crop_idx,
            "disease_index": disease_idx,

            "crop_confidence": crop_confidence,
            "disease_confidence": disease_confidence,

            "crop_energy": crop_energy,
            "disease_energy": disease_energy,

            "crop_threshold": self.crop_energy_threshold,
            "disease_threshold": self.disease_energy_threshold
        }

        return result if return_details else result["label"]