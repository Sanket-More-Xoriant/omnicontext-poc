# generate specs
import json


class SpecificationAgent:

    def generate(
        self,
        analysis
    ):

        spec = {
            "analysis": analysis
        }

        with open(
            "data/generated_spec.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                spec,
                file,
                indent=4,
                ensure_ascii=False
            )

        return spec