import requests
import json

def get_methods(api_endpoint):
    all_endpoints = []
    ignore_list = ["index","libraries","relatedtools"]
    if api_endpoint in ignore_list:
        return
    url = "https://raw.githubusercontent.com/hashicorp/vault/main/website/content/api-docs/" + api_endpoint + ".mdx"
    req = requests.get(url)
    if req.status_code != 200:
        return
    content = req.content.decode("utf-8")

    for line in content.splitlines():
        if line.startswith("| `"):
            arr = line.split("|")
            all_endpoints.append(arr[1].replace("`", "").strip() + " " + arr[2].replace("`", "").strip())

    return all_endpoints

def get_paths(routes):
    current_list = []
    for key in routes:
        if key == "path":
            current_list.append(routes[key])
        if key == "routes":
            for x in routes[key]:
                current_list.extend(get_paths(x))
    return current_list

def main():
    req = requests.get("https://raw.githubusercontent.com/hashicorp/vault/main/website/data/api-docs-nav-data.json")
    path_list = []
    endpoints = []
    if req.status_code == 200:
        payload = json.loads(req.content)
        for key in payload:
            path_list.extend(get_paths(key))
    for path in path_list:
        current = get_methods(path)
        if current is not None:
            endpoints.extend(current)
    
    print(endpoints)

if __name__ == "__main__":
    main()


