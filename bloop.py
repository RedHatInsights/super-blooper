#!/usr/bin/env python

import json
import requests
import argparse
import config

parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, required=True, help='Input query file path.')
parser.add_argument('--config', type=str, default="config.yml", help='Path to config.yml')
args = parser.parse_args()

config = config.get_config(args.config)


def get_query(file):
    with open(file, "r") as f:
        json_data = f.read()
    return json_data


def graphql_request(url, payload):
    headers = {"Content-Type": "application/json",
               "Accept": "application/json",
               "Connection": "keep-alive",
               "DNT": "1"}
    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        print("Error:", response.status_code, response.text)


def find_insights_assets(data):
    insights_assets = []
    for asset in data["data"]["saas_files_v2"]:
        if not asset.get("labels"):
            continue
        labels = json.loads(asset["labels"])
        if "platform" in labels and labels["platform"] == "insights":
            insights_assets.append(asset)
    return insights_assets


def get_namespace_info(data):

    namespace_info = []
    for asset in data:
        for resource in asset["resourceTemplates"]:
            resource_name = resource["name"]
            for target in resource["targets"]:
                if target["namespace"]["name"] not in config.namespaces:
                    continue
                if "namespace" in target and target["namespace"]["name"] not in namespace_info:
                    params = target.get('parameters', {})
                    if params and params != {}:
                        params = json.loads(params)
                    namespace_info.append({
                        'resource': resource_name,
                        'ns': target['namespace']['name'],
                        'ref': target.get('ref', ''),
                        'image_tag': target.get('ref')[:7],
                        'params': params,
                    })
    return namespace_info


def filter_production(data):
    filtered_assets = []
    for asset in data:
        if "prod" in str(asset["ns"]).lower():
            filtered_assets.append(asset)
    return filtered_assets


if __name__ == "__main__":
    json_payload = get_query(args.file)
    data = graphql_request(config.graphql_endpoints["source_a"], json_payload)
    insights_assets = find_insights_assets(data)
    result_data = get_namespace_info(insights_assets)
    filtered_data = filter_production(result_data)
    print(json.dumps(filtered_data, indent=4))
