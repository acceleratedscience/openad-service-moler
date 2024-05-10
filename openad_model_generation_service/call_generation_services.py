"""This library calls generation processes remotely on a given host"""

import json
from pathlib import Path
import glob
import definitions.services as new_prop_services
import os, copy, sys
import pandas as pd
from generation_applications import ApplicationsRegistry as GeneratorRegistry
from generation_applications import AVAILABLE_ALGORITHMS

print(AVAILABLE_ALGORITHMS)

# from ray import serve
from pydantic import BaseModel


class Info(BaseModel):
    conf_one: float
    conf_two: str
    conf_three: bool

    class Config:
        extra = "forbid"


class ConfStructure(BaseModel):
    version: int
    info: Info


docking_props = ["molecule_one", "askcos", "docking"]


def is_valid_service(service: dict):
    "to be completed"
    required_fields = [
        "service_name",
        "service_type",
        "parameters",
        "required_parameters",
        "category",
        "sub_category",
        "wheel_package",
        "GPU",
        "persistent",
        "help",
    ]

    for x in required_fields:
        if x not in service.keys():
            print("not valid service " + service["service_name"] + "   " + x)
            return False
    return True


def get_services() -> list:
    """pulls the list of available services for"""
    service_list = []
    service_files = glob.glob(os.path.abspath(os.path.dirname(new_prop_services.__file__) + "/*.json"))

    for file in service_files:
        print(file)
        with open(file, "r") as file_handle:
            try:
                jdoc = json.load(file_handle)
                if is_valid_service(jdoc):
                    service_list.append(jdoc)
            except Exception as e:
                print(e)
                print("invalid service json definition  " + file)
    return service_list


ALL_AVAILABLE_SERVICES = get_services()


# @serve.deployment


class service_requester:

    property_requestor = None
    valid_services = ["property", "prediction", "generation", "training"]

    def __init__(self) -> None:
        pass

    def is_valid_service_request(self, request) -> bool:
        return True

    def get_available_services(self):
        return ALL_AVAILABLE_SERVICES

    def route_service(self, request):
        result = None
        if not self.is_valid_service_request(request):
            return False
        category = None

        for service in ALL_AVAILABLE_SERVICES:
            current_service = None
            if (
                service["service_type"] == request["service_type"]
                and service["service_name"] == request["service_name"]
            ):
                category = service["category"]
                current_service = service
                break

        if current_service is None:
            print("service mismatch")
            return None
        if current_service["service_name"] in []:
            return [current_service["service_name"] + "   Not Currently Available"]

        if "sample_size" in request:
            try:
                SAMPLE_SIZE = int(request["sample_size"])

            except:
                SAMPLE_SIZE = 10
        else:
            SAMPLE_SIZE = 10

        if category == "generation":
            if self.property_requestor == None:
                self.property_requestor = request_generation()
            result = self.property_requestor.request(
                request["service_type"], request["parameters"], request["api_key"], SAMPLE_SIZE
            )

        return result

    async def __call__(self, req: json):
        req = await req.json()
        return self.route_service(req)


def get_generator_type(generator_application: str, parameters):
    service_list = get_services()
    for service in service_list:

        if (
            generator_application == service["service_type"]
            and service["generator_type"]["algorithm_application"] == parameters["property_type"][0]
        ):
            print("Generator")
            print(service)
            return service["generator_type"]

    return None


class request_generation:

    Generator_cache = []

    def __init__(self) -> None:
        pass

    def request(self, generator_application, parameters: dict, apikey: str, sample_size=10):
        results = []
        print("generator_application :" + generator_application + " params" + str(parameters))
        generator_type = get_generator_type(generator_application, parameters)
        if len(parameters["subjects"]) > 0:
            subject = parameters["subjects"][0]
        else:
            subject = None
        if generator_type is None:
            results.append({"subject": subject, "generator": generator_application, "result": "check Parameters"})
        try:
            parms = self.set_parms(generator_type=generator_type, parameters=parameters)
        except Exception as e:
            result = {"exception": str(e)}
            result = {"error": result}
            return result

        print(generator_type)
        parms.update(generator_type)
        print(parms)

        # try:
        if "target" in parms:
            target = copy.deepcopy(parms["target"])
            parms.pop("target")
            if isinstance(target, list):
                if len(target) == 1:
                    target = target[0]
            print("-----------------------------------------")
            print(parms)
            print("-----------------------------------------")
            print(target)
            print(sample_size)
            print("-----------------------------------------")

            model = GeneratorRegistry.get_application_instance(**parms, target=target)
        else:
            model = GeneratorRegistry.get_application_instance(**parms)

        # except Exception as e:
        #    exc_type, exc_obj, exc_tb = sys.exc_info()
        #    fname = "\n".join(os.path.split(exc_tb.tb_frame.f_code.co_filename))
        #    result = {"exception": str(exc_type) + "\n" + str(fname) + "\n" + str(exc_tb.tb_lineno)}
        #    result = {"error": result}
        #    return result

        try:
            result = list(model.sample(sample_size))
            result = pd.DataFrame(result)
            if len(result.columns) == 1:
                result.columns = ["result"]
            return result
        except OSError as e:
            result = e
            result = {"error": result}

        return result

    def set_parms(self, generator_type, parameters):
        request_params = {}
        service_list = get_services()
        for service in service_list:
            if generator_type == service["generator_type"]["algorithm_application"]:
                break

        if "required" in service.keys():
            for param in service["required"]:

                if param in ["subjects", "subject_type"]:
                    continue
                elif param in parameters.keys():
                    continue
                else:
                    print("no required " + param)
                    return None
        for param in parameters.keys():
            if param == "subjects":
                if len(parameters[param]) > 0:
                    request_params["target"] = parameters[param]
                continue
            if param in ["subject_type", "property_type"]:
                continue

            request_params[param] = parameters[param]

        return copy.deepcopy(request_params)


if __name__ == "__main__":
    from datetime import datetime

    dt = datetime.now()
    ts = datetime.timestamp(dt)
    print("Starting", datetime.fromtimestamp(ts))
    import test_request_generator
    import pandas as pd

    requestor = service_requester()
    dt = datetime.now()
    ts = datetime.timestamp(dt)

    print("Service Requestor Loaded ", datetime.fromtimestamp(ts))
    print("----------RUN SERVICES----------------------------------------")

    for request in test_request_generator.tests:
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        if request["service_type"] != "get_crystal_property":
            print(
                "\n\n Properties for subject:  " + ", ".join(request["parameters"]["subjects"]) + "   ",
                datetime.fromtimestamp(ts),
            )
            result = requestor.route_service(request)
            if result == None:
                print("Not Supported")
            else:
                print(pd.DataFrame(result))
        else:
            print("\n\n Properties for crystals")
            print()
            print(pd.DataFrame(requestor.route_service(request)))
