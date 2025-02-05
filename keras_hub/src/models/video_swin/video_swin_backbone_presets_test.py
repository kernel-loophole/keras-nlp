# Copyright 2024 The Kerashub Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for loading pretrained model presets."""

import numpy as np
import pytest

from keras_hub.src.models.video_swin.video_swin_aliases import (
    VideoSwinTBackbone,
)
from keras_hub.src.models.video_swin.video_swin_backbone import (
    VideoSwinBackbone,
)
from keras_hub.src.tests.test_case import TestCase


@pytest.mark.large
class VideoSwinPresetSmokeTest(TestCase):
    """A smoke test for VideoSwin presets we run continuously.
    Run with:
    `pytest keras_hub/models/backbones/video_swin/video_swin_backbone_presets_test.py --run_large`  # noqa: E501
    """

    def setUp(self):
        self.input_batch = np.ones(shape=(1, 32, 224, 224, 3))

    def test_applications_model_output(self):
        model = VideoSwinBackbone()
        model(self.input_batch)

    def test_applications_model_output_with_preset(self):
        self.skipTest("TODO: Enable after Kaggle model is public")
        model = VideoSwinBackbone.from_preset("videoswin_tiny")
        model(self.input_batch)

    def test_applications_model_predict(self):
        self.skipTest("TODO: Enable after Kaggle model is public")
        model = VideoSwinTBackbone()
        model.predict(self.input_batch)

    def test_preset_docstring(self):
        """Check we did our docstring formatting correctly."""
        self.skipTest("TODO: Enable after Kaggle model is public")
        for name in VideoSwinBackbone.presets:
            self.assertRegex(VideoSwinBackbone.from_preset.__doc__, name)

    def test_unknown_preset_error(self):
        # Not a preset name
        with self.assertRaises(ValueError):
            VideoSwinBackbone.from_preset("videoswin_nonexistant")


@pytest.mark.extra_large
class VideoSwinPresetFullTest(TestCase):
    """Test the full enumeration of our preset.
    This tests every preset for VideoSwin and is only run manually.
    Run with:
    `pytest keras_hub/models/backbones/video_swin/video_swin_backbone_presets_test.py --run_extra_large`  # noqa: E501
    """

    def test_load_ViTDet(self):
        self.skipTest("TODO: Enable after Kaggle model is public")
        input_data = np.ones(shape=(1, 32, 224, 224, 3))
        for preset in VideoSwinBackbone.presets:
            model = VideoSwinBackbone.from_preset(preset)
            model(input_data)
