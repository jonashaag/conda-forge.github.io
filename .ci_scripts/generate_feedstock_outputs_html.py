import os
import sys
import glob

import tqdm
import jinja2
import rapidjson as json
import requests

input_file = sys.argv[1]
output_file = sys.argv[2]
feedstocks_repo = sys.argv[3]

with open(input_file) as fp:
    tmpl = jinja2.Template(fp.read())

outputs = glob.glob(
    os.path.join(feedstocks_repo, "outputs", "**/*.json"),
    recursive=True,
)

packages = {}
for output in tqdm.tqdm(outputs):
    key = os.path.basename(output).replace(".json", "")
    with open(output, "r") as fp:
        packages[key] = json.load(fp)

channeldata_packages = requests.get("https://conda.anaconda.org/conda-forge/channeldata.json").json()["packages"]
# Example package info:
# {'binary_prefix': True,
#  'description': 'This model simulates subsurface flow, fate, and transport of contaminants that are undergoing chemical or biological transformations. This model is applicable to transient conditions in both saturated and unsaturated zones.',
#  'dev_url': None,
#  'doc_url': 'https://nepis.epa.gov/Adobe/PDF/P1006YEP.pdf',
#  'home': 'https://www.epa.gov/water-research/two-dimensional-subsurface-flow-fate-and-transport-microbes-and-chemicals-2dfatmic',
#  'license': 'Public Domain',
#  'source_url': None,
#  'summary': 'Two-Dimensional Subsurface Flow, Fate and Transport of Microbes and Chemicals Model',
#  'text_prefix': False,
#  'timestamp': 1602245775,
#  'version': '1.0',
#  'subdirs': ['win-64'],
#  'activate.d': True,
#  'deactivate.d': True,
#  'run_exports': {'4.5': {'weak': ['_openmp_mutex >=4.5']}},
#  'source_git_url': 'https://github.com/dmlc/xgboost',
#  'doc_source_url': 'https://github.com/sgillies/affine/blob/master/README.rst',
#  'post_link': True,
#  'pre_unlink': True,
#  'keywords': ['cosapp'],
#  'pre_link': True,
#  'identifiers': [{'doi': '10.5334/jors.161'}]}

for pkg, pkginfo in channeldata_packages.items():
    if pkg in packages:
        packages[pkg]["info"] = pkginfo
    else:
        print("misisng", pkg)

with open(output_file, "w") as fp:
    fp.write(tmpl.render({"packages": packages}))
