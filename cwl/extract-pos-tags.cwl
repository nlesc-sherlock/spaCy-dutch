#!/usr/bin/env cwlrunner
cwlVersion: cwl:v1.0
class: CommandLineTool
baseCommand: ["python", "/home/jvdzwaan/code/spaCy-dutch/commands/extract_pos_tags.py"]
arguments:
  - valueFrom: $(runtime.outdir)/
    position: 4

inputs:
- id: in_files
  type:
    type: array
    items: File
  inputBinding:
    position: 2

outputs:
- id: metadata_out
  type: File
  outputBinding:
    glob: ""
