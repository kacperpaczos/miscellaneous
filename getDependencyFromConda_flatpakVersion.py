import json
import subprocess
import hashlib
import requests
from datetime import datetime

def create_conda_env():
    print("Initiating process: Creation of conda environment")
    subprocess.run(['conda', 'create', '--name', 'temp', '--dry-run', '--json', 'jupyterlab', '-c', 'conda-forge'], stdout=open('dependencies.json', 'w'))

def load_json_file():
    print("Initiating process: Loading JSON file")
    with open('dependencies.json', 'r') as file:
        data = json.load(file)
        links = data['actions']['LINK']
    return links

def process_links(links):
    install = []
    mamba_install = []
    sources = []
    print("Initiating process: Processing each link")
    for link in links:
        name, version = link['name'], link['version']
        install.append(f'install -Dm 755 -t $FLATPAK_DEST/download {name}.conda')
        mamba_install.append(f'$FLATPAK_DEST/anaconda/bin/mamba install $FLATPAK_DEST/download/{name}.conda')
        url = f'https://anaconda.org/conda-forge/{name}/{version}/download/linux-64/{name}-{version}.conda'
        print(f"Process: Downloading file from URL: {url}")
        try:
            response = requests.get(url)
            sha256_hash = hashlib.sha256(response.content).hexdigest()
            sources.append({
                '- type': 'file',
                'only-arches': ' x86_64',
                'url': url,
                'sha256': sha256_hash,
                'dest-filename': f'{name}.conda'
            })
        except:
            print("Failure occurred. Exception handling initiated. Unable to calculate checksum.")
            sources.append({
                '- type': 'file',
                'only-arches': ' x86_64',
                'url': url,
                'sha256': 'idontknow',
                'dest-filename': f'{name}.conda'
            })
    return install, mamba_install, sources

def display_sources(install, mamba_install, sources):
    print("===========================================")
    print("Initiating process: Displaying all sources")
    print("===========================================")
    for i in install:
        print(i)
    print("-------------------------------------------")
    for i in mamba_install:
        print(i)
    print("-------------------------------------------")
    for s in sources:
        print(f"- type: {s['- type']}")
        print(f"  only-arches:\n    -{s['only-arches']}")
        print(f"  url: {s['url']}")
        print(f"  sha256: {s['sha256']}")
        print(f"  dest-filename: {s['dest-filename']}")
    print("--------------------------------------------")
    print(f"Date and time: {datetime.now()}")

def write_output_to_file(install, mamba_install, sources):
    with open(f"output_{datetime.now().strftime('%Y%m%d_%H%M')}.txt", "a") as file:
        file.write("===========================================\n")
        file.write("Initiating process: Displaying all sources\n")
        file.write("===========================================\n")
        for i in install:
            file.write(i + "\n")
        file.write("-------------------------------------------\n")
        for i in mamba_install:
            file.write(i + "\n")
        file.write("-------------------------------------------\n")
        for s in sources:
            file.write(f"- type: {s['- type']}\n")
            file.write(f"  only-arches:\n    -{s['only-arches']}\n")
            file.write(f"  url: {s['url']}\n")
            file.write(f"  sha256: {s['sha256']}\n")
            file.write(f"  dest-filename: {s['dest-filename']}\n")
        file.write("--------------------------------------------\n")
        file.write(f"Date and time: {datetime.now()}\n")

def main():
    create_conda_env()
    links = load_json_file()
    install, mamba_install, sources = process_links(links)
    display_sources(install, mamba_install, sources)
    write_output_to_file(install, mamba_install, sources)

if __name__ == "__main__":
    main()


