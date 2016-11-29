#!/usr/bin/env cwlrunner
cwlVersion: cwl:v1.0
class: CommandLineTool
baseCommand: ["python", "/home/jvdzwaan/code/spaCy-dutch/commands/cgn2universal4spacy.py"]
arguments:
  - valueFrom: $(runtime.outdir)/nl_tag_map.json
    position: 4

inputs:
- id: meta_in
  type: File
  inputBinding:
    position: 1

outputs:
- id: metadata_out
  type: File
  outputBinding:
    glob: "nl_tag_map.json"
