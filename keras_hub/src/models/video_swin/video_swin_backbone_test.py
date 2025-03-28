import os
import numpy as np
import pytest
import keras
from keras import ops
from keras_hub.src.models.video_swin.video_swin_backbone import (
    VideoSwinBackbone,
)
from keras_hub.src.tests.test_case import TestCase


class TestVideoSwinSBackbone(TestCase):

    @pytest.mark.large
    def test_call(self):
        model = VideoSwinBackbone(  # TODO: replace with aliases
            include_rescaling=True, input_shape=(8, 256, 256, 3)
        )
        x = np.ones((1, 8, 256, 256, 3))
        x_out = ops.convert_to_numpy(model(x))
        num_parameters = sum(
            np.prod(tuple(x.shape)) for x in model.trainable_variables
        )
        self.assertEqual(x_out.shape, (1, 4, 8, 8, 768))
        self.assertEqual(num_parameters, 27_663_894)

    @pytest.mark.extra_large
    def teat_save(self):
        # saving test
        model = VideoSwinBackbone(include_rescaling=False)
        x = np.ones((1, 32, 224, 224, 3))
        x_out = ops.convert_to_numpy(model(x))
        path = os.path.join(self.get_temp_dir(), "model.keras")
        model.save(path)
        loaded_model = keras.saving.load_model(path)
        x_out_loaded = ops.convert_to_numpy(loaded_model(x))
        self.assertAllClose(x_out, x_out_loaded)

    @pytest.mark.extra_large
    def test_fit(self):
        model = VideoSwinBackbone(include_rescaling=False)
        x = np.ones((1, 32, 224, 224, 3))
        y = np.zeros((1, 16, 7, 7, 768))
        model.compile(optimizer="adam", loss="mse", metrics=["mse"])
        model.fit(x, y, epochs=1)

    @pytest.mark.extra_large
    def test_can_run_in_mixed_precision(self):
        keras.mixed_precision.set_global_policy("mixed_float16")
        model = VideoSwinBackbone(
            include_rescaling=False, input_shape=(8, 224, 224, 3)
        )
        x = np.ones((1, 8, 224, 224, 3))
        y = np.zeros((1, 4, 7, 7, 768))
        model.compile(optimizer="adam", loss="mse", metrics=["mse"])
        model.fit(x, y, epochs=1)

    @pytest.mark.extra_large
    def test_can_run_on_gray_video(self):
        model = VideoSwinBackbone(
            include_rescaling=False,
            input_shape=(96, 96, 96, 1),
            window_size=[6, 6, 6],
        )
        x = np.ones((1, 96, 96, 96, 1))
        y = np.zeros((1, 48, 3, 3, 768))
        model.compile(optimizer="adam", loss="mse", metrics=["mse"])
        model.fit(x, y, epochs=1)

    @pytest.mark.extra_large
    def test_can_run_non_square_shape(self):
        input_batch = np.ones(shape=(2, 8, 224, 256, 3))
        model = VideoSwinBackbone(
            input_shape=(8, 224, 256, 3),
            include_rescaling=False,
        )
        model(input_batch)
