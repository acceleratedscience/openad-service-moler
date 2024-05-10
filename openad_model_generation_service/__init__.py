#
# MIT License
#
# Copyright (c) 2022 GT4SD team
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Module initialization for gt4sd_common ."""
from gt4sd_common.extras import EXTRAS_ENABLED

# NOTE: here we import the applications to register them

try:
    from gt4sd_common.algorithms.conditional_generation.molgx import MolGXQM9Generator  # noqa: F401
except:
    pass

try:
    from gt4sd_inference_moler.algorithms.generation.moler import MoLeRDefaultGenerator  # noqa: F401
except:
    pass


from dataclasses import Field


def get_generator_parameters(Generator):
    Properties = {}
    for key, item in Generator.__pydantic_model__.schema()["properties"].items():
        Properties[key] = item

    return (
        Generator.__pydantic_model__.schema()["title"],
        Generator.__pydantic_model__.schema()["description"],
        Properties,
    )


# print(PaccMannGPGenerator.__pydantic_model__.schema())
# print(GraphGAGenerator.__pydantic_model__.schema())
