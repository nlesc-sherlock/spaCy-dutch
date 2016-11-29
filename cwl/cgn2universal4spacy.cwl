#!/usr/bin/env cwlrunner
cwlVersion: cwl:v1.0
class: CommandLineTool
baseCommand: ["python", "-m", "nlppln.cgn2universal4spacy"]
arguments:
  - valueFrom: $(runtime.outdir)/
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
    glob: ""

