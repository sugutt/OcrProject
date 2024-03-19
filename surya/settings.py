from typing import Dict, Optional

from dotenv import find_dotenv
from pydantic import computed_field
from pydantic_settings import BaseSettings
import torch
import os


class Settings(BaseSettings):
    # General
    TORCH_DEVICE: Optional[str] = None
    IMAGE_DPI: int = 96

    # Paths
    DATA_DIR: str = "data"
    RESULT_DIR: str = "results"
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FONT_DIR: str = os.path.join(BASE_DIR, "static", "fonts")

    @computed_field
    def TORCH_DEVICE_MODEL(self) -> str:
        if self.TORCH_DEVICE is not None:
            return self.TORCH_DEVICE

        if torch.cuda.is_available():
            return "cuda"

        return "cpu"

    @computed_field
    def TORCH_DEVICE_DETECTION(self) -> str:
        if self.TORCH_DEVICE is not None:
            return self.TORCH_DEVICE

        # Does not work with mps
        if torch.cuda.is_available():
            return "cuda"

        return "cpu"

    # Text detection
    DETECTOR_BATCH_SIZE: Optional[int] = None # Defaults to 2 for CPU, 32 otherwise
    DETECTOR_MODEL_CHECKPOINT: str = "vikp/surya_det2"
    DETECTOR_MATH_MODEL_CHECKPOINT: str = "vikp/surya_det_math"
    DETECTOR_BENCH_DATASET_NAME: str = "vikp/doclaynet_bench"
    DETECTOR_IMAGE_CHUNK_HEIGHT: int = 1400 # Height at which to slice images vertically
    DETECTOR_TEXT_THRESHOLD: float = 0.6 # Threshold for text detection (above this is considered text)
    DETECTOR_BLANK_THRESHOLD: float = 0.35 # Threshold for blank space (below this is considered blank)

    # Text recognition
    RECOGNITION_MODEL_CHECKPOINT: str = "vikp/surya_rec"
    RECOGNITION_MAX_TOKENS: int = 175
    RECOGNITION_BATCH_SIZE: Optional[int] = None # Defaults to 8 for CPU/MPS, 256 otherwise
    RECOGNITION_IMAGE_SIZE: Dict = {"height": 196, "width": 896}
    RECOGNITION_RENDER_FONTS: Dict[str, str] = {
        "all": os.path.join(FONT_DIR, "GoNotoCurrent-Regular.ttf"),
        "zh": os.path.join(FONT_DIR, "GoNotoCJKCore.ttf"),
        "ja": os.path.join(FONT_DIR, "GoNotoCJKCore.ttf"),
        "ko": os.path.join(FONT_DIR, "GoNotoCJKCore.ttf"),
    }
    RECOGNITION_FONT_DL_BASE: str = "https://github.com/satbyy/go-noto-universal/releases/download/v7.0"
    RECOGNITION_BENCH_DATASET_NAME: str = "vikp/rec_bench"
    RECOGNITION_PAD_VALUE: int = 0 # Should be 0 or 255

    # Layout
    LAYOUT_MODEL_CHECKPOINT: str = "vikp/surya_layout"

    # Tesseract (for benchmarks only)
    TESSDATA_PREFIX: Optional[str] = None

    @computed_field
    @property
    def MODEL_DTYPE(self) -> torch.dtype:
        return torch.float32 if self.TORCH_DEVICE_MODEL == "cpu" else torch.float16

    @computed_field
    @property
    def MODEL_DTYPE_DETECTION(self) -> torch.dtype:
        return torch.float32 if self.TORCH_DEVICE_DETECTION == "cpu" else torch.float16

    class Config:
        env_file = find_dotenv("local.env")
        extra = "ignore"


settings = Settings()