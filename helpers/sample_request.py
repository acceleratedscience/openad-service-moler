tests = []

tests.append(
    {
        "service_name": "generate with RegressionTransformerMolecules",
        "service_type": "generate_data",
        "parameters": {
            "property_type": ["RegressionTransformerMolecules"],
            "subjects": "<esol>-3.53|[Br][C][=C][C][MASK][MASK][=C][C][=C][C][=C][Ring1][MASK][MASK][Branch2_3][Ring1][Branch1_2]",
            "algorithm_version": "solubility",
            "search": "sample",
            "temperature": 2.0,
            "tolerance": "5.0",
        },
        "api_key": "api-dthgwrhrthrtrth",
        "sample_size": "5",
    }
)
